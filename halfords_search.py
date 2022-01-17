import json
import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tabulate import tabulate
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
import time
import os
import re

# Loading secure credentials, should be replaced with preferred method of retreiving email address & password
load_dotenv()


def query_stock(product_number, address, max_results=10):
	if type(product_number) is not str:
		product_number = str(product_number)

	# Converting post code to longitude and latitude

	url = 'https://nominatim.openstreetmap.org/?addressdetails=1&q=' + address + '&format=json&limit=1'
	address_data = requests.get(url).json()
	if not address_data:
		print("Address not found")
		return None
	else:
		loc = address_data[0]

	# Building query url and parsing the json
	url = 'https://www.halfords.com/find-stores?lat={lat}&lng={lng}&pid={pid}&qty=1&size={max_results}'.format(
		lat=loc['lat'], lng=loc['lon'], pid=product_number, max_results=max_results)

	site = requests.get(url)
	text = site.content
	try:
		data = json.loads(text)
	except json.JSONDecodeError:
		print('PID "{pid}" didn\'t match any product'.format(pid=pid))
		return None

	# Stores listed in json
	stores = data['stores']

	# Initialising array of stock available in each store (first element is headers for a table later)
	available_stock = [[]] * (len(stores) + 1)
	available_stock[0] = ['Store', 'In Store Stock', 'Orderable Stock', 'Distance (km)', 'Post Code', 'Phone Number']

	# Looping over remaining elements and populating array with above headers
	stock_available = False

	for i, store in enumerate(stores, start=1):
		inventory = store['inventory']
		available_stock[i] = [store['name'], inventory['rcPids'][product_number]['stock'], inventory['pids'][product_number],
							store['distance'], store['postalCode'], store['phone']]

		if any([x > 0 for x in available_stock[i][1:3] if x is not None]):
			stock_available = True

	if not stock_available:
		return None
	else:
		return available_stock


def print_stock(stock_table):
	print(tabulate(stock_table, headers='firstrow', tablefmt='grid'))


def send_availability_email(nearby_stock, barcode):
	product_page = "https://www.halfords.com/{pid}.html".format(pid=barcode)
	# Getting credentials
	USER = os.getenv('USER')
	PASS = os.getenv('PASS')

	server = re.match('[\w]*[\W\S]([\w]*)', USER)[1]
	context = ssl.create_default_context()

	# Opening SMTP server to send email to self. It should adjust according to email address but haven't tested
	with smtplib.SMTP_SSL("smtp.{}.com".format(server), 465, context=context) as server:
		product_name, product_image = get_product_details(barcode)
		server.login(USER, PASS)
		plain_text = """
		Your product ({pid}) is available!

		Go order it now at: "{url}"

		{table}
		""".format(pid=barcode, table=tabulate(nearby_stock, headers='firstrow', tablefmt='grid'), url=product_page)

		html = """
		<html>
			<head>
				<style> 
					table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
					th, td {{ padding: 5px; }}

					a, a:link, a:visited a:hover {{color: black; text-decoration: none;}}

					p {{color:black;}}
				</style>
			</head>
			<body>
				<h1>{name}</h1>
				<a href="{url}">
					<div>
						<img src="{image}">
						<p>Your product ({pid}) is available! Click here to order.</p>
					</div>
				</a>
				{table}
			</body>
		</html>
		""".format(pid=barcode, table=tabulate(nearby_stock, headers='firstrow', tablefmt='html'), url=product_page,
					name=product_name, image=product_image)

		# Sending message

		message = MIMEMultipart('alternative', None, [MIMEText(plain_text), MIMEText(html, 'html')])
		message['Subject'] = 'Halfords Availability'
		message['From'] = USER
		message['To'] = USER

		server.sendmail(USER, USER, message.as_string())


def get_product_details(barcode):
	product_page = "https://www.halfords.com/{pid}.html".format(pid=barcode)
	r = requests.get(product_page)
	soup = bs(r.content, 'html.parser')
	scripts = soup.find_all('script', type="application/ld+json")
	script = [x for x in scripts if "description" in x.string][0].string
	script_json = json.loads(script)
	try:
		product_name = script_json['name']
	except KeyError:
		try:
			product_name = script_json['description']
		except KeyError:
			product_name = ''

	product_image = script_json['image']

	return product_name, product_image


def loop_until_available(barcode, address, refresh_time=60 * 5):
	while True:
		nearby_stock = query_stock(barcode, address)
		if nearby_stock is not None:
			send_availability_email(nearby_stock, barcode)
			break
		else:
			time.sleep(refresh_time)


if __name__ == '__main__':
	pid = '134078'
	bad_pid = '1'
	post_code = 'OX12 9AW'
	product_webpage = "https://www.halfords.com/{pid}.html".format(pid=pid)

	stock = query_stock(pid, post_code)
	#loop_until_available(pid, post_code)
