import re
import os

# Wazne linie do starts with:
# Date:

httpd_begin = " --------------------- httpd Begin ------------------------"
httpd_end = " ---------------------- httpd End -------------------------"
scan_line = "       /"
sshd_begin = " --------------------- SSHD Begin ------------------------"
sshd_end = " ---------------------- SSHD End -------------------------"

eml_path = "home/bartek/eclipse-workspace/logwatch_parser/eml/hrankiety/*.eml"

ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
date_pattern = r"\d{4}\-d{2}\-d{2}"

#import glob
#print(glob.glob(eml_path))

#lista = os.listdir("eml/hrankiety/")
lista = os.listdir("eml/backup/")
#print(len(lista))
#print(lista[:5])

counter = 0

for el in lista:
    flag = False
    if "Logwatch for " in el:
        #flag = True
        #print(el, flag)
        counter += 1
        
        if counter < 9999:
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
                            httpd_ips +=  re.findall(ip_pattern, line)
                            
                        if sshd_flag:
                            sshd_ips +=  re.findall(ip_pattern, line)    
                        
                        #print(line, httpd_flag, sshd_flag)
                
                print("\n\nfile {}: {}\n\thttpd probing ips: {}\n\tssh succesull logins: {}".format(counter, el, ", ".join(httpd_ips), ", ".join(sshd_ips)))
                    

