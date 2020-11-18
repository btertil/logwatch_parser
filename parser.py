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
date_pattern = r"\d{4}\-d{2}\-d{2}"

# logi serwera prod i backup
# lista = os.listdir("eml/hrankiety/")
lista = os.listdir("eml/backup/")

counter = 0

# Każdy mail z logawatch jest parsowany po kolei
for el in lista:
    flag = False
    if "Logwatch for " in el:
        counter += 1
        
        with open("./eml/backup/{}".format(el), "r") as file:
            lines = file.read()

            # re-setting flags for a new file / message
            httpd_flag = False
            sshd_flag = False

            httpd_ips = []
            sshd_ips = []

            # parse log messages line by line
            for line in lines.split("\n"):
                if line not in (""," ", "\n"):

                    # is it httpd line?
                    if httpd_flag == False and httpd_begin in line:
                        httpd_flag = True
                    if httpd_flag == True and httpd_end in line:
                        httpd_flag = False

                    # is it sshd line?
                    if sshd_flag == False and sshd_begin in line:
                        sshd_flag = True
                    if sshd_flag == True and sshd_end in line:
                        sshd_flag = False

                    if httpd_flag:
                        httpd_ips += re.findall(ip_pattern, line)

                    if sshd_flag:
                        sshd_ips += re.findall(ip_pattern, line)

            print("\n\nfile {}: {}\n\thttpd probing ips: {}\n\tssh succesull logins: {}"
                  .format(counter, el, ", ".join(httpd_ips), ", ".join(sshd_ips)))
                    

