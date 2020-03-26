import requests
import re 
import os.path
from os import path
import bs4
from bs4 import BeautifulSoup
from datetime import datetime

states = {}
states["Andhra Pradesh"]="AP"
states["Arunachal Pradesh"]="AR"
states["Assam"]="AS"
states["Bihar"]="BR"
states["Chattisgarh"]="CT"
states["Chhattisgarh"]="CT"
states["Goa"]="GA"
states["Gujarat"]="GJ"
states["Haryana"]="HR"
states["Himachal Pradesh"]="HP"
states["Jharkhand"]="JH"
states["Karnataka"]="KA"
states["Kerala"]="KL"
states["Madhya Pradesh"]="MP"
states["Maharashtra"]="MH"
states["Manipur"]="MN"
states["Meghalaya"]="ML"
states["Mizoram"]="MZ"
states["Nagaland"]="NL"
states["Odisha"]="OR"
states["Punjab"]="PB"
states["Rajasthan"]="RJ"
states["Sikkim"]="SK"
states["Tamil Nadu"]="TN"
states["Telengana"]="TG"
states["Tripura"]="TR"
states["Uttarakhand"]="UT"
states["Uttar Pradesh"]="UP"
states["West Bengal"]="WB"
states["Andaman and Nicobar Islands"]="AN"
states["Chandigarh"]="CH"
states["Dadra and Nagar Haveli"]="DN"
states["Daman and Diu"]="DD"
states["Delhi"]="DL"
states["Jammu and Kashmir"]="JK"
states["Ladakh"]="LA"
states["Lakshadweep"]="LD"
states["Pondicherry"]="PY"
states["Puducherry"]="PY"



def getContents():
	url = "https://www.mohfw.gov.in/"
	r = requests.get(url)	
	txt = ""
	if r.status_code == 200:
		txt = r.text
		return txt

def scrape_now():
	txt = getContents()
	actual_data = {}
	state_list=[]
	confirmed_data = []
	cured_data = []
	death_data = []
	confirmed_india = 0
	confirmed_foreign = 0
	confirmed_cured = 0
	confirmed_deaths = 0
	#get to parsing
	soup = BeautifulSoup(txt, 'html.parser')
	#cases = soup.find(id="cases")
	tables = soup.find_all("tbody")
	
	if len(tables) > 0:
		table = tables[7]
		#print(table)
		first_row = False
		for tr in list(table.children):
			if isinstance(tr, bs4.element.Tag): 
				if first_row:
					print("FIRST ROW")
					first_row = False
					continue

				tds = list(tr.children)

				if len(tds) > 1:
					pass
				else:
					continue
				#print(tds[11])

				if "Total number of confirmed cases in India" == tds[1].get_text():
					continue

				now = datetime.now()
				report_time = now.strftime("%d/%m/%Y %H:%M:%S")
				state = (tds[3]).get_text()
				state = state.replace("Union Territory of ","")
				state = state.strip()
				state_code = ""
				if state in states :
					state_code = (states[state]).lower()
				# else:
				# 	sendMessage("ERROR WRONG STATE",  "Not found: {0}".format(state))
				# 	print("------> Wrong state {0}".format(state))
				# 	return 0

				
				data = {}
				#data["state"] = state_code
				data["report_time"] = report_time
				confirmed_india = confirmed_india + int( (tds[5]).get_text() )
				data["confirmed_india"] =  int( (tds[5]).get_text() )
				confirmed_foreign = confirmed_foreign + int( (tds[7]).get_text() )
				data["confirmed_foreign"] = int( (tds[7]).get_text() )
				state_list.append(state)
				confirmed_data.append(data["confirmed_india"]+data["confirmed_foreign"])
				confirmed_cured = confirmed_cured + int( (tds[9]).get_text() )
				data["cured"] = int( (tds[9]).get_text() )
				cured_data.append(int( (tds[9]).get_text() ))
				#temp = re.findall(r'\d+', (tds[11]).get_text())[0]
				confirmed_deaths = confirmed_deaths + int((tds[11]).get_text())
				data["death"] = int( (tds[11]).get_text() )
				death_data.append(int( (tds[11]).get_text() ))
				actual_data[state] = data

		return state_list, confirmed_data, cured_data, death_data, actual_data, confirmed_india, confirmed_foreign, confirmed_cured, confirmed_deaths
		
		
	else:
		return "!!!!ERROR!!!!"

