#!/usr/bin/env python3

import os
import json
import emoji
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SLACK_URL = os.getenv('SLACK_URL')
PAGE_URL = os.getenv('PAGE_URL')
API_URL = os.getenv('API_URL')

def slack(msg):
	r = requests.post(SLACK_URL, json={'text': msg}, headers={'Content-Type': 'application/json'})

def printMsg(msg, slackMsg=False):
        print("[", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), "]", msg)
        if (slackMsg):
                slack(msg)

def createMsg(label, value):
	index = int(value)
	icon = ':red_square:' if (index < 34)  else ':orange_square:' if (index < 67) else ':green_square:'
	severity = 'Extreme Fear' if (index < 26) else 'Fear' if (index < 51) else 'Greed' if (index < 76) else 'Extreme Greed'
	return icon + ' ' + label + ': ' + severity + ' (' + value + ')\n'

headers = {'Host': 'alternative.me', 'User-Agent': 'PostmanRuntime/7.28.2', 'Connection': 'close'}

while True:
	page = requests.get(PAGE_URL, headers=headers)
	soup = BeautifulSoup(page.content, "html.parser")

	msg = ""

	for x in soup.find_all("div", {"class": "fng-value"}):
		label = x.find_all("div", {"class": "gray"})[0].text
		value = x.find_all("div", {"class": "fng-circle"})[0].text
		msg += createMsg(label, value)

	response = json.loads(requests.get(API_URL).content)
	ttl = int(response['data'][0]['time_until_update']) + 10

	printMsg(emoji.emojize(msg), True)
	time.sleep(ttl)
