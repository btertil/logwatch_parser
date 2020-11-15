import re
import os

# Wazne linie do starts with:
# Date:

httpd_begin = " --------------------- httpd Begin ------------------------"
httpd_end = " ---------------------- httpd End -------------------------"
#        /
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