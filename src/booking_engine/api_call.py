import urllib2, json, time
import urllib
import constants
import hashlib
from StringIO import StringIO
import gzip

def getPropertyURL(property_id):
	base_url = constants.GET_PROPERTY_API_URL + property_id
	url = base_url + '&api_key=' + constants.api_key
	post_params = None
	api_key = constants.api_key
	ts = str(int(time.time()))
	secure_hash = getSecureHash(url, post_params, api_key, ts)
	sender_url = base_url + '&sign=' + str(secure_hash) + '&timestamp=' + ts

	request = urllib2.Request(sender_url)
	request.add_header('Accept-encoding', 'gzip')
	response = urllib2.urlopen(request)
	if response.info().get('Content-Encoding') == 'gzip':
	    buf = StringIO(response.read())
	    f = gzip.GzipFile(fileobj=buf)
	    response_api_val = f.read()

	response_api = json.loads(response_api_val)
	if(response_api and response_api['status'] != 'null' and response_api['status'] != '0'):
		result["status"] = 1
		result["povp_url"] = response_api["apartmentMain"]["promotional_url"]
		result_json = result
	else:
		result_json = {'status':0}

	return result_json

def getAPIProperty(property_id):
	base_url = constants.GET_PROPERTY_API_URL + property_id
	url = base_url + '&api_key=' + constants.api_key
	post_params = None
	api_key = constants.api_key
	ts = str(int(time.time()))
	secure_hash = getSecureHash(url, post_params, api_key, ts)
	sender_url = base_url + '&sign=' + str(secure_hash) + '&timestamp=' + ts

	request = urllib2.Request(sender_url)
	request.add_header('Accept-encoding', 'gzip')
	response = urllib2.urlopen(request)
	if response.info().get('Content-Encoding') == 'gzip':
	    buf = StringIO(response.read())
	    f = gzip.GzipFile(fileobj=buf)
	    response_api_val = f.read()

	response_api = json.loads(response_api_val)
	#print response_api
	if(response_api and response_api['status'] != 'null' and response_api['status'] != '0'):
		result = {'property_name': response_api["apartmentMain"]["name"], 'has_image':response_api["apartmentMain"]["has_image"],'property_Area':response_api["apartmentMain"]["area"],'total_sqft':response_api["apartmentMain"]["total_sqft"],'property_status':response_api["apartmentMain"]["property_status"],'property_type':response_api["apartmentMain"]["property_type"],'launch_date':response_api["apartmentMain"]["launch_date"],'address':response_api["apartmentMain"]["address"],'launch_units':response_api["apartmentMain"]["launch_units"]}
		property_images = response_api["apartmentPublicImages"]
		for property_image in property_images:
			if property_image["caption"] == "Main Image":
				result["property_image"] = property_image["url_full_image"].replace("ak.is3","is1")

		result["property_thumb_image"] = response_api["apartmentMain"]["apt_image"]
		aprt_plans = {}
		for plan in response_api["apartmentPlan"]:
			no_bedrooms = str(plan['num_of_bedrooms'])
			plan_image = str(plan['plan_image_url'])
			#print no_bedrooms
			if plan['num_of_bedrooms'] is not None:
				if(no_bedrooms in aprt_plans):
					aprt_plans[no_bedrooms].append(plan_image)
				else:
					aprt_plans[no_bedrooms] = [plan_image]
					aprt_plans["thumb_image"+no_bedrooms] = "http://is1.cfcdn.com/is/p/t20/260x200" + plan_image

		#print aprt_plans

		apartmentHouseDetails = response_api["apartmentHouseDetails"]
		aprt_house_detail = []
		for apartmentHouseDetail in apartmentHouseDetails:
			apartment_House_Detail = {}
			apartment_House_Detail['num_of_bedrooms'] = str(apartmentHouseDetail['num_of_bedrooms'])
			
			apartment_House_Detail['approx_area'] = ''
			if(apartmentHouseDetail['approx_area'] is not None):
				for approx_area in json.loads(apartmentHouseDetail['approx_area']):
					apartment_House_Detail['approx_area'] += str(approx_area)+' sqft, '
				apartment_House_Detail['approx_area'] = apartment_House_Detail['approx_area'][:-2]

			apartment_House_Detail['approx_price_sale'] = ''
			if(apartmentHouseDetail['approx_price_sale'] is not None):
				for approx_price_sale in json.loads(apartmentHouseDetail['approx_price_sale']):
					apartment_House_Detail['approx_price_sale'] += str(approx_price_sale)+'-'
				apartment_House_Detail['approx_price_sale'] = apartment_House_Detail['approx_price_sale'][:-1]

			#apartment_House_Detail['approx_price_sale'] = json.loads(apartmentHouseDetail['approx_price_sale'])
			if apartmentHouseDetail['num_of_bedrooms'] is not None:
				if(apartment_House_Detail['num_of_bedrooms'] in aprt_plans):
					#print "thumb_image"+apartment_House_Detail['num_of_bedrooms']
					apartment_House_Detail['thumb_image'] = aprt_plans["thumb_image"+apartment_House_Detail['num_of_bedrooms']]
					apartment_House_Detail['images'] = aprt_plans[apartment_House_Detail['num_of_bedrooms']]
			aprt_house_detail.append(apartment_House_Detail)

		result["apartmentHouseDetails"] = aprt_house_detail
		result["apartmentPlan"] = aprt_plans
		result["apartmentAmenities"] = response_api["apartmentAmenities"]
		result["builder_name"] = response_api["apartmentPropertyInfo"]["builder"]
		result["povp_url"] = response_api["apartmentMain"]["promotional_url"]
		property_type = response_api["apartmentMain"]["property_type"]
		if(property_type == 'apartments'):
			result["property_type"] = "Apartment"
		elif(property_type == 'villas_and_row_houses'):
			result["property_type"] = "Villa And Row House"
		elif(property_type == 'layouts_and_plots'):
			result["property_type"] = "Layouts And Plots"
		else:
			result["property_type"] = property_type
		result["city"] = response_api["apartmentMain"]["city"]

		result_json = result
	else:
		result_json = {'status':0}

	return result_json

def getAPICities():
	base_url = constants.GET_CITIES_API_URL
	url = base_url + '?api_key=' + constants.api_key
	post_params = None
	api_key = constants.api_key
	ts = str(int(time.time()))
	secure_hash = getSecureHash(url, post_params, api_key, ts)

	sender_url = base_url + '?sign=' + str(secure_hash) + '&timestamp=' + ts
	#print 'secure_url --------> ',sender_url
	#response_api_val = urllib2.urlopen(sender_url).read()


	request = urllib2.Request(sender_url)
	request.add_header('Accept-encoding', 'gzip')
	response = urllib2.urlopen(request)
	if response.info().get('Content-Encoding') == 'gzip':
	    buf = StringIO(response.read())
	    f = gzip.GzipFile(fileobj=buf)
	    response_api_val = f.read()

	result_json = json.loads(response_api_val)
	if not (result_json and result_json['status'] != 'null' and result_json['status'] != '0'):
		result_json = {'status':0}

	return result_json


def getAPIAreaByCity(city,area_str):
	print "inside getAPIAreaByCity"

	base_url = constants.GET_AREA_BY_CITY_API_URL + city +'&str='+area_str
	url = base_url + '&api_key=' + constants.api_key
	post_params = None
	api_key = constants.api_key
	ts = str(int(time.time()))
	secure_hash = getSecureHash(url, post_params, api_key, ts)
	sender_url = base_url + '&sign=' + str(secure_hash) + '&timestamp=' + ts

	print 'sender_url', sender_url
	request = urllib2.Request(sender_url)
	request.add_header('Accept-encoding', 'gzip')
	response = urllib2.urlopen(request)
	if response.info().get('Content-Encoding') == 'gzip':
	    buf = StringIO(response.read())
	    f = gzip.GzipFile(fileobj=buf)
	    response_api_val = f.read()

	response_api_val = urllib2.urlopen(sender_url).read()
	result_json = json.loads(response_api_val)
	#print 'result_json', result_json
	if(result_json):
		area_array = result_json
		result_name = {}
		for area_entry in area_array:
			if('~' in area_entry):
				area_name = area_entry.split('~')[0]
				zone_name = area_entry.split('|')[-1:]
				if(area_str.lower() in area_name.lower()):
					result_name[area_name] = zone_name
		return result_name
	else:
		result_json = {}

	return result_json

def getUnitInfo(unit_id):
	print "in get Unit Info call"
	authKey = constants.UNITSELECTOR_AUTHKEY
	unitSummary = constants.UNIT_SUMMARY_URL

	sender_url = unitSummary + unit_id
	request = urllib2.Request(sender_url)
	request.add_header('X-Authorization', authKey)
	try:
		response = urllib2.urlopen(request)
		response_json = json.load(response)
	except urllib2.URLError as e:
		print 'getUnitInfo Error => ' +e.reason 
		result = {}
		result['error']=True
		result['error_message']= 'getUnitInfo Error => ' + e.reason
		return result

	return response_json

def updateUnitInfoStatus(unit_id, unit_status):
	print "update unit info call"
	authKey = constants.UNITSELECTOR_AUTHKEY
	unitSummary = constants.UNIT_SUMMARY_URL

	sender_url = unitSummary + unit_id
	post_data = {'status':unit_status}
	request = urllib2.Request(sender_url)
	request.add_header('X-Authorization', authKey)

	try:
		response = urllib2.urlopen(request, urllib.urlencode(post_data))
		response_json = json.load(response)
	except urllib2.URLError as e:
		print 'updateUnitInfoStatus Error => ' +e.reason 
		result = {}
		result['error']=True
		result['error_message']= 'updateUnitInfoStatus Error => ' + e.reason
		return result

	return response_json

def getAPIPropertyByArea(city,area_zone):
	print "inside getAPIPropertiesByArea"

	base_url = constants.GET_PROPERTIES_BY_AREA_API_URL+area_zone +'&city='+ city
	url = base_url + '&api_key=' + constants.api_key
	post_params = None
	api_key = constants.api_key
	ts = str(int(time.time()))
	secure_hash = getSecureHash(url, post_params, api_key, ts)
	sender_url = base_url + '&sign=' + str(secure_hash) + '&timestamp=' + ts

	print 'sender_url', sender_url
	
	request = urllib2.Request(sender_url)
	request.add_header('Accept-encoding', 'gzip')
	response = urllib2.urlopen(request)
	if response.info().get('Content-Encoding') == 'gzip':
	    buf = StringIO(response.read())
	    f = gzip.GzipFile(fileobj=buf)
	    response_api_val = f.read()

	#response_api_val = urllib2.urlopen(sender_url).read()
	result_json = json.loads(response_api_val)
	result = []
	if(result_json and result_json['status'] != 'null' and result_json['status'] != '0'):
		total_page = int(result_json['results']['total_page'])
		# print "***************",total_page
		# total_projects = int(result_json['results']['total_projects'])
		# print "***************",total_projects
		projects = result_json['results']['projects']
		for project in projects:
			project_info = {}
			project_info['property_id'] = project['property_id']
			project_info['name'] = project['name']
			project_info['builder_name'] = project['builder_name']
			project_info['project_type'] = project['project_type']
			result.append(project_info)
			#print project_info

		#print result_json

		if(total_page > 1):
			index = 2
			while (index<=total_page):
				base_url = constants.GET_PROPERTIES_BY_AREA_API_URL+area_zone + '&page=' + str(index) +'&city='+ city
				url = base_url + '&api_key=' + constants.api_key
				post_params = None
				api_key = constants.api_key
				ts = str(int(time.time()))
				secure_hash = getSecureHash(url, post_params, api_key, ts)
				sender_url = base_url + '&sign=' + str(secure_hash) + '&timestamp=' + ts
				request = urllib2.Request(sender_url)
				request.add_header('Accept-encoding', 'gzip')
				response = urllib2.urlopen(request)
				if response.info().get('Content-Encoding') == 'gzip':
				    buf = StringIO(response.read())
				    f = gzip.GzipFile(fileobj=buf)
				    response_api_val = f.read()
				#response_api_val = urllib2.urlopen(sender_url).read()
				result_json = json.loads(response_api_val)

				projects = result_json['results']['projects']
				for project in projects:
					project_info = {}
					project_info['property_id'] = project['property_id']
					project_info['name'] = project['name']
					project_info['builder_name'] = project['builder_name']
					project_info['project_type'] = project['project_type']
					# if(project_info in result):
					# 	print project_info
					result.append(project_info)

				index += 1
	else:
		result = []

	return result

def getSecureHash(url,post_params,api_key, ts):
	if post_params is not None:
		url = url + "&"+post_params

   	split_url = url.split('?')
   	base_url = split_url[0];

   	params=[]
   	if len(split_url) > 1:
   		params=split_url[1].split("&")
   	#print 'params',params
   	query_map={}
   	if len(params) > 0:
   		for param in params:
   			param_split=param.split('=')
   			query_map.update({param_split[0]:param_split[1]})

		# add time stamp if any param exists
		query_map.update({'timestamp':ts})

	keys = query_map.keys()
	keys.sort()
	new_url = '?'
	if('api_key' in keys):
		keys.remove('api_key') # remove the key such that we can add the api key later on manually
	for key in keys:
	   new_url += urllib.urlencode({key:query_map.get(key)})+'&'
	print 'new_url', new_url
	new_url_with_key = new_url + 'api_key='+api_key
	md5_seed_url= base_url + new_url_with_key
	md5_hash = hashlib.md5(md5_seed_url).hexdigest()
	print 'md5_seed_url',md5_seed_url

	return md5_hash