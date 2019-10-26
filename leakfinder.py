import argparse
import requests
import sys
import time
from colorama import init
init()
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from threading import Thread
import re
def banner():
	print("""\x1b[1m\x1b[92m               _          _            _       __ _           _           
  __ _ _   _| |_ ___   | | ___  __ _| | __  / _(_)_ __   __| | ___ _ __ 
 / _` | | | | __/ _ \  | |/ _ \/ _` | |/ / | |_| | '_ \ / _` |/ _ \ '__|
| (_| | |_| | || (_) | | |  __/ (_| |   <  |  _| | | | | (_| |  __/ |   
 \__,_|\__,_|\__\___/  |_|\___|\__,_|_|\_\ |_| |_|_| |_|\__,_|\___|_|   
                                                                          \x1b[0m """)
	print("\x1b[1m\x1b[94mby j0seph ..\x1b[0m" + "\n")
	parser = argparse.ArgumentParser() # daymen
	parser.add_argument("-f","--file", dest = "file" ,help="file containing emails", required = True)
	parser.add_argument("-p", "--pattern", dest = "pattern", help="emails (em) or phones(ph)",type=str, required = True)
	args = parser.parse_args() # dest hia li katkhlik tdirhou f variable
	pattern_choice = args.pattern #hethom f variable
	file_choice = args.file
	return file_choice,pattern_choice# //
def pattern_checker(pattern_choice): #chouf wach dekhel email oula tiliphone
	if pattern_choice == "em":
		pattern = pattern_email
	elif pattern_choice == "ph" :
		pattern = pattern_phone
	else :
		print("\x1b[1m\x1b[91m[-]invalid pattern name\x1b[0m \n")
		quit()
	return pattern
def write_to_file(resultat,r,i):
	"""output to file output.txt"""
	old_stdout = sys.stdout
	sys.stdout = open("output.txt","a")
	print("###################{}##################### : \n".format(resultat))
	print("\t{}\n".format(r.json()[i]["Name"]))
	sys.stdout = old_stdout
def file_open_and_extract(file_choice):
	""" jbed emails oula phones men fichier (rahom f match)"""
	global pattern_email
	global pattern_phone
	global match
	pattern_email = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+" #regex email
	pattern_phone = r"06\d{7}" # regex phone? machi mezyana
	pattern = pattern_checker(pattern_choice)
	with open(file_choice,"r") as fich :
		fichier_string = fich.read()
		match = re.findall(pattern, fichier_string, re.M)
		if pattern == pattern_email :
			a = "email(s)"
			print("\x1b[1m\x1b[94m[+]fetching emails ... \x1b[0m" )
		elif pattern == pattern_phone :
			a = "phone number(s)"
			print("\x1b[1m\x1b[94m[+]fetching phone numbers ...\x1b[0m")
		print("\n")
		if len(match) == 0 :
			print("\x1b[1m\x1b[91mno %s found.\x1b[0m"%a)
		else :
			print("\x1b[1m\x1b[92m[+]found %s %s\x1b[0m"%(len(match),a))
			time.sleep(3)
	return match
def request_maker(resultat) :
	global r
	url = "https://haveibeenpwned.com/api/v2/breachedaccount/{}?truncateResponse=true".format(resultat)
	sys.stdout.write("\x1b[93m[+]waiting for leaks for {} ... \n\x1b[0m".format(resultat))
	sys.stdout.flush()
	try :
		r = requests.get(url) #boom
	except KeyboardInterrupt :
		print("\n\x1b[1m\x1b[96m goodbye\x1b[0m")
		quit()
	if len(r.text) != 0 :
		sys.stdout.write("\x1b[92m[+]{} found in {} entrie(s) \n\x1b[0m".format(resultat,len(r.json())))
		time.sleep(3)
		sys.stdout.flush()
		sys.stdout.write("\x1b[92m[+]entries : \n\x1b[0m")
		for i in range(0, len(r.json())):
			sys.stdout.write("\x1b[1m\x1b[97m\t[+]{}\n\x1b[0m".format(r.json()[i]["Name"]))
			sys.stdout.write("\n")			
			sys.stdout.write("####################################################")
			sys.stdout.write("\n\n")
			write_to_file(resultat,r,i)
		sys.stdout.flush()
		sys.stdout.write("\x1b[1m\x1b[92m [+]saved to output.txt..\x1b[0m")
	else :
		sys.stdout.write("\x1b[91mno leaks found for {}. \n\n\x1b[0m".format(resultat))
		sys.stdout.flush()



file_choice,pattern_choice = banner()
threads = [] #multi ..threading? hhhhh?
match = file_open_and_extract(file_choice)
start = time.time()
for resultat in match:
	t = Thread(target=request_maker(resultat))
	t.start()
	threads.append(t)
	sys.stdout.write("\r")
	sys.stdout.flush()
	time.sleep(0.2)

for a in threads:
	a.join()
time_taken = time.time()-start
print("\n")
print("\x1b[96m[+]done in {} seconds.\x1b[0m".format(time_taken))
