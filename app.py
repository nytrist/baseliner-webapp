from flask import Flask, render_template, url_for, request
import requests, json


# site URLS
api_base_url = "http://japan-api.soil.watch"
webapp_base_url = "http://japan.soil.watch"
title = "Baseliner"
deploy_site = "Japan Sandbox"

# set navigation URLs
nav_urls = {
	#set top nav URLs
	"freaklabsjpn_url" : webapp_base_url + "/freaklabsjpn",
	"freaklabsau_url" : webapp_base_url + "/freaklabsau",
	"monash_url" : webapp_base_url + "/monash",
	"nardoo_url" : webapp_base_url + "/nardoo",
	"roundhouse_url" : webapp_base_url + "/roundhouse",
	"photos_url" : webapp_base_url + "/gallery",
	"about_url" : webapp_base_url + "/about",
	"team_url" : webapp_base_url + "/team",
	"contact_url" : webapp_base_url + "/contact",

	#set main nav URLS
	"gateways_url" : webapp_base_url + "/",
	"readings_url" : webapp_base_url + "/readings",
	"stations_url" : webapp_base_url + "/stations",
	"add_url" : webapp_base_url + "/add",
	"mod_url" : webapp_base_url + "/modify",
	"delete_url" : webapp_base_url + "/delete",
	"download_url" : webapp_base_url + "/download",
}

app  = Flask(__name__)


#GET Requests
@app.route('/') # active gateways
def home():
	api_url = api_base_url + "/"
	response = requests.get(api_url)
	gateways = json.loads(response.text)
	#print(json.dumps(data, indent=4))
	return render_template(
	'index.html',
	api_url=api_url,
	title=title,
	deploy_site=deploy_site,
	nav_urls=nav_urls,
	gateways=gateways
	)

#Readings
@app.route('/readings') #last 20 full readings from all gateways
def get_readings():
	api_url = api_base_url + "/readings"
	response = requests.get(api_url)
	readings = json.loads(response.text)
	#print(json.dumps(readings, indent=4))
	return render_template('readings.html',
	api_url=api_url,
	title=title,
	deploy_site=deploy_site,
	nav_urls=nav_urls,
	readings=readings)

#last 20 complete results for individual gateway
@app.route('/gateway/<gw_id>/readings')
def get_readings_gw_all(gw_id):
	api_url = api_base_url + "/gateway/" + gw_id +"/readings"
	response = requests.get(api_url)
	readings = json.loads(response.text)
	return render_template(
	'readings_gw_full.html',
	api_url=api_url,
	title=title,
	deploy_site=deploy_site,
	nav_urls=nav_urls,
	gw_id=gw_id,
	readings=readings)

#all readings, gw data only, for individual gateway
@app.route('/gateway/<gw_id>')
def get_readings_gw(gw_id):
	api_url = api_base_url + "/gateway/" + gw_id
	response = requests.get(api_url)
	gateway_data = json.loads(response.text)
	return render_template(
	'gateway.html',
	api_url=api_url,
	title=title,
	deploy_site=deploy_site,
	nav_urls=nav_urls,
	gw_id=gw_id,
	gateway_data=gateway_data)

 # active stations
@app.route('/stations')
def stations():
	api_url = api_base_url + "/stations"
	response = requests.get(api_url)
	stations = json.loads(response.text)
	#print(json.dumps(data, indent=4))
	return render_template(
	'stations.html',
	api_url=api_url,
	nav_urls=nav_urls,
	deploy_site=deploy_site,
	title=title,
	stations=stations
	)

#individual station, station data only, all readings
@app.route('/station/<ss_id>')
def get_readings_ss(ss_id):
	api_url = api_base_url + "/station/" + ss_id
	response = requests.get(api_url)
	station_data = json.loads(response.text)
	#print(json.dumps(station_data, indent=4))
	return render_template(
	'station.html',
	api_url=api_url,
	title=title,
	deploy_site=deploy_site,
	nav_urls=nav_urls,
	ss_id=ss_id,
	station_data=station_data)

# individual station last 20 complete readings
@app.route('/station/<ss_id>/readings')
def get_readings_ss_all(ss_id):
	api_url = api_base_url + "/station/" + ss_id +"/readings"
	response = requests.get(api_url)
	readings = json.loads(response.text)
	#print(json.dumps(readings, indent=4))
	return render_template(
	'readings_ss_full.html',
	api_url=api_url,
	title=title,
	deploy_site=deploy_site,
	nav_urls=nav_urls,
	ss_id=ss_id,
	readings=readings)

#POST
@app.route('/add', methods=["GET", "POST"]) #add gateway / add or update node
def add():
	api_url = api_base_url
	message = "*All fields required."
	if request.method == "POST":
		data = request.form

		if data["form"] == "addGateway":
			api_url = api_base_url + "/gateway"

		elif data["form"] == "addStation":
			api_url = api_base_url + "/station"

		new_device = dict(data)
		new_device.pop('form')
		response = requests.post(api_url, data=new_device)
		message = json.loads(response.text)
		message=message["message"]

	return render_template(
	'add.html',
	api_url=api_url,
	title=title,
	deploy_site=deploy_site,
	nav_urls=nav_urls,
	message=message)

@app.route('/modify', methods=["GET", "POST"]) #delete gateway
def patch():
	api_url = api_base_url
	message = "*Device id is required."
	if request.method == "POST":
		data = request.form

		if data["form"] == "modifyGateway":
			api_url = api_base_url + "/gateway"

		elif data["form"] == "modifyStation":
			api_url = api_base_url + "/station"

		mod_device = dict(data)

		# remove form key, value
		mod_device.pop('form')

		#remove keys with no values
		mod_device = {k:v for k,v in mod_device.items() if v != ""}

		response = requests.patch(api_url, data=mod_device)
		message = json.loads(response.text)
		message=message["message"]

	return render_template(
	'modify.html',
	api_url=api_url,
	title=title,
	deploy_site=deploy_site,
	nav_urls=nav_urls,
	message=message)



@app.route('/delete', methods=["GET", "POST"]) #delete gateway
def delete():
	api_url = api_base_url
	message = "Please enter device id."
	if request.method == "POST":
		data = request.form

		if data["form"] == "deleteGateway":
			api_url = api_base_url + "/gateway"

		elif data["form"] == "deleteStation":
			api_url = api_base_url + "/station"

		del_device = dict(data)
		del_device.pop('form')
		response = requests.delete(api_url, data=del_device)
		message = json.loads(response.text)
		message=message["message"]

	return render_template(
	'delete.html',
	api_url=api_url,
	title=title,
	deploy_site=deploy_site,
	nav_urls=nav_urls,
	message=message)


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
