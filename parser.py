import re
import os


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

# Każdy mail z logawatch jest parsowany po kolei
for log_tuple in logs:

    log_srv = log_tuple[0]
    log_msg = log_tuple[1]

    # only logwatch messages / mails
    if "Logwatch for " in log_msg:

        counter += 1
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
                        httpd_ips += re.findall(ip_pattern, line)

                    if sshd_flag:
                        sshd_ips += re.findall(ip_pattern, line)

            print("\n\nfile {}: {} ({}): {}\n\thttpd probing ips: {}\n\tssh succesull logins: {}"
                  .format(counter, log_srv, date_msg, log_msg, ", ".join(httpd_ips), ", ".join(sshd_ips)))
                    

