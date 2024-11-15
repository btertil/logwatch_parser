import re
import os
import sys
import psycopg2
from dbsqls import drop_logwatch_entries_sql, create_logwatch_entries_sql, create_views_list
from dbsettings import db_settings as dbs


# definicja specjalnych linii
httpd_begin = " --------------------- httpd Begin ------------------------"
httpd_end = " ---------------------- httpd End -------------------------"
scan_line = "       /"
sshd_begin = " --------------------- SSHD Begin ------------------------"
sshd_end = " ---------------------- SSHD End -------------------------"

# regexp używane do znajdowania ip i dat
ip_pattern = r" \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
date_pattern = r"\d{4}\-\d{2}\-\d{2}"

# logi serwera prod i backup
logs = [("backup", "./eml/backup/" + i) for i in os.listdir("eml/backup/")]
logs += [("hrankiety", "./eml/hrankiety/" + i) for i in os.listdir("eml/hrankiety/")]

# ole plików sparsowano
counter = 0


# funkcja do spr czy zmatchowano z patternem ipv4
def isipv4(addr):

    try:
        octets = [int(i) for i in addr.split(".")]
        o0 = (octets[0] >= 0) & (octets[0] <= 255)
        o1 = (octets[1] >= 0) & (octets[1] <= 255)
        o2 = (octets[2] >= 0) & (octets[2] <= 255)
        o3 = (octets[3] >= 0) & (octets[3] <= 255)
        return o0 & o1 & o2 & o3

    except ValueError:
        return False


if __name__ == "__main__":

    replace_flag = False

    if len(sys.argv) > 1:
        if sys.argv[1] == "-r" or sys.argv[1] == "--replace":
            print("[!] NOTE! -r or --replace parameter provided, all logwatch data will be replaced in the database")
            replace_flag = True
        else:
            print("[-] Unknown parameter: " + sys.argv[1])
            print("Run parser without additional arguments if you want to parse logs only")
            print("Use: \"-r\" or \"--replace\" if you want to replace all existing data in logwatch_parser database")
            exit(1)

    try:
        conn = psycopg2.connect(**dbs)
        cursor = conn.cursor()
        print("[+] Database connection established")

        # format inserta
        insert_sql = "insert into logwatch_entries (server, log_date, service, ip, comment, logwatch_file) values "

        # placeholder for all insert statement (file level)
        # it might have duplicates as a single ip can be mentioned several times on different lines
        # Eg: (like rev dns, httpd probes with proxy + ip, etc), later it will be filtered by set()
        insert_sql_all = []

        # Każdy mail z logawatch jest parsowany po kolei
        for log_tuple in logs:

            log_srv = log_tuple[0]
            log_msg = log_tuple[1]

            # only logwatch messages / mails
            if "Logwatch for " in log_msg:

                counter += 1

                # zawsze jedna data tylko w nazwie wiadomości z logwatch
                date_msg = re.findall(date_pattern, log_msg)[0]

                with open("{}".format(log_msg), "r") as file:
                    lines = file.read()

                    # re-setting flags for a new file / message
                    httpd_flag = False
                    sshd_flag = False

                    httpd_ips = []
                    sshd_ips = []

                    # parse log messages line by line
                    for line in lines.split("\n"):
                        if line not in ("", " ", "\n"):

                            # is it httpd line?
                            if not httpd_flag and httpd_begin in line:
                                httpd_flag = True
                            if httpd_flag and httpd_end in line:
                                httpd_flag = False

                            # is it sshd line?
                            if not sshd_flag and sshd_begin in line:
                                sshd_flag = True
                            if sshd_flag and sshd_end in line:
                                sshd_flag = False

                            if httpd_flag:
                                httpd_ips = re.findall(ip_pattern, line)
                                if len(httpd_ips) > 0:
                                    for ip in set(httpd_ips):
                                        if isipv4(ip):
                                            line_add = "(\'{}\', \'{}\', \'httpd\', \'{}\', \'httpd probing\', \'{}\')"\
                                                .format(log_srv, date_msg, ip.lstrip(), log_msg)
                                            insert_sql_all += [line_add]

                            if sshd_flag:
                                sshd_ips = re.findall(ip_pattern, line)
                                if len(sshd_ips) > 0:
                                    for ip in set(sshd_ips):
                                        if isipv4(ip):
                                            line_add = "(\'{}\', \'{}\', \'sshd\', \'{}\', \'ssh logged-in\', \'{}\')"\
                                                .format(log_srv, date_msg, ip.lstrip(), log_msg)
                                            insert_sql_all += [line_add]

        # inserting only unique enties as some of ips might be duplicated because mentioned several times
        # within sshd or httpd sections
        unique_inserts = set(insert_sql_all)
        values = ", ".join(unique_inserts)
        insert_sql += values

        print("[+] Logwatch messages/logs parsed: " + str(counter))
        print("[+] Unique inserts (ip, service, server and date entries): " + str(len(unique_inserts)))

        # DO NOT RUN !!! this APPEND DATA TO DATABASE
        if replace_flag:
            try:
                cursor.execute(drop_logwatch_entries_sql)
                conn.commit()
                print("[+] The existing logwach table has been successfully dropped", flush=True)
                cursor.execute(create_logwatch_entries_sql)
                conn.commit()
                print("[+] The new logwach table has been successfully created", flush=True)

                cursor.execute(insert_sql)
                conn.commit()
                print("[+] OK, all rows successfully inserted!", flush=True)

                cursor.execute("ANALYZE public.logwatch_entries")
                print("[+] Statistics calculated", flush=True)

                v_cnt = 0
                for v in create_views_list:
                    cursor.execute(v)
                    conn.commit()
                    v_cnt += 1

                print("[+] Analytical views created: " + str(v_cnt), flush=True)
                print("[+] Done!", flush=True)

            except psycopg2.Error as err:
                print("[-] Insert failed:\n" + str(err))

        cursor.close()
        conn.close()

    except psycopg2.Error as err:
        print("[-] Database problem:\n" + str(err))
