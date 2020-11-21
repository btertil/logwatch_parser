import re
import os
import psycopg2
from dbsettings import db_settings as dbs


# definicja specjalnych linii
httpd_begin = " --------------------- httpd Begin ------------------------"
httpd_end = " ---------------------- httpd End -------------------------"
scan_line = "       /"
sshd_begin = " --------------------- SSHD Begin ------------------------"
sshd_end = " ---------------------- SSHD End -------------------------"

# regexp używane do znajdowania ip i dat
ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
date_pattern = r"\d{4}\-\d{2}\-\d{2}"

# logi serwera prod i backup
logs = [("backup", "./eml/backup/" + i) for i in os.listdir("eml/backup/")]
logs += [("hrankiety", "./eml/hrankiety/" + i) for i in os.listdir("eml/hrankiety/")]

counter = 0

try:
    conn = psycopg2.connect(**dbs)
    cursor = conn.cursor()
    print("Database connection established")

    # format inserta
    insert_sql = "insert into logwatch_entries (server, log_date, service, ip, comment, logwatch_file) values "
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

                # placeholder for all insert statement (file level)
                # it might have duplicates as a single ip can be mentioned several times on different lines
                # Eg: (like rev dns, httpd probes with proxy + ip, etc), later it will be filtered by set()

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
                                    line_add = "(\'{}\', \'{}\', \'httpd\', \'{}\', \'httpd probing\', \'{}\')"\
                                        .format(log_srv, date_msg, ip, log_msg)
                                    insert_sql_all += [line_add]

                        if sshd_flag:
                            sshd_ips = re.findall(ip_pattern, line)
                            if len(sshd_ips) > 0:
                                for ip in set(sshd_ips):
                                    line_add = "(\'{}\', \'{}\', \'sshd\', \'{}\', \'ssh logged-in\', \'{}\')"\
                                        .format(log_srv, date_msg, ip, log_msg)
                                    insert_sql_all += [line_add]

    # inserting only unique enties as some of ips might be duplicated because mentioned several times
    # within sshd or httpd sections
    values = ", ".join(set(insert_sql_all))
    insert_sql += values

    # DO NOT RUN !!! this APPEND DATA TO DATABASE
    # cursor.execute(insert_sql)
    # conn.commit()

    # debug:
    # print("\n\nFinal insert_sql:\n" + insert_sql)

    cursor.close()
    conn.close()


except psycopg2.Error as err:
    print("Database problem:\n" + str(err.pgerror))


# TODO: poprawić odpowiednie psycopg2 errors: połąć czenie z bazą i błąd SQL
