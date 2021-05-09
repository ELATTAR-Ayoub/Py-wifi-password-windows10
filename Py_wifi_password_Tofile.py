#-----------------------------Besmi allah-----------------------------------------------

#This import allows you ur code to use system commands (windows cmd)
import subprocess

#Impoprt the re module allows you to use regular expressions. (find a specific text in some output and do something with it).
import re

#Import os to open our text file in default program after we are done.
import os

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

#We gonna use the re modules so ewe can find regular expressions (specific text in output).
#We gonna search for thye wifi names which always listed after "All User Profile" in the output of the command line
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

#We gonna create an empty list to store all wifi names in it.
#User names and password will be saved.
wifi_list = list()

#if we didn't find profile names--> that's mean we don't have connection.
#we will continue the process with just wifi we have connection with, and try to get there info.
if len(profile_names) != 0:
    for name in profile_names:
        #every wifi connection will need its dictionnary to store info in.
        # so we will create to every wifi a dict.
        wifi_profile = dict()
        #we gonna now to run "netsh wlan show  profiles <wifi name>" in cmd to get info.
        #if the security key is present, we could hopefuly get there password.
        wifi_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        # we gonna use regular expression to look for the absent cases so we ignore them.
        if re.search("Security Key            : Absent", wifi_info):
            continue
        else:
            #assign the ssid of the wifi to the dict
            wifi_profile["ssid"] = name
            #for the cases that are not absent, we need to run the code "key=clear" to get there password
            profile_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            #after that we gonna searsh for "Key Content" with re method to find the password.
            password = re.search("Key Content            : (.*)\r", profile_pass)
            #if we found a password in the regular expression, we gonna store it. otherwise we won't.
            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            #we append(add) the wifi information to the wifi list
            wifi_list.append(wifi_profile)

print("Loading...")

for i in range(len(wifi_list)):
    stringFile = str(wifi_list[i]) + "\n"

myFile = open("Wifi_Passwords" + ".txt", 'w') # w means we can write in the file, if the file already excist it will overwrite it
myFile.write(stringFile) #write the wifi-list in the file
myFile.close() # close the file

print("Done.")
