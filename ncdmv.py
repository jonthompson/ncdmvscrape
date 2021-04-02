#!/usr/bin/python3

import requests
import datetime
import time

startdaysout = 7 
checkdays = 14


locations = {"Carrboro": "140",
		"Cary": "66",
		"Durham South": "80",
		"Hillsborough": "52",
		"Siler City": "109",
		"Sanford": "54"
		}


headers = {
    'Connection': 'close',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.40 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,la;q=0.7',
}

s = requests.Session()
s.keep_alive = False

# Load the main page incase we need to to trigger any application logic

s.get("https://skiptheline.ncdot.gov/Webapp/_/_/_/en/WizardAppt/AppointmentTypes", headers=headers)

# Set your appointment type
s.post("https://skiptheline.ncdot.gov/Webapp/_/_/_/en/WizardAppt/SelectAppointmentType", headers=headers, data={"apptType": "Teen Driver Level 1"})

for location in locations:

	# Set the location via a post
	print("Setting location to %s" %location)
	s.post('https://skiptheline.ncdot.gov/Webapp/_/_/_/en/WizardAppt/SelectedUnit', headers=headers, data={'unitId': locations[location]})


	# Iterate through days to check for appointments
	for day in range(checkdays):

		date = datetime.date.today()+datetime.timedelta(days=startdaysout) + datetime.timedelta(days=day)

		#Skip weekends
		if date.weekday() in (5,6):
			continue

		# Don't flood them
		time.sleep(1)

		url = "%s?date=%s&_=%s" %("https://skiptheline.ncdot.gov/Webapp/_/_/_/en/WizardAppt/SlotsTime", date.strftime("%m/%d/%Y"), int(time.time()))
		
		print("Fetching", url)

		# dont bother retrying just fail and continue
		try:
			r = s.get(url, headers=headers).json()
			if "Result" in r and r["Result"]: 
				print("DMV APPOINTMENT FOUND: %s @ %s https://skiptheline.ncdot.gov/Webapp/_/_/_/en/WizardAppt/Units?input=Appointment" %(date,location), r)
		except:
			print("Error, skipping")
			continue
