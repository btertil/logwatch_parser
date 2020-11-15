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

lista = os.listdir("eml/hrankiety/")
print(len(lista))
print(lista[:5])

counter = 0
for l in lista:
    flag = False
    if "Logwatch for " in l:
        flag = True
        print(l, flag)
        counter += 1
    else:
        pass
    
print(counter)
