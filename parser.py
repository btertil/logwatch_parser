import re
import os

# Wazne linie do starts with:
# Date:

httpd_begin = " --------------------- httpd Begin ------------------------"
httpd_end = " ---------------------- httpd End -------------------------"
scan_line = "       /"
sshd_begin = " --------------------- SSHD Begin ------------------------"
sshd_end = " ---------------------- SSHD End -------------------------"

https_flag = False
sshd_flag = False

eml_path = "home/bartek/eclipse-workspace/logwatch_parser/eml/hrankiety/*.eml"

#import glob
#print(glob.glob(eml_path))

#lista = os.listdir("eml/hrankiety/")
lista = os.listdir("eml/backup/")
print(len(lista))
print(lista[:5])

counter = 0
for el in lista:
    flag = False
    if "Logwatch for " in el:
        #flag = True
        #print(el, flag)
        counter += 1
        
        if counter < 3:
            with open("./eml/backup/{}".format(el), "r") as file:
                lines = file.read()
                
                # re-setting flags for a new file / message
                httpd_flag_begin_in_lines = False
                httpd_flag_end_in_lines = False
                sshd_flag_begin_in_lines = False
                sshd_flag_end_in_lines = False
                
                for line in lines.split("\n"):
                    if line not in (""," ", "\n"):
                        if sshd_flag_begin_in_lines == False and sshd_begin in line:
                            sshd_flag_begin_in_lines = True
                            sshd_flag_end_in_lines = False
                        if sshd_flag_end_in_lines == False and sshd_end in line:
                            sshd_flag_end_in_lines = True
                        
                        print(line, sshd_flag_begin_in_lines, sshd_flag_end_in_lines)
                    
                    #if sshd_begin in lines:
                    #    print("sshd_begin in lines")
                    #print(el)
                    #print(lines)
                    #lines = lines.split("\n")
                    #if sshd_begin in lines:
                    #    print("sshd_begin in lines")
                    #for line in lines:
                           #if line.contains(sshd_begin):
                           #    print("line == sshd_begin")
                           #    print(el, line)
        
    else:
        pass
    
print(counter)
