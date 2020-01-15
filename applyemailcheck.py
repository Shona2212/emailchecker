import re
import requests
import lxml
from lxml import html
import pandas as pd
import unicodecsv as csv
import re, time

df1 = pd.read_csv("to_check.csv")
#print df1
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#headers={'User-Agent':'Mozilla/5'}
file_handler=open("email_Jan_2020_clients.csv", "wb")
writer_obj=csv.writer(file_handler)
writer_obj.writerow(['Company_Id','jobUrl','Response_Code','applyOnEmailId'])
temp_email = []

df = df1.head(5)

print df

for a, b in df1.iterrows():
	comp_id = b['compId']
	new = b['jobUrl']
	print ("###############################################")
	print "Company_Id : "+str(comp_id)+"\nJob URL : "+str(new)
	temp_email.append(comp_id)
	temp_email.append(new)

	try:
		resp = requests.get(new, headers= headers, timeout = 15)
		r_code = resp.status_code
		print "Response_Code : "+str(r_code)
		temp_email.append(r_code)

		if (r_code==200):

			print "Site Opening"
			data = resp.content
		#print data
			#print ("************")
			m = re.search (r'mailto:([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})', data)
			#print m
			#print ("************")
			if m:
				email_id = m.group()
				print "Email Id : "+str(email_id)
				temp_email.append(email_id)

				print temp_email

				writer_obj.writerow(temp_email)

				temp_email = []
			else:
				email_id = "No_Email_Found"
				print "Email Id : "+str(email_id)

				temp_email.append(email_id)
				print temp_email

				writer_obj.writerow(temp_email)

				temp_email = []

			print ("*************")

		else:

			print "Site Not Discoverable"

			print temp_email
			writer_obj.writerow(temp_email)

			temp_email = []
			continue


	except Exception as e:

		print e

		temp_email.append("Site Not Discoverable")

		temp_email.append(e)

		print temp_email
		writer_obj.writerow(temp_email)

		temp_email = []
		continue

#writer_obj.writerow(temp_email)
