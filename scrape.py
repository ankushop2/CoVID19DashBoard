import requests
import re 
import os.path
from os import path
import bs4
from bs4 import BeautifulSoup
from datetime import datetime

def getContents():
	url = "https://www.mohfw.gov.in/"
	r = requests.get(url)	
	txt = ""
	if r.status_code == 200:
		txt = r.text
		return txt

def scrape_now():
	######## list declarations #######
	stats_list = []
	state_list = []
	confirmed_list = []
	cured_list = []
	death_list = []
	######## parse starts #######
	txt = getContents()
	soup = BeautifulSoup(txt, 'html.parser')
	###### get stats first ########
	stats = soup.find("div", {"class": "site-stats-count"})
	for length in stats.find_all("strong"):
		stats_list.append(length.getText())
	###### get states data #######
	states_data  = soup.find("section", {"id": "state-data"})
	tables = states_data.find_all('tbody')
	for row in tables[0].findAll("tr"):
		col = row.findAll("td")
		if((col[0].getText()).isnumeric()):
			state_list.append(col[1].getText())
			confirmed_list.append(int(col[2].getText()))
			cured_list.append(int(col[3].getText()))
			death_list.append(int(col[4].getText()))
	return stats_list, state_list, confirmed_list, cured_list, death_list
