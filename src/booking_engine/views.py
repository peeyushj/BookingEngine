from django.shortcuts import render ,render_to_response, RequestContext, redirect

from django.contrib import messages

from models import *
from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required

from manage_db import execute_query
import server_setting.settings
import string, random, json
import traceback

import sched, time, threading
import user_emails
import logging
import hashlib
import urllib, urllib2
from StringIO import StringIO
import gzip
import api_call, constants
from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError

scheduler = sched.scheduler(time.time, time.sleep)
#logger = logging.getLogger('booking_crm')

# Create your views here.

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

def homepage(request):
	return render_to_response("dashboard.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
@csrf_exempt
def account_info(request):
	user_info = request.user
	try:
		user_detail = booking_engine_users.objects.get(user_id=user_info.id)
		request.session['user_role'] = user_detail.role
	except booking_engine_users.DoesNotExist:
		user_detail = None

	try:
		if user_detail:
			if request.method == 'POST':
				if 'save_user_name' in request.POST:
					user=User.objects.get(id=user_info.id)
					user.first_name = request.POST['first_name']
					user.last_name = request.POST['last_name']
					user.save()
					messages.add_message(request, messages.SUCCESS, 'You have successfully changed the user name.')
				if 'change_password' in request.POST:
					user=User.objects.get(id=user_info.id)
					old_password = request.POST['old_password']
					new_password = request.POST['new_password']
					valid = user.check_password(old_password)
					if(valid):
						if(old_password==new_password):
							messages.add_message(request, messages.ERROR, 'Both the password provided by you is same.')
						else:
							user.set_password(new_password)
							user.save()
							messages.add_message(request, messages.SUCCESS, 'You have successfully changed the password')
					else:
						messages.add_message(request, messages.ERROR, 'Please provide the correct password')
	except Exception as e:
		print "Exception => ", e.message

	return render_to_response("account_info.html", 
									locals(), 
									context_instance = RequestContext(request))

def access_error(request):
	try:
		# if('next' in request.GET):
		# 	request.session['next_url'] = request.GET['next']
		# if request.user.is_authenticated():
		# 	if('next_url' in request.session):
		# 		return redirect(request.session['next_url'])
		return render_to_response("access-error.html", 
									locals(), 
									context_instance = RequestContext(request))
	except Exception as e:
		logger.critical('%s %s (%s)' % ('Access Page Error:--',e.message, type(e)))
		print '%s %s (%s)' % ('Access Page Error',e.message, type(e))
		return redirect("/error")

@login_required
def add_project(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	cities = get_cities()
	booking_engine_added_projects = booking_engine_projects.objects.all()

	if request.method == 'POST':
		print "in add project"
		if 'booking_engine_added_project_delete' in request.POST:
			project = booking_engine_projects.objects.get(id=request.POST['booking_engine_added_project_id'])
			project.delete()
		if 'booking_engine_added_project_add' in request.POST:
			if not 'project_id' in request.POST:
				messages.add_message(request, messages.ERROR, 'Some problem in adding a project')
			else:
				projects = booking_engine_projects.objects.filter(project_id=request.POST['project_id'])
				if not projects:
					booking_engine_project = booking_engine_projects()
					booking_engine_project.project_id = request.POST['project_id']
					booking_engine_project.project_name = request.POST['project_name']
					booking_engine_project.project_area = request.POST['area']
					booking_engine_project.project_city = request.POST['city']
					booking_engine_project.project_type = request.POST['project_type']
					booking_engine_project.builder_name = request.POST['builder_name']
					booking_engine_project.save()

					messages.add_message(request, messages.SUCCESS, 'You have successfully added a project: ' + request.POST['project_name'])
				else:
					messages.add_message(request, messages.ERROR, 'This project \''+ request.POST['project_name'] +'\' already exists')


	return render_to_response("add_project.html", 
									locals(), 
									context_instance = RequestContext(request))

# @csrf_exempt
# def login(request):
# 	print "here"
# 	if request.method == 'POST':
# 		if not request.user:
# 			messages.add_message(request, messages.ERROR, 'Some problem in user authentication')
# 	return render_to_response("login.html", 
# 									locals(), 
# 									context_instance = RequestContext(request))

# @expose_service(['POST'], public=True)
# def test(request):
#     service_url = generate_service_url('/login')
#     return invoke_backend_service_as_proxy(request, 'POST', service_url, json_data={ 'email': 'admin@test.com', 'password': 'password' })

@login_required
def users(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin'):
		return redirect("/access_error")
	users = booking_engine_users.objects.all()
	return render_to_response("users.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
def payments(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Booking Team'):
		return redirect("/access_error")
	try:
		# if request.method == 'POST':
		# 	print 'payment_id', request.POST['payment_id']

		#payments = booking_engine_payment_history.objects.all().group_by("payment_id").order_by("-updated_on")
		payments = execute_query("SELECT booking_id, payment_id, is_active, updated_on, GROUP_CONCAT(DISTINCT payment_status SEPARATOR ' => ') as payment_status FROM booking_engine_payment_history GROUP BY booking_id, payment_id, is_active order by updated_on DESC", "default")
		#booking_engine_payment_history.objects.all().order_by('booking_id', '-updated_on')
	except Exception as e:
		print '%s %s (%s)' % ('Payments Page Error',e.message, type(e))
	return render_to_response("payments.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
@csrf_exempt
def unit_project_payment_plan(request):
	result = {}
	try:
		unit_id = request.POST['unit_id']
	except Exception as e:
		print '%s %s (%s)' % ('Unit Payment Plan Error',e.message, type(e))
		result['error']=True
		result['error_message']='Unit Id is not provided.'
		data = json.dumps(result)
		return HttpResponse(data)

	try:
		payment_plan_id = request.POST['payment_plan_id']
	except Exception as e:
		print '%s %s (%s)' % ('Unit Payment Plan Error',e.message, type(e))
		result['error']=True
		result['error_message']='Payment Plan Id is not stored in the database.'
		data = json.dumps(result)
		return HttpResponse(data)

	try:
		payment_plan_milestones = booking_engine_payment_plan_milestones.objects.filter(payment_plan_id=payment_plan_id)
		milestones = {}

		price_sheet_id = request.POST['price_sheet_id']
		total_sale_value = calc_total_sale_value(unit_id, False, price_sheet_id)

		current_total_value = 0.0
		is_free_text_available = False

		for payment_plan_milestone in payment_plan_milestones:
			milestone = {}
			milestone['milestone'] = payment_plan_milestone.milestone
			milestone['milestone_date'] = str(payment_plan_milestone.milestone_date)
			milestone['cost_type'] = payment_plan_milestone.cost_type
			milestone['entered_value'] = payment_plan_milestone.amount
			if 'Lumpsump' in payment_plan_milestone.cost_type:
				milestone['amount'] = payment_plan_milestone.amount
				current_total_value = current_total_value + float(milestone['amount'])
			elif 'Remaining Percentage' in payment_plan_milestone.cost_type:
				milestone['amount'] = float(int(total_sale_value)*int(payment_plan_milestone.amount)/100) - current_total_value
				current_total_value = current_total_value + float(milestone['amount'])
			elif 'Percentage' in payment_plan_milestone.cost_type:
				milestone['amount'] = int(total_sale_value)*int(payment_plan_milestone.amount)/100
				current_total_value = current_total_value + float(milestone['amount'])
			else:
				milestone['amount'] = payment_plan_milestone.amount
				is_free_text_available = True

			milestones[payment_plan_milestone.payment_plan_milestone_id] = milestone

		result['milestones'] = milestones
		if(is_free_text_available):
			result['total_sale_value'] = '--NA--'
		else:
			result['total_sale_value'] = total_sale_value

		data = json.dumps(result)
		return HttpResponse(data)

	except Exception as e:
		print '%s %s (%s)' % ('Unit Payment Plan Error => ',e.message, type(e))
		traceback.print_exc()
		result['error']=True
		result['error_message']='Unit Payment Plan Error => ' + e.message
		data = json.dumps(result)
		return HttpResponse(data)

@login_required
@csrf_exempt
def unit_project_price_sheet(request):
	print "inside unit_project_price_sheet"
	result = {}
	try:
		unit_id = request.POST['unit_id']
	except Exception as e:
		print '%s %s (%s)' % ('Unit Price Sheet Error',e.message, type(e))
		result['error']=True
		result['error_message']='Unit Id is not provided.'
		data  = json.dumps(result)
		return HttpResponse(data)

	try:
		price_sheet_id = request.POST['price_sheet_id']
	except Exception as e:
		print '%s %s (%s)' % ('Unit Price Sheet Error',e.message, type(e))
		result['error']=True
		result['error_message']='Price Sheet Id is not provided.'
		data = json.dumps(result)
		return HttpResponse(data)

	try:
		try:
			unit_extra_info = getUnitData(str(unit_id))
		except Exception as e:
			unit_extra_info = None
			print "inside except => ", e.message
		price_sheet_components = booking_engine_pricesheet_component.objects.filter(pricesheet_id=price_sheet_id)
		components = {}
		
		total_sale_value = calc_total_sale_value(unit_id, False, price_sheet_id)


		for price_sheet_component in price_sheet_components:
			component = {}
			component['component_price_type'] = price_sheet_component.price_type
			component['component_price_sub_type'] = price_sheet_component.price_sub_type
			component['cost_type'] = price_sheet_component.cost_type
			component['entered_value'] = str(price_sheet_component.amount)
			if 'Lumpsump' in price_sheet_component.cost_type:
				component['amount'] = price_sheet_component.amount
			elif 'Per sqft' in price_sheet_component.cost_type:
				calculated_sqft = 0
				if 'Basic' in price_sheet_component.price_type:
					if 'Super Builtup Area' in price_sheet_component.price_sub_type:
						calculated_sqft = int(unit_extra_info['data']['unit']['super_built_up_area'])
					elif 'Builtup Area' in price_sheet_component.price_sub_type:
						calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
					elif 'Carpet Area' in price_sheet_component.price_sub_type:
						calculated_sqft = int(unit_extra_info['data']['unit']['carpet_area'])
					else:
						calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
					component['amount'] = calculated_sqft*int(price_sheet_component.amount)
				elif 'PLC-Floorrise' in price_sheet_component.price_type:
					calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
					floor_number = unit_extra_info['data']['unit']['floor_number']
					if 'Fix Increasing Cost' in price_sheet_component.price_sub_type:
						component['amount'] = calculated_sqft*int(price_sheet_component.amount)*int(floor_number)
					elif 'Fix Decreasing Cost' in price_sheet_component.price_sub_type:
						component['amount'] = -(calculated_sqft*int(price_sheet_component.amount)*int(floor_number))
					elif price_sheet_component.price_sub_type==floor_number:
						component['amount'] = calculated_sqft*int(price_sheet_component.amount)
					else:
						component['amount'] = 0
				else:
					calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
					component['amount'] = calculated_sqft*int(price_sheet_component.amount)
			elif 'Percentage' in price_sheet_component.cost_type:
				component['amount'] = int(total_sale_value)*int(price_sheet_component.amount)/100
			#total_price += float(component['amount'])
			component['amount'] = str(component['amount'])

			components[price_sheet_component.pricesheet_component_id] = component
			
		result['components'] = components
		#result['extra_components'] = extra_components
		#result['total_price'] = total_price
		result['total_sale_value'] = total_sale_value

		data  = json.dumps(result)
		return HttpResponse(data)
	except Exception as e:
		print '%s %s (%s)' % ('Unit Price Sheet Error',e.message, type(e))
		result['error']=True
		result['error_message']=e.message
		data  = json.dumps(result)
		return HttpResponse(data)

@token_required
def unit_price_sheet(request):
	print "inside unit_price_sheet"
	result = {}
	try:
		unit_id = request.POST['unit_id']
	except Exception as e:
		print '%s %s (%s)' % ('Unit Price Sheet Error',e.message, type(e))
		result['error']=True
		result['error_message']='Unit Id is not provided.'
		data  = json.dumps(result)
		return HttpResponse(data)

	print "unit_id => ", unit_id
	is_unit_process = True
	try:
		unit_info = booking_engine_units.objects.get(unit_id=unit_id)
		price_sheet_id = unit_info.price_sheet_id
	except booking_engine_units.DoesNotExist:
		result['error']=True
		result['error_message']='Unit Information is not stored in database.'
		is_unit_process = False
		unit_info = None
		data  = json.dumps(result)
		return HttpResponse(data)

	try:
		print "is_unit_process => ", str(is_unit_process)
		if not is_unit_process:
			project_id = request.POST['project_id']
			pricesheet_info = booking_engine_pricesheet.objects.get(project_id=project_id, is_default=True)
			price_sheet_id = pricesheet_info.pricesheet_id
	except booking_engine_pricesheet.DoesNotExist:
		result['error']=True
		result['error_message']='No Unit Price Sheet Found.'
		data  = json.dumps(result)
		return HttpResponse(data)

	try:
		try:
			unit_extra_info = getUnitData(str(unit_id))
		except Exception as e:
			unit_extra_info = None
			print "inside except => ", e.message
		price_sheet_components = booking_engine_pricesheet_component.objects.filter(pricesheet_id=price_sheet_id)
		components = {}
		
		total_sale_value = calc_total_sale_value(unit_id, False)


		for price_sheet_component in price_sheet_components:
			component = {}
			component['component_price_type'] = price_sheet_component.price_type
			component['component_price_sub_type'] = price_sheet_component.price_sub_type
			component['cost_type'] = price_sheet_component.cost_type
			component['entered_value'] = str(price_sheet_component.amount)
			if 'Lumpsump' in price_sheet_component.cost_type:
				component['amount'] = price_sheet_component.amount
			elif 'Per sqft' in price_sheet_component.cost_type:
				calculated_sqft = 0
				if 'Basic' in price_sheet_component.price_type:
					if 'Super Builtup Area' in price_sheet_component.price_sub_type:
						calculated_sqft = int(unit_extra_info['data']['unit']['super_built_up_area'])
					elif 'Builtup Area' in price_sheet_component.price_sub_type:
						calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
					elif 'Carpet Area' in price_sheet_component.price_sub_type:
						calculated_sqft = int(unit_extra_info['data']['unit']['carpet_area'])
					else:
						calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
					component['amount'] = calculated_sqft*int(price_sheet_component.amount)
				elif 'PLC-Floorrise' in price_sheet_component.price_type:
					calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
					floor_number = unit_extra_info['data']['unit']['floor_number']
					if 'Fix Increasing Cost' in price_sheet_component.price_sub_type:
						component['amount'] = calculated_sqft*int(price_sheet_component.amount)*int(floor_number)
					elif 'Fix Decreasing Cost' in price_sheet_component.price_sub_type:
						component['amount'] = -(calculated_sqft*int(price_sheet_component.amount)*int(floor_number))
					elif price_sheet_component.price_sub_type==floor_number:
						component['amount'] = calculated_sqft*int(price_sheet_component.amount)
					else:
						component['amount'] = 0
				else:
					calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
					component['amount'] = calculated_sqft*int(price_sheet_component.amount)
			elif 'Percentage' in price_sheet_component.cost_type:
				component['amount'] = int(total_sale_value)*int(price_sheet_component.amount)/100
			#total_price += float(component['amount'])
			component['amount'] = str(component['amount'])

			components[price_sheet_component.pricesheet_component_id] = component
			
		result['components'] = components
		#result['extra_components'] = extra_components
		#result['total_price'] = total_price
		result['total_sale_value'] = total_sale_value

		data  = json.dumps(result)
		return HttpResponse(data)
	except Exception as e:
		print '%s %s (%s)' % ('Unit Price Sheet Error',e.message, type(e))
		result['error']=True
		result['error_message']=e.message
		data  = json.dumps(result)
		return HttpResponse(data)

@token_required
def get_booking_amount(request):
	booking_amount = 0.0
	try:
		if 'booking_id' in request.POST:
			booking_id = request.POST['booking_id']
			booking_amount = calc_booking_amount(booking_id, True)
		elif 'unit_id' in request.POST:
			unit_id = request.POST['unit_id']
			booking_amount = calc_booking_amount(unit_id, False)
	except Exception as e:
		print '%s %s (%s)' % ('get_booking_amount Error',e.message, type(e))
		result = {}
		result['error']=True
		result['error_message']= 'get_booking_amount Error => ' + e.message
		HttpResponse(json.dumps(result))

	return HttpResponse(booking_amount)

def calc_booking_amount(id, is_booked):
	if is_booked:
		return 20000
	else:
		return 20000

@token_required
def get_total_sale_value(request):
	try:
		total_sale_value = 0.0
		if 'booking_id' in request.POST:
			booking_id = request.POST['booking_id']
			total_sale_value = calc_total_sale_value(booking_id, True)
		elif 'unit_id' in request.POST:
			unit_id = request.POST['unit_id']
			total_sale_value = calc_total_sale_value(unit_id, False)
	except Exception as e:
		#logger.critical('%s %s (%s)' % ('get_total_sale_value Page Error:--',e.message, type(e)))
		print '%s %s (%s)' % ('get_total_sale_value Error',e.message, type(e))
		result = {}
		result['error']=True
		result['error_message']= 'get_total_sale_value Error => ' + e.message
		HttpResponse(json.dumps(result))

	return HttpResponse(total_sale_value)

def calc_total_sale_value(id, is_booked, price_sheet_id=None):
	try:
		total_sale_value = 0.0
		if is_booked:
			booking_id = id
			price_sheet_components = booked_pricesheet_component.objects.filter(booking_id=booking_id)
			if(price_sheet_components):
				for price_sheet_component in price_sheet_components:
					total_sale_value += float(price_sheet_component.total_amount)
		else:
			unit_id = id
			unit_info = booking_engine_units.objects.get(unit_id=unit_id)
			if unit_info.total_sale_value:
				total_sale_value = float(unit_info.total_sale_value)
			else:
				project_price_sheet_id = price_sheet_id
				if project_price_sheet_id:
					price_sheet_components = booking_engine_pricesheet_component.objects.filter(pricesheet_id=project_price_sheet_id)
				else:
					price_sheet_components = booking_engine_pricesheet_component.objects.filter(pricesheet_id=unit_info.price_sheet_id)
				total_sale_value_lumpsump = 0.0
				total_sale_value_percentage = 0.0

				unit_extra_info = getUnitData(str(unit_id))
				
				if(price_sheet_components):
					for price_sheet_component in price_sheet_components:
						if 'Lumpsump' in price_sheet_component.cost_type:
							total_sale_value_lumpsump += float(price_sheet_component.amount)
						elif 'Per sqft' in price_sheet_component.cost_type:
							calculated_sqft = 0
							if 'Basic' in price_sheet_component.price_type:
								if 'Super Builtup Area' in price_sheet_component.price_sub_type:
									calculated_sqft = int(unit_extra_info['data']['unit']['super_built_up_area'])
								elif 'Builtup Area' in price_sheet_component.price_sub_type:
									calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
								elif 'Carpet Area' in price_sheet_component.price_sub_type:
									calculated_sqft = int(unit_extra_info['data']['unit']['carpet_area'])
								else:
									calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
								total_sale_value_lumpsump += calculated_sqft*int(price_sheet_component.amount)
							elif 'PLC-Floorrise' in price_sheet_component.price_type:
								calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
								floor_number = unit_extra_info['data']['unit']['floor_number']
								print floor_number, " --> ", price_sheet_component.price_sub_type
								if 'Fix Increasing Cost' in price_sheet_component.price_sub_type:
									total_sale_value_lumpsump += calculated_sqft*int(price_sheet_component.amount)*int(floor_number)
								elif 'Fix Decreasing Cost' in price_sheet_component.price_sub_type:
									total_sale_value_lumpsump -= (calculated_sqft*int(price_sheet_component.amount)*int(floor_number))
								elif price_sheet_component.price_sub_type==floor_number:
									total_sale_value_lumpsump += calculated_sqft*int(price_sheet_component.amount)
								# else:
								# 	print "in else"
							else:
								calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
								total_sale_value_lumpsump += calculated_sqft*int(price_sheet_component.amount)
						else:
							total_sale_value_percentage += float(price_sheet_component.amount)
					#print total_sale_value_lumpsump, " ----- >  ", total_sale_value_percentage
					total_sale_value = round((100.0*total_sale_value_lumpsump)/(100.0-total_sale_value_percentage))
					#print total_sale_value
	except Exception as e:
		#logger.critical('%s %s (%s)' % ('calc_total_sale_value Page Error:--',e.message, type(e)))
		print '%s %s (%s)' % ('calc_total_sale_value Error => ',e.message, type(e))
	return total_sale_value

@token_required
def booked_unit_price_sheet(request):
	try:
		if 'booking_id' in request.POST:
			booking_id = request.POST['booking_id']
			price_sheet_components = booked_pricesheet_component.objects.filter(booking_id=booking_id)
			result = {}
			components = {}
			total_sale_value = 0.0

			for price_sheet_component in price_sheet_components:
				component = {}
				component['component_price_type'] = price_sheet_component.price_type
				component['component_price_sub_type'] = price_sheet_component.price_sub_type
				component['cost_type'] = price_sheet_component.cost_type
				component['entered_value'] = str(price_sheet_component.entered_value)
				component['amount'] = str(price_sheet_component.total_amount)
				
				if component['amount']:
					total_sale_value += float(component['amount'])
				components[price_sheet_component.pricesheet_component_id] = component
				
			result['components'] = components
			result['total_sale_value'] = total_sale_value

			data  = json.dumps(result)
			return HttpResponse(data)
		else:
			result = {}
			result['error'] = True
			result['error_message'] = 'No Booking ID Provided'
			data  = json.dumps(result)
			return HttpResponse(data)
	except Exception as e:
		print '%s %s (%s)' % ('Unit Price Sheet Error',e.message, type(e))
		result = {}
		result['error'] = True
		result['error_message'] = 'Unit Price Sheet Error' + e.message
		data  = json.dumps(result)
		return HttpResponse(data)

@token_required
def unit_payment_plan(request):
	result = {}
	try:
		unit_id = request.POST['unit_id']
	except Exception as e:
		print '%s %s (%s)' % ('Unit Payment Plan Error',e.message, type(e))
		result['error']=True
		result['error_message']='Unit Id is not provided.'
		data = json.dumps(result)
		return HttpResponse(data)

	is_unit_process = True
	try:
		unit_info = booking_engine_units.objects.get(unit_id=unit_id)
		payment_plan_id = unit_info.payment_plan_id
	except booking_engine_units.DoesNotExist:
		is_unit_process = False
		unit_info = None
		result['error']=True
		result['error_message']='Unit Id is not stored in the database.'
		data = json.dumps(result)
		return HttpResponse(data)

	try:
		if not is_unit_process:
			project_id = request.POST['project_id']
			payment_plan_info =	booking_engine_payment_plan.objects.get(project_id=project_id, is_default=True)
			payment_plan_id = payment_plan_info.payment_plan_id
	except booking_engine_payment_plan.DoesNotExist:
		result['error']=True
		result['error_message']='No Unit Payment Plan Found.'
		data  = json.dumps(result)
		return HttpResponse(data)

	try:
		payment_plan_milestones = booking_engine_payment_plan_milestones.objects.filter(payment_plan_id=payment_plan_id)
		milestones = {}
		#total_price = 0.0
		# total_sale_value_lumpsump = 0.0
		# total_sale_value_percentage = 0.0

		# for payment_plan_milestone in payment_plan_milestones:
		# 	if 'Lumpsump' in payment_plan_milestone.cost_type:
		# 		total_sale_value_lumpsump += float(payment_plan_milestone.amount)
		# 	else:
		# 		total_sale_value_percentage += float(payment_plan_milestone.amount)

		# total_sale_value = round((100.0*total_sale_value_lumpsump)/(100.0-total_sale_value_percentage))

		total_sale_value = calc_total_sale_value(unit_id, False)

		current_total_value = 0.0

		for payment_plan_milestone in payment_plan_milestones:
			milestone = {}
			milestone['milestone'] = payment_plan_milestone.milestone
			milestone['milestone_date'] = str(payment_plan_milestone.milestone_date)
			milestone['cost_type'] = payment_plan_milestone.cost_type
			milestone['entered_value'] = payment_plan_milestone.amount
			if 'Lumpsump' in payment_plan_milestone.cost_type:
				milestone['amount'] = payment_plan_milestone.amount
				current_total_value = current_total_value + float(milestone['amount'])
			elif 'Remaining Percentage' in payment_plan_milestone.cost_type:
				milestone['amount'] = float(int(total_sale_value)*int(payment_plan_milestone.amount)/100) - current_total_value
				current_total_value = current_total_value + float(milestone['amount'])
			elif 'Percentage' in payment_plan_milestone.cost_type:
				milestone['amount'] = int(total_sale_value)*int(payment_plan_milestone.amount)/100
				current_total_value = current_total_value + float(milestone['amount'])
			else:
				milestone['amount'] = payment_plan_milestone.amount

			milestones[payment_plan_milestone.payment_plan_milestone_id] = milestone

		result['milestones'] = milestones
		#result['total_price'] = total_price
		result['total_sale_value'] = total_sale_value

		data = json.dumps(result)
		return HttpResponse(data)

	except Exception as e:
		print '%s %s (%s)' % ('Unit Payment Plan Error => ',e.message, type(e))
		traceback.print_exc()
		result['error']=True
		result['error_message']='Unit Payment Plan Error => ' + e.message
		data = json.dumps(result)
		return HttpResponse(data)


@token_required
def book_payment_structure(request):
	result={}
	try:
		if request.method == 'POST':
			booking_id = request.POST['booking_id']
			if booking_id is None:
				result['error']=True
				result['error_message']='No Booking ID provided'
				data = json.dumps(result)
				return HttpResponse(data)
			try:
				booking_info = booking_engine_bookings.objects.get(booking_id=str(booking_id))
			except booking_engine_bookings.DoesNotExist:
				result['error']=True
				result['error_message']='No Booking Information is present for this booking ID'
				data = json.dumps(result)
				return HttpResponse(data)

			try:
				unit_info = booking_engine_units.objects.get(unit_id=booking_info.unit_id)
			except booking_engine_units.DoesNotExist:
				result['error']=True
				result['error_message']='No Unit Information is present for this booking ID'
				data = json.dumps(result)
				return HttpResponse(data)

			try:
				unit_extra_info = getUnitData(str(booking_info.unit_id))
			except:
				result['error']=True
				result['error_message']='No Unit Information from UnitSelector is present for this booking ID'
				data = json.dumps(result)
				return HttpResponse(data)
			
			payment_plans = booking_engine_payment_plan.objects.filter(payment_plan_id=unit_info.payment_plan_id)
			for payment_plan in payment_plans:			
				booking_in_progress_payment_plan = booked_payment_plan()
				booking_in_progress_payment_plan.payment_plan_id = payment_plan.payment_plan_id
				booking_in_progress_payment_plan.as_of_date = payment_plan.as_of_date
				booking_in_progress_payment_plan.payment_plan_name = payment_plan.payment_plan_name
				booking_in_progress_payment_plan.payment_plan_description = payment_plan.payment_plan_description
				booking_in_progress_payment_plan.project_id = payment_plan.project_id
				booking_in_progress_payment_plan.booking_id = booking_id
				booking_in_progress_payment_plan.save()

			payment_plan_milestones = booking_engine_payment_plan_milestones.objects.filter(payment_plan_id=unit_info.payment_plan_id)
			
			# total_sale_value_lumpsump = 0.0
			# total_sale_value_percentage = 0.0

			# for payment_plan_milestone in payment_plan_milestones:
			# 	if 'Lumpsump' in payment_plan_milestone.cost_type:
			# 		total_sale_value_lumpsump += float(payment_plan_milestone.amount)
			# 	else:
			# 		total_sale_value_percentage += float(payment_plan_milestone.amount)

			# total_sale_value = round((100.0*total_sale_value_lumpsump)/(100.0-total_sale_value_percentage))

			total_sale_value = calc_total_sale_value(booking_info.unit_id, False)

			for payment_plan_milestone in payment_plan_milestones:
				book_payment_plan_milestone = booked_payment_plan_milestones()
				book_payment_plan_milestone.payment_plan_id = payment_plan_milestone.payment_plan_id
				book_payment_plan_milestone.payment_plan_milestone_id = payment_plan_milestone.payment_plan_milestone_id
				book_payment_plan_milestone.milestone = payment_plan_milestone.milestone
				book_payment_plan_milestone.milestone_free_text = payment_plan_milestone.milestone_free_text
				book_payment_plan_milestone.milestone_date = payment_plan_milestone.milestone_date
				book_payment_plan_milestone.booking_id = booking_id
				book_payment_plan_milestone.cost_type = payment_plan_milestone.cost_type

				current_total_value = 0.0

				if 'Lumpsump' in payment_plan_milestone.cost_type:
					book_payment_plan_milestone.entered_value = 'Rs. '+str(payment_plan_milestone.amount)
					book_payment_plan_milestone.total_amount = payment_plan_milestone.amount
					current_total_value = current_total_value + book_payment_plan_milestone.total_amount
				elif 'Remaining Percentage' in payment_plan_milestone.cost_type:
					book_payment_plan_milestone.entered_value = str(payment_plan_milestone.amount) + '% of the Total Sale Value'
					book_payment_plan_milestone.total_amount = float(int(total_sale_value)*int(payment_plan_milestone.amount)/100) - current_total_value
					current_total_value = current_total_value + book_payment_plan_milestone.total_amount
				elif 'Percentage' in payment_plan_milestone.cost_type:
					book_payment_plan_milestone.entered_value = str(payment_plan_milestone.amount) + '% of the Total Sale Value'
					book_payment_plan_milestone.total_amount = int(total_sale_value)*int(payment_plan_milestone.amount)/100
					current_total_value = current_total_value + book_payment_plan_milestone.total_amount
				else:
					book_payment_plan_milestone.entered_value = str(payment_plan_milestone.amount)
					book_payment_plan_milestone.total_amount = payment_plan_milestone.amount

				book_payment_plan_milestone.formula = payment_plan_milestone.formula
				book_payment_plan_milestone.save()

			price_sheets = booking_engine_pricesheet.objects.filter(pricesheet_id=unit_info.price_sheet_id)
			for price_sheet in price_sheets:			
				booking_in_progress_price_sheet = booked_pricesheet()
				booking_in_progress_price_sheet.pricesheet_id = price_sheet.pricesheet_id
				booking_in_progress_price_sheet.as_of_date = price_sheet.as_of_date
				booking_in_progress_price_sheet.name = price_sheet.name
				booking_in_progress_price_sheet.description = price_sheet.description
				booking_in_progress_price_sheet.project_id = price_sheet.project_id
				booking_in_progress_price_sheet.booking_id = booking_id
				booking_in_progress_price_sheet.save()

			price_sheet_components = booking_engine_pricesheet_component.objects.filter(pricesheet_id=unit_info.price_sheet_id)
			
			# total_sale_value_lumpsump = 0.0
			# total_sale_value_percentage = 0.0

			# for price_sheet_component in price_sheet_components:
			# 	if 'Lumpsump' in price_sheet_component.cost_type:
			# 		total_sale_value_lumpsump += float(price_sheet_component.amount)
			# 	elif 'Per sqft' in price_sheet_component.cost_type:
			# 		calculated_sqft = 0
			# 		if 'Super Builtup Area' in price_sheet_component.price_sub_type:
			# 			calculated_sqft = int(unit_extra_info['data']['unit']['super_built_up_area'])
			# 		elif 'Builtup Area' in price_sheet_component.price_sub_type:
			# 			calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
			# 		elif 'Carpet Area' in price_sheet_component.price_sub_type:
			# 			calculated_sqft = int(unit_extra_info['data']['unit']['carpet_area'])
			# 		else:
			# 			calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
			# 		total_sale_value_lumpsump += calculated_sqft*int(price_sheet_component.amount)
			# 	else:
			# 		total_sale_value_percentage += float(price_sheet_component.amount)

			# total_sale_value = round((100.0*total_sale_value_lumpsump)/(100.0-total_sale_value_percentage))

			for price_sheet_component in price_sheet_components:
				book_pricesheet_component = booked_pricesheet_component()
				book_pricesheet_component.pricesheet_component_id = price_sheet_component.pricesheet_component_id
				book_pricesheet_component.pricesheet_id = price_sheet_component.pricesheet_id
				book_pricesheet_component.price_type = price_sheet_component.price_type
				book_pricesheet_component.price_sub_type = price_sheet_component.price_sub_type
				book_pricesheet_component.price_type_free_text = price_sheet_component.price_type_free_text
				book_pricesheet_component.price_sub_type_free_text = price_sheet_component.price_sub_type_free_text
				book_pricesheet_component.cost_type = price_sheet_component.cost_type
				book_pricesheet_component.booking_id = booking_id

				if 'Lumpsump' in price_sheet_component.cost_type:
					book_pricesheet_component.entered_value = 'Rs. '+str(price_sheet_component.amount)
					book_pricesheet_component.total_amount = price_sheet_component.amount
				elif 'Percentage' in price_sheet_component.cost_type:
					book_pricesheet_component.entered_value = str(price_sheet_component.amount) + '% of the Total Sale Value'
					book_pricesheet_component.total_amount = int(total_sale_value)*int(price_sheet_component.amount)/100
				elif 'Per sqft' in price_sheet_component.cost_type:
					calculated_sqft = 0
					if 'Basic' in price_sheet_component.price_type:
						if 'Super Builtup Area' in price_sheet_component.price_sub_type:
							calculated_sqft = int(unit_extra_info['data']['unit']['super_built_up_area'])
						elif 'Builtup Area' in price_sheet_component.price_sub_type:
							calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
						elif 'Carpet Area' in price_sheet_component.price_sub_type:
							calculated_sqft = int(unit_extra_info['data']['unit']['carpet_area'])
						else:
							calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
						book_pricesheet_component.total_amount = calculated_sqft*int(price_sheet_component.amount)
					elif 'PLC-Floorrise' in price_sheet_component.price_type:
						calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
						floor_number = unit_extra_info['data']['unit']['floor_number']
						if 'Fix Increasing Cost' in price_sheet_component.price_sub_type:
							book_pricesheet_component.total_amount += calculated_sqft*int(price_sheet_component.amount)*int(floor_number)
						elif 'Fix Decreasing Cost' in price_sheet_component.price_sub_type:
							book_pricesheet_component.total_amount -= (calculated_sqft*int(price_sheet_component.amount)*int(floor_number))
						elif price_sheet_component.price_sub_type==floor_number:
							book_pricesheet_component.total_amount = calculated_sqft*int(price_sheet_component.amount)
						else:
							book_pricesheet_component.total_amount = 0
					else:
						calculated_sqft = int(unit_extra_info['data']['unit']['built_up_area'])
						book_pricesheet_component.total_amount = calculated_sqft*int(price_sheet_component.amount)

					book_pricesheet_component.entered_value = 'Rs. ' + str(price_sheet_component.amount) + ' per sqft'
					book_pricesheet_component.total_amount = calculated_sqft*int(price_sheet_component.amount)
				else:
					book_pricesheet_component.entered_value = 'Rs. '+str(price_sheet_component.amount)
					book_pricesheet_component.total_amount = price_sheet_component.amount

				book_pricesheet_component.formula = price_sheet_component.formula
				book_pricesheet_component.save()

			booking_info.payment_plan_id = unit_info.payment_plan_id
			booking_info.price_sheet_id = unit_info.price_sheet_id
			booking_info.save()

			return HttpResponse('SUCCESS')
	except Exception as e:
		print '%s %s (%s)' % ('Booked Payment Plan Error',e.message, type(e))
		result['error']=True
		result['error_message']='Booked Payment Plan Error' + e.message
		data = json.dumps(result)
		return HttpResponse(data)

@token_required
def booked_unit_payment_plan(request):
	result = {}
	try:
		if 'booking_id' in request.POST:
			booking_id = request.POST['booking_id']
			payment_plan_milestones = booked_payment_plan_milestones.objects.filter(booking_id=booking_id).order_by("-milestone_date")
			milestones = {}
			total_sale_value = 0.0
			
			for payment_plan_milestone in payment_plan_milestones:
				milestone = {}
				milestone['milestone'] = payment_plan_milestone.milestone
				milestone['milestone_date'] = str(payment_plan_milestone.milestone_date)
				milestone['cost_type'] = payment_plan_milestone.cost_type
				milestone['entered_value'] = payment_plan_milestone.entered_value
				milestone['amount'] = payment_plan_milestone.total_amount

				if milestone['amount']:
					total_sale_value = total_sale_value + float(milestone['amount'])
				milestones[payment_plan_milestone.payment_plan_milestone_id] = milestone

			result['milestones'] = milestones
			result['total_sale_value'] = total_sale_value

			data = json.dumps(result)
			return HttpResponse(data)
		else:
			result['error']=True
			result['error_message']='No Booking ID Provided'
			data = json.dumps(result)
			return HttpResponse(data)

	except Exception as e:
		print '%s %s (%s)' % ('Unit Payment Plan Error => ',e.message, type(e))
		traceback.print_exc()
		result['error']=True
		result['error_message']='Unit Payment Plan Error => ' + e.message
		data = json.dumps(result)
		return HttpResponse(data)

def sendAsyncMail(subject , template_name, email_context, mails):
	scheduler.enter(1, 1, sendMail, argument=(subject , template_name, email_context,mails,))
	t = threading.Thread(target=scheduler.run)
	t.start()

def sendMail(subject , template_name, email_context, mails):
	print "in sendMail ", subject , template_name, email_context
	user_emails.send_templated_email(subject , template_name, email_context, mails)

@csrf_exempt
@login_required
def register(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin'):
		return redirect("/access_error")
	try:
		if request.method == 'POST':
			print "inside post"
			if 'register' in request.POST:
				user = User.objects.create_user(request.POST['user_name'], request.POST['email'], request.POST['password'])
				user.first_name = request.POST['first_name']
				user.last_name = request.POST['last_name']
				user.save()

				user_info = booking_engine_users()
				user_info.user_id = user.id
				user_info.role = request.POST['role']
				user_info.create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				user_info.save()

				messages.add_message(request, messages.SUCCESS, 'You have successfully signed up.')

				email_context = { 'username': user.first_name+' ' + user.last_name, 'user_email': user.email}
				sendAsyncMail('Welcome To The Booking CRM', 'mailers/registration_email.html', email_context, [user.email])

	except Exception as e:
		print '%s %s (%s)' % ('Sign up Page Error',e.message, type(e))
		messages.add_message(request, messages.ERROR, 'User Already Exists.')
		#return redirect("/error")

	return render_to_response("register.html", 
									locals(), 
									context_instance = RequestContext(request))


@login_required
def towers(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		projects = booking_engine_projects.objects.all()
	except booking_engine_projects.DoesNotExist:
		projects = None

	return render_to_response("towers.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
@csrf_exempt
def project_towers(request, project_id):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		project = booking_engine_projects.objects.filter(project_id=project_id)[:1].get()
	except booking_engine_projects.DoesNotExist:
		project = None

	try:
		if request.method == 'POST':
		 	if 'booking_engine_tower_delete' in request.POST:
				tower = booking_engine_towers.objects.filter(tower_id=request.POST['booking_engine_tower_id'])[:1].get()
				tower.delete()
				messages.add_message(request, messages.SUCCESS, 'You have successfully deleted a tower.')
			elif 'booking_engine_tower_create' in request.POST:
				tower = booking_engine_towers()
				tower.tower_id = id_generator()
				tower.project_id=project_id
				tower.tower_name=request.POST['tower_name']
				tower.no_of_floors = request.POST['tower_floors']
				tower.save()
				messages.add_message(request, messages.SUCCESS, 'You have successfully added a tower.')
			
		towers = booking_engine_towers.objects.filter(project_id=project_id)
	except booking_engine_payment_plan.DoesNotExist:
		towers = None

	return render_to_response("project_towers.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
def unit_variants(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		projects = booking_engine_projects.objects.all()
	except booking_engine_projects.DoesNotExist:
		projects = None

	return render_to_response("unit_variants.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
@csrf_exempt
def project_unit_variants(request, project_id):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		project = booking_engine_projects.objects.filter(project_id=project_id)[:1].get()
	except booking_engine_projects.DoesNotExist:
		project = None

	try:
		if request.method == 'POST':
		 	if 'booking_engine_unit_variant_delete' in request.POST:
				unit_variant = booking_engine_unit_variants.objects.filter(unit_variant_id=request.POST['unit_variant_id'])[:1].get()
				unit_variant.delete()
				messages.add_message(request, messages.SUCCESS, 'You have successfully deleted a unit variant.')
			elif 'booking_engine_unit_variant_create' in request.POST:
				unit_variant = booking_engine_unit_variants()
				unit_variant.unit_variant_id = id_generator()
				unit_variant.project_id=project_id
				unit_variant.unit_variant_name=request.POST['unit_variant_name']
				unit_variant.save()
				messages.add_message(request, messages.SUCCESS, 'You have successfully added a unit variant.')
			
		unit_variants = booking_engine_unit_variants.objects.filter(project_id=project_id)
	except booking_engine_unit_variants.DoesNotExist:
		unit_variants = None

	return render_to_response("project_unit_variants.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
def payment_plan(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		projects = booking_engine_projects.objects.all()
	except booking_engine_projects.DoesNotExist:
		projects = None

	return render_to_response("payment_plan.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
@csrf_exempt
def project_payment_plan(request, project_id):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		project = booking_engine_projects.objects.filter(project_id=project_id)[:1].get()
	except booking_engine_projects.DoesNotExist:
		project = None

	try:
		if request.method == 'POST':
		 	if 'payment_plan_delete' in request.POST:
				payment_plan = booking_engine_payment_plan.objects.filter(payment_plan_id=request.POST['payment_plan_id'])[:1].get()
				payment_plan.delete()
				messages.add_message(request, messages.SUCCESS, 'You have successfully deleted a payment plan.')
			elif 'payment_plan_create' in request.POST:
				is_default = False
				try:
					if booking_engine_payment_plan.objects.filter(project_id=project_id):
						is_default = False
					else:
						is_default = True
				except booking_engine_payment_plan.DoesNotExist:
					is_default = True

				payment_plan = booking_engine_payment_plan()
				payment_plan.payment_plan_id = id_generator()
				payment_plan.payment_plan_name=request.POST['payment_plan_name']
				payment_plan.payment_plan_description=request.POST['payment_plan_description']

				payment_plan.project_type_id=request.POST['payment_plan_property_type']
				payment_plan.tower_id=request.POST['payment_plan_property_tower']
				payment_plan.unit_variant_id=request.POST['payment_plan_property_unit_variant']
				payment_plan.broker_id=request.POST['broker_name']

				payment_plan.is_active = int(request.POST['is_active'])
				payment_plan.project_id = project_id;
				payment_plan.as_of_date = request.POST['payment_plan_date']
				payment_plan.is_default = is_default
				payment_plan.save()
				messages.add_message(request, messages.SUCCESS, 'You have successfully added a payment plan.')
			elif 'make_it_default' in request.POST:
				project_id = request.POST['project_id']
				payment_plan_id = request.POST['payment_plan_id']

				payment_plans = booking_engine_payment_plan.objects.filter(project_id=project_id)
				for payment_plan in payment_plans:
					if payment_plan.payment_plan_id == payment_plan_id:
						payment_plan.is_default = True
					else:
						payment_plan.is_default = False
					payment_plan.save()

				units = booking_engine_units.objects.filter(project_id=project_id)
				for unit in units:
					if unit.payment_plan_id == payment_plan_id:
						unit.is_default = True
					else:
						unit.is_default = False
					unit.save()
				messages.add_message(request, messages.SUCCESS, 'You have successfully made this payment plan as a default option.')

		payment_plan_info = execute_query("select pp.payment_plan_id as payment_plan_id, pp.payment_plan_name as payment_plan_name, pp.payment_plan_description as payment_plan_description, pp.project_type_id as project_type_id, pt.project_type_name as project_type_name, pp.tower_id as tower_id, t.tower_name as tower_name, pp.unit_variant_id as unit_variant_id, uv.unit_variant_name as unit_variant_name, pp.broker_id as broker_id, b.broker_name as broker_name, pp.is_active as is_active, pp.is_default as is_default, pp.project_id as project_id, pp.as_of_date as as_of_date from booking_engine_payment_plan pp LEFT JOIN booking_engine_project_types pt on pt.project_type_id=pp.project_type_id LEFT JOIN booking_engine_brokers b on b.broker_id=pp.broker_id LEFT JOIN booking_engine_unit_variants uv on uv.unit_variant_id=pp.unit_variant_id LEFT JOIN booking_engine_towers t on t.tower_id=pp.tower_id where pp.project_id='" + project_id + "'",'default')

		#payment_plan_info = booking_engine_payment_plan.objects.filter(project_id=project_id).order_by('-as_of_date')
	except booking_engine_payment_plan.DoesNotExist:
		payment_plan_info = None

	try:
		towers = booking_engine_towers.objects.filter(project_id=project_id)
	except booking_engine_towers.DoesNotExist:
		towers = None

	try:
		unit_variants = booking_engine_unit_variants.objects.filter(project_id=project_id)
	except booking_engine_unit_variants.DoesNotExist:
		unit_variants = None

	try:
		project_types = booking_engine_project_types.objects.all()
	except booking_engine_project_types.DoesNotExist:
		project_types = None

	try:
		brokers = booking_engine_brokers.objects.all()
	except booking_engine_brokers.DoesNotExist:
		brokers = None

	return render_to_response("project_payment_plan.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
def add_broker(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	
	try:
		if request.method == 'POST':
		 	if 'booking_engine_broker_delete' in request.POST:
				broker = booking_engine_brokers.objects.filter(broker_id=request.POST['broker_id'])[:1].get()
				broker.delete()
				messages.add_message(request, messages.SUCCESS, 'You have successfully deleted a broker.')
			elif 'booking_engine_broker_create' in request.POST:
				broker = booking_engine_brokers()
				broker.broker_id = id_generator()
				broker.broker_name=request.POST['broker_name']
				broker.save()
				messages.add_message(request, messages.SUCCESS, 'You have successfully added a broker.')
			
		brokers = booking_engine_brokers.objects.all()
	except booking_engine_brokers.DoesNotExist:
		brokers = None

	return render_to_response("add_broker.html", 
								locals(), 
								context_instance = RequestContext(request))

@login_required
@csrf_exempt
def project_payment_plan_edit(request, payment_plan_id):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	if request.method == 'POST':
		if 'payment_plan_edit' in request.POST:
			payment_plan_info = booking_engine_payment_plan.objects.get(payment_plan_id=payment_plan_id)
			payment_plan_info.payment_plan_name = request.POST['payment_plan_name']
			payment_plan_info.payment_plan_description = request.POST['payment_plan_description']

			payment_plan_info.project_type_id=request.POST['payment_plan_property_type']
			payment_plan_info.tower_id=request.POST['payment_plan_property_tower']
			payment_plan_info.unit_variant_id=request.POST['payment_plan_property_unit_variant']
			payment_plan_info.broker_id=request.POST['broker_name']

			payment_plan_info.is_active = int(request.POST['is_active'])
			payment_plan_info.as_of_date = request.POST['payment_plan_date']
			payment_plan_info.save()
			messages.add_message(request, messages.SUCCESS, 'You have successfully edited this payment plan.')
		if 'payment_plan_milestone_create' in request.POST:
	 		payment_plan_milestone = booking_engine_payment_plan_milestones()
	 		payment_plan_milestone.payment_plan_milestone_id = id_generator()
	 		payment_plan_milestone.payment_plan_id = payment_plan_id
			payment_plan_milestone.milestone=request.POST['milestone']
			payment_plan_milestone.milestone_free_text=request.POST['milestone_free_text']
			payment_plan_milestone.cost_type=request.POST['cost_type']
			payment_plan_milestone.amount=request.POST['amount']
			if(request.POST['milestone_date']==''):
				payment_plan_milestone.milestone_date = None
			else:
				payment_plan_milestone.milestone_date = request.POST['milestone_date']
			payment_plan_milestone.save()
			messages.add_message(request, messages.SUCCESS, 'You have successfully added a payment plan milestone.')	
	 	if 'payment_plan_milestone_update' in request.POST:
	 		payment_plan_milestone = booking_engine_payment_plan_milestones.objects.get(payment_plan_milestone_id=request.POST['payment_plan_milestone_id'])
			payment_plan_milestone.milestone=request.POST['milestone']
			payment_plan_milestone.milestone_free_text=request.POST['milestone_free_text']
			payment_plan_milestone.cost_type=request.POST['cost_type']
			payment_plan_milestone.amount=request.POST['amount']
			if(request.POST['milestone_date']==''):
				payment_plan_milestone.milestone_date = None
			else:
				payment_plan_milestone.milestone_date = request.POST['milestone_date']
			payment_plan_milestone.save()
			messages.add_message(request, messages.SUCCESS, 'You have successfully updated a payment plan milestone.')
		if 'payment_plan_milestone_delete' in request.POST:
			print "payment_plan_milestone_id -> ", request.POST['payment_plan_milestone_id']
			payment_plan_milestone = booking_engine_payment_plan_milestones.objects.get(payment_plan_milestone_id=request.POST['payment_plan_milestone_id'])
			payment_plan_milestone.delete()
			messages.add_message(request, messages.SUCCESS, 'You have successfully deleted a payment plan milestone.')
		if 'update_all_units' in request.POST:
			payment_plan_id = request.POST['payment_plan_id']
			project_id = request.POST['project_id']
			return_message = update_payment_plan_for_project(project_id, payment_plan_id)
			if(return_message == "SUCCESS"):
				messages.add_message(request, messages.SUCCESS, 'You have successfully made this payment plan as a default option for all units.')
			else:
				messages.add_message(request, messages.ERROR, 'Some Error happened in updating all units.')
	try:
		payment_plan_info = booking_engine_payment_plan.objects.filter(payment_plan_id=payment_plan_id)[:1].get()
	except booking_engine_payment_plan.DoesNotExist:
		payment_plan_info = None

	try:
		payment_plan_milestone_info = booking_engine_payment_plan_milestones.objects.filter(payment_plan_id=payment_plan_id)
	except booking_engine_payment_plan_milestones.DoesNotExist:
		payment_plan_milestone_info = None

	try:
		project = booking_engine_projects.objects.get(project_id=payment_plan_info.project_id)
	except booking_engine_projects.DoesNotExist:
		project = None

	try:
		towers = booking_engine_towers.objects.filter(project_id=payment_plan_info.project_id)
	except booking_engine_towers.DoesNotExist:
		towers = None

	try:
		unit_variants = booking_engine_unit_variants.objects.filter(project_id=payment_plan_info.project_id)
	except booking_engine_unit_variants.DoesNotExist:
		unit_variants = None

	try:
		project_types = booking_engine_project_types.objects.all()
	except booking_engine_project_types.DoesNotExist:
		project_types = None

	try:
		brokers = booking_engine_brokers.objects.all()
	except booking_engine_brokers.DoesNotExist:
		brokers = None

	TOKENIZER_USER_ID = constants.TOKENIZER_USER_ID
	TOKENIZER_TOKEN = constants.TOKENIZER_TOKEN

	return render_to_response("project_payment_plan_edit.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
@csrf_exempt
def project_price_sheet_edit(request, price_sheet_id):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	if request.method == 'POST':
		if 'price_sheet_edit' in request.POST:
			price_sheet_info = booking_engine_pricesheet.objects.get(pricesheet_id=price_sheet_id)
			price_sheet_info.name = request.POST['price_sheet_name']
			price_sheet_info.description = request.POST['price_sheet_description']

			price_sheet_info.project_type_id=request.POST['price_sheet_property_type']
			price_sheet_info.tower_id=request.POST['price_sheet_property_tower']
			price_sheet_info.unit_variant_id=request.POST['price_sheet_property_unit_variant']
			price_sheet_info.broker_id=request.POST['broker_name']

			price_sheet_info.is_active = int(request.POST['is_active'])
			price_sheet_info.as_of_date = request.POST['price_sheet_date']
			price_sheet_info.save()
			messages.add_message(request, messages.SUCCESS, 'You have successfully edited a price sheet.')
		if 'price_sheet_component_create' in request.POST:
			print request.POST
			price_sheet_component = booking_engine_pricesheet_component()
			price_sheet_component.pricesheet_component_id = id_generator()
			price_sheet_component.pricesheet_id = price_sheet_id
			price_sheet_component.price_type=request.POST['price_type']
			price_sheet_component.price_type_free_text=request.POST['price-type-free-text']
			if request.POST['price_type']=="Basic" or request.POST['price_type']=="Parking" or request.POST['price_type']=="View Facing" or request.POST['price_type']=="Direction" or request.POST['price_type']=="PLC" or request.POST['price_type']=="PLC-Floorrise":
				price_sheet_component.price_sub_type=request.POST['price_sub_type_sqft']
			else:
				price_sheet_component.price_sub_type=request.POST['price_sub_type']
			price_sheet_component.price_sub_type_free_text=request.POST['price-sub-type-free-text']
			price_sheet_component.cost_type=request.POST['cost_type']
			price_sheet_component.amount=request.POST['amount']
			price_sheet_component.save()
			messages.add_message(request, messages.SUCCESS, 'You have successfully created a price sheet component.')
		if 'price_sheet_component_update' in request.POST:
			print 'pricesheet_component_id',request.POST['price_sheet_component_id']
			price_sheet_component = booking_engine_pricesheet_component.objects.get(pricesheet_component_id=request.POST['price_sheet_component_id'])
			price_sheet_component.price_type=request.POST['price_type']
			price_sheet_component.price_type_free_text=request.POST['price-type-free-text']
			#price_sheet_component.price_sub_type=request.POST['price_sub_type']
			price_sheet_component.price_sub_type_free_text=request.POST['price-sub-type-free-text']
			price_sheet_component.cost_type=request.POST['cost_type']
			if request.POST['price_type']=="Basic" or request.POST['price_type']=="Parking" or request.POST['price_type']=="View Facing" or request.POST['price_type']=="Direction" or request.POST['price_type']=="PLC" or request.POST['price_type']=="PLC-Floorrise":
				price_sheet_component.price_sub_type=request.POST['price_sub_type_sqft']
			else:
				price_sheet_component.price_sub_type=request.POST['price_sub_type']
			price_sheet_component.amount=request.POST['amount']
			price_sheet_component.save()
			messages.add_message(request, messages.SUCCESS, 'You have successfully updated a price sheet component.')
		if 'price_sheet_component_delete' in request.POST:
			price_sheet_component = booking_engine_pricesheet_component.objects.get(pricesheet_component_id=request.POST['price_sheet_component_id'])
			price_sheet_component.delete()
			messages.add_message(request, messages.SUCCESS, 'You have successfully deleted a price sheet component.')
		if 'update_all_units' in request.POST:
			price_sheet_id = request.POST['price_sheet_id']
			project_id = request.POST['project_id']
			return_message = update_price_sheet_for_project(project_id, price_sheet_id)
			if(return_message == "SUCCESS"):
				messages.add_message(request, messages.SUCCESS, 'You have successfully made this price sheet as a default option for all units.')
			else:
				messages.add_message(request, messages.ERROR, 'Some Error happened in updating all units.')
	try:
		price_sheet_info = booking_engine_pricesheet.objects.get(pricesheet_id=price_sheet_id)
	except booking_engine_pricesheet.DoesNotExist:
		price_sheet_info = None

	try:
		price_sheet_component_info = booking_engine_pricesheet_component.objects.filter(pricesheet_id=price_sheet_id)
	except booking_engine_pricesheet_component.DoesNotExist:
		price_sheet_component_info = None

	try:
		project = booking_engine_projects.objects.get(project_id=price_sheet_info.project_id)
	except booking_engine_projects.DoesNotExist:
		project = None

	try:
		towers = booking_engine_towers.objects.filter(project_id=price_sheet_info.project_id)
	except booking_engine_towers.DoesNotExist:
		towers = None

	try:
		unit_variants = booking_engine_unit_variants.objects.filter(project_id=price_sheet_info.project_id)
	except booking_engine_unit_variants.DoesNotExist:
		unit_variants = None

	try:
		project_types = booking_engine_project_types.objects.all()
	except booking_engine_project_types.DoesNotExist:
		project_types = None

	try:
		brokers = booking_engine_brokers.objects.all()
	except booking_engine_brokers.DoesNotExist:
		brokers = None

	TOKENIZER_USER_ID = constants.TOKENIZER_USER_ID
	TOKENIZER_TOKEN = constants.TOKENIZER_TOKEN

	return render_to_response("project_price_sheet_edit.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
def pricing_structure(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		projects = booking_engine_projects.objects.all()
	except booking_engine_projects.DoesNotExist:
		projects = None

	return render_to_response("pricing_structure.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
@csrf_exempt
def project_pricing_structure(request, project_id):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		project = booking_engine_projects.objects.get(project_id=project_id)
	except booking_engine_projects.DoesNotExist:
		project = None

	try:
		if request.method == 'POST':
			if 'price_sheet_create' in request.POST:
				is_default = False
				try:
					if booking_engine_pricesheet.objects.filter(project_id=project_id):
						is_default = False
					else:
						is_default = True
				except booking_engine_pricesheet.DoesNotExist:
					is_default = True

				price_sheet = booking_engine_pricesheet()
				price_sheet.pricesheet_id = id_generator()
				price_sheet.name = request.POST['price_sheet_name']
				price_sheet.description = request.POST['price_sheet_description']

				price_sheet.project_type_id=request.POST['price_sheet_property_type']
				price_sheet.tower_id=request.POST['price_sheet_property_tower']
				price_sheet.unit_variant_id=request.POST['price_sheet_property_unit_variant']
				price_sheet.broker_id=request.POST['broker_name']

				price_sheet.is_active = int(request.POST['is_active'])
				price_sheet.project_id = project_id;
				price_sheet.as_of_date = request.POST['price_sheet_date']
				price_sheet.is_default = is_default
				price_sheet.save()
				messages.add_message(request, messages.SUCCESS, 'You have successfully created a price sheet.')
		 	if 'pricing_structure_delete' in request.POST:
				pricing_structure = booking_engine_pricesheet.objects.get(pricesheet_id=request.POST['price_sheet_id'])
				pricing_structure.delete()
				messages.add_message(request, messages.SUCCESS, 'You have successfully deleted a price sheet.')
			if 'make_it_default' in request.POST:
				project_id = request.POST['project_id']
				price_sheet_id = request.POST['price_sheet_id']

				pricesheets = booking_engine_pricesheet.objects.filter(project_id=project_id)
				for pricesheet in pricesheets:
					if pricesheet.pricesheet_id == price_sheet_id:
						pricesheet.is_default = True
					else:
						pricesheet.is_default = False
					pricesheet.save()

				units = booking_engine_units.objects.filter(project_id=project_id)
				for unit in units:
					if unit.price_sheet_id == price_sheet_id:
						unit.is_default = True
					else:
						unit.is_default = False
					unit.save()
				messages.add_message(request, messages.SUCCESS, 'You have successfully made this price sheet as a default option.')
		

		pricing_structure_info = execute_query("select pp.pricesheet_id as pricesheet_id, pp.name as name, pp.description as description, pp.project_type_id as project_type_id, pt.project_type_name as project_type_name, pp.tower_id as tower_id, t.tower_name as tower_name, pp.unit_variant_id as unit_variant_id, uv.unit_variant_name as unit_variant_name, pp.broker_id as broker_id, b.broker_name as broker_name, pp.is_active as is_active, pp.is_default as is_default, pp.project_id as project_id, pp.as_of_date as as_of_date from booking_engine_pricesheet pp LEFT JOIN booking_engine_project_types pt on pt.project_type_id=pp.project_type_id LEFT JOIN booking_engine_brokers b on b.broker_id=pp.broker_id LEFT JOIN booking_engine_unit_variants uv on uv.unit_variant_id=pp.unit_variant_id LEFT JOIN booking_engine_towers t on t.tower_id=pp.tower_id where pp.project_id='" + project_id + "'",'default')

		#pricing_structure_info = booking_engine_pricesheet.objects.filter(project_id=project_id)
	except booking_engine_pricesheet.DoesNotExist:
		pricing_structure_info = None

	try:
		towers = booking_engine_towers.objects.filter(project_id=project_id)
	except booking_engine_towers.DoesNotExist:
		towers = None

	try:
		unit_variants = booking_engine_unit_variants.objects.filter(project_id=project_id)
	except booking_engine_unit_variants.DoesNotExist:
		unit_variants = None

	try:
		project_types = booking_engine_project_types.objects.all()
	except booking_engine_project_types.DoesNotExist:
		project_types = None

	try:
		brokers = booking_engine_brokers.objects.all()
	except booking_engine_brokers.DoesNotExist:
		brokers = None

	return render_to_response("project_pricing_structure.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
@csrf_exempt
def booking_info(request, booking_id):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Booking Team'):
		return redirect("/access_error")
	checked_status = ''

	try:
		booking_info = booking_engine_bookings.objects.get(booking_id=booking_id)
	except booking_engine_bookings.DoesNotExist:
		print "in booking_info"
		booking_info = None

	if booking_info != None:
		try:
			buyer_info = booking_engine_buyers.objects.get(buyer_id=booking_info.buyer_id)
		except booking_engine_buyers.DoesNotExist:
			print "in buyer_info"
			buyer_info = None

		try:
			unit_info = booking_engine_units.objects.get(unit_id=booking_info.unit_id)
		except booking_engine_units.DoesNotExist:
			unit_info = None

		try:
			unit_extra_info = getUnitData(str(booking_info.unit_id))
		except:
			unit_extra_info = None

		try:
			pricesheet_info = booked_pricesheet.objects.filter(pricesheet_id=booking_info.price_sheet_id, booking_id=booking_id)[:1].get()
		except booking_engine_pricesheet.DoesNotExist:
			pricesheet_info = None

		try:
			pricesheet_component_info = booked_pricesheet_component.objects.filter(pricesheet_id=booking_info.price_sheet_id, booking_id=booking_id)
		except booking_engine_pricesheet_component.DoesNotExist:
			pricesheet_component_info = None

		try:
			payment_plan_info = booked_payment_plan.objects.filter(payment_plan_id=booking_info.payment_plan_id, booking_id=booking_id)[:1].get()
		except booking_engine_payment_plan.DoesNotExist:
			payment_plan_info = None

		try:
			payment_plan_milestone_info = booked_payment_plan_milestones.objects.filter(payment_plan_id=booking_info.payment_plan_id, booking_id=booking_id).order_by('-milestone_date')
		except booking_engine_payment_plan_milestones.DoesNotExist:
			payment_plan_milestone_info = None

		total_sale_value = calc_total_sale_value(booking_id, True)
		booking_amount = calc_booking_amount(booking_id, True)

		# try:
		# 	tower_info = booking_engine_towers.objects.get(tower_id=unit_info.tower_id)
		# except booking_engine_towers.DoesNotExist:
		# 	tower_info = None

		# try:
		# 	project_info = booking_engine_projects.objects.get(project_id=unit_info.project_id)
		# except booking_engine_projects.DoesNotExist:
		# 	project_info = None

		try:
			project_contact_info = booking_engine_project_contacts.objects.filter(project_id=unit_info.project_id).order_by('contact_designation')
		except booking_engine_project_contacts.DoesNotExist:
			project_contact_info = None

		try:
			booking_histories = booking_engine_booking_history.objects.filter(booking_id=booking_id).order_by('-updated_on')
		except booking_engine_booking_history.DoesNotExist:
			booking_histories = None

		try:
			payment_histories = booking_engine_payment_history.objects.filter(booking_id=booking_id).order_by('-updated_on')
		except booking_engine_payment_history.DoesNotExist:
			payment_histories = None

	if(request.method=='POST'):
		if 'payment_status_update' in request.POST:
			payment_id = request.POST['payment_id']
			change_payment_status = request.POST['change_payment_status']
			booking_id = request.POST['booking_id']

			payment_history = booking_engine_payment_history()
			payment_history.payment_id = payment_id
			payment_history.booking_id = booking_id
			payment_history.payment_status = change_payment_status
			payment_history.is_active = 1
			payment_history.updated_on = datetime.now()
			payment_history.save()

			messages.add_message(request, messages.SUCCESS, 'Payment status has been changed.')

	TOKENIZER_USER_ID = constants.TOKENIZER_USER_ID
	TOKENIZER_TOKEN = constants.TOKENIZER_TOKEN

	return render_to_response("booking-info.html", 
									locals(), 
									context_instance = RequestContext(request))

def rand_x_digit_num(x, leading_zeroes=True):
    """Return an X digit number, leading_zeroes returns a string, otherwise int"""
    if not leading_zeroes:
        # wrap with str() for uniform results
        return random.randint(10**(x-1), 10**x-1)  
    else:
        if x > 6000:
            return ''.join([str(random.randint(0, 9)) for i in xrange(x)])
        else:
            return '{0:0{x}d}'.format(random.randint(0, 10**x-1), x=x)

@login_required
@csrf_exempt
def check_payment_status(request):
	print 'inside check_payment_status'
	try:
		if 'user_role' not in request.session:
			user_detail = booking_engine_users.objects.get(user_id=request.user.id)
			request.session['user_role'] = user_detail.role
		user_role = request.session['user_role']
		if(user_role != 'Admin' and user_role != 'Booking Team'):
			return redirect("/access_error")
		key = server_setting.settings.PAYU_INFO['merchant_key']
		salt = server_setting.settings.PAYU_INFO['merchant_salt']
		command = "verify_payment"
		var1 = request.POST['transaction_id'] #Payu Request ID of transaction

		hash_str = key  + '|' + command + '|' + var1 + '|' + salt
		hash = hashlib.sha512(hash_str)
		hash_digest_str = hash.hexdigest().lower()

		data_payu = {}
		data_payu['key'] = key
		data_payu['var1'] = var1
		data_payu['hash'] = hash_digest_str
		data_payu['command'] = command

		sender_url = server_setting.settings.PAYU_INFO['payment_url']
		request_payu = urllib2.Request(sender_url)
		request_payu.add_data(urllib.urlencode(data_payu))
		request_payu.add_header('Accept-encoding', 'gzip')
		response_payu = urllib2.urlopen(request_payu)
		if response_payu.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(response_payu.read())
			f = gzip.GzipFile(fileobj=buf)
			response_api_val = f.read()

		response_api = json.loads(response_api_val)
		#print response_api

		result = {}

		if response_api['status'] == 1:
			result['status'] = 1
			if response_api['transaction_details'][var1]:
				result['checked_status'] = response_api['transaction_details'][var1]['unmappedstatus']
			else:
				result['error'] = 'No Payment Exists with this payment id in Payu'
		else:
			result['status'] = 0
			result['error'] = 'No Payment Exists with this payment id in Payu'
	except Exception as e:
		result['status'] = 0
		result['error'] = e.message
		print "Exception occured with reason => ", e.message
	return HttpResponse(json.dumps(result))

@login_required
@csrf_exempt
def update_payment_status(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Booking Team'):
		return redirect("/access_error")
	try:
		if(request.method=='POST'):
			payment_id = request.POST['payment_id']
			change_payment_status = request.POST['change_payment_status']
			booking_id = request.POST['booking_id']

			payment_history = booking_engine_payment_history()
			payment_history.payment_id = payment_id
			payment_history.booking_id = booking_id
			payment_history.payment_status = change_payment_status
			payment_history.is_active = 1
			payment_history.updated_on = datetime.now()
			payment_history.save()

			return HttpResponse("SUCCESS")
		else:
			return HttpResponse("FAILURE")

	except Exception as e:
		print '%s %s (%s)' % ('update_payment_status Error',e.message, type(e))

@login_required
@csrf_exempt
def refund_payment(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Booking Team'):
		return redirect("/access_error")
	try:
		key = server_setting.settings.PAYU_INFO['merchant_key']
		salt = server_setting.settings.PAYU_INFO['merchant_salt']
		command = "cancel_refund_transaction"
		print request.POST['amount']
		var1 = request.POST['mihpayid'] #Payu Request ID of transaction

		hash_str = key  + '|' + command + '|' + var1 + '|' + salt
		hash = hashlib.sha512(hash_str)
		hash_digest_str = hash.hexdigest().lower()

		data_payu = {}
		data_payu['key'] = key
		data_payu['var1'] = var1
		data_payu['hash'] = hash_digest_str
		data_payu['command'] = command
		data_payu['var2'] = rand_x_digit_num(7)
		data_payu['var3'] = request.POST['amount']

		sender_url = server_setting.settings.PAYU_INFO['payment_url']


		request_payu = urllib2.Request(sender_url)
		request_payu.add_data(urllib.urlencode(data_payu))
		request_payu.add_header('Accept-encoding', 'gzip')
		response_payu = urllib2.urlopen(request_payu)
		if response_payu.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(response_payu.read())
			f = gzip.GzipFile(fileobj=buf)
			response_api_val = f.read()

		response_api = json.loads(response_api_val)

		print response_api
		refund_payment_status = {}

		if response_api['status'] == 1:
			refund_payment_status['status'] = 1
			#refund_payment_status['txn_update_id'] = response_api['txn_update_id']
			payment_history = booking_engine_payment_history()
			payment_history.payment_id = request.POST['payment_id']
			payment_history.booking_id = request.POST['booking_id']
			payment_history.payment_status = 'Refund Initiated'
			payment_history.is_active = 1
			payment_history.updated_on = datetime.now()
			payment_history.mihpayid = var1
			payment_history.save()

			booking = booking_engine_bookings.objects.get(booking_id=request.POST['booking_id'])

			booking_history = booking_engine_booking_history()
			booking_history.booking_history_id = id_generator(size=13)
			booking_history.booking_id = request.POST['booking_id']
			booking_history.old_status = booking.status
			booking_history.new_status = 'Cancelled'
			booking_history.comments = 'Commonfloor has cancelled this booking'
			booking_history.updated_on = datetime.now()
			booking_history.updated_by = request.user.first_name+ " " +request.user.last_name
			booking_history.save()

			booking.status='Cancelled'
			booking.save()

			api_call.updateUnitInfoStatus(request.POST['unit_id'], 'available')

			booking_user = User.objects.get(id=request.POST['buyer_id'])

			email_context = { 'username': booking_user.first_name+' ' + booking_user.last_name, 'user_email': booking_user.email, 'booking_id': request.POST['booking_id']}
			sendAsyncMail('You have cancelled a booking - ' + request.POST['booking_id'], 'mailers/cancelled_booking.html', email_context, [booking_user.email])
		else:
			#checked_status = 'No Payment Exists with this payment id in Payu'
			refund_payment_status['status'] = 0
			refund_payment_status['error'] = response_api['msg']
			#print response_api
	except Exception as e:
		print "Error in refund_payment => ", e.message
	return HttpResponse(json.dumps(refund_payment_status))

@login_required
def bookings(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Booking Team'):
		return redirect("/access_error")
	try:
		if(request.method=='GET'):
			if 'buyer_id' in request.GET:
				bookings = execute_query("select beb.booking_id as booking_id, bebu.buyer_name as buyer_name, bebu.email as email, bebu.phone as phone, bep.project_name, beu.unit_name as unit_purchased, beb.booking_date as purchase_date, beb.status as status from booking_engine_bookings beb, booking_engine_units beu, booking_engine_projects bep, booking_engine_buyers bebu where beb.buyer_id=bebu.buyer_id and beb.unit_id=beu.unit_id and beu.project_id=bep.project_id and beb.status!='Initialized' and beb.buyer_id='"+request.GET['buyer_id']+"'",'default')
			else:
				bookings = execute_query("select beb.booking_id as booking_id, bebu.buyer_name as buyer_name, bebu.email as email, bebu.phone as phone, bep.project_name, beu.unit_name as unit_purchased, beb.booking_date as purchase_date, beb.status as status from booking_engine_bookings beb, booking_engine_units beu, booking_engine_projects bep, booking_engine_buyers bebu where beb.buyer_id=bebu.buyer_id and beb.unit_id=beu.unit_id and beu.project_id=bep.project_id and beb.status!='Initialized'",'default')	
		else:
			bookings = execute_query("select beb.booking_id as booking_id, bebu.buyer_name as buyer_name, bebu.email as email, bebu.phone as phone, bep.project_name, beu.unit_name as unit_purchased, beb.booking_date as purchase_date, beb.status as status from booking_engine_bookings beb, booking_engine_units beu, booking_engine_projects bep, booking_engine_buyers bebu where beb.buyer_id=bebu.buyer_id and beb.unit_id=beu.unit_id and beu.project_id=bep.project_id and beb.status!='Initialized'",'default')
	except booking_engine_buyers.DoesNotExist:
		bookings = None
	return render_to_response("bookings.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
def buyer_list(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Booking Team'):
		return redirect("/access_error")
	try:
		buyers = None
		if request.method == 'POST':
		 	if 'search_buyer' in request.POST:
		 		search_term = request.POST['search-term']
		 		buyers = booking_engine_buyers.objects.filter(buyer_name__contains=search_term)
		else:
			buyers = booking_engine_buyers.objects.all()
	except booking_engine_buyers.DoesNotExist:
		buyers = None

	return render_to_response("buyers.html", 
									locals(), 
									context_instance = RequestContext(request))

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def getPropertyTowers():
	try:
		if(request.method=='POST'):
			project_id = request.POST['property_id']
			towers = booking_engine_towers.objects.filter(project_id=project_id)
			return HttpResponse(towers)
	except Exception as e:
		print '%s %s (%s)' % ('getPropertyTowers Error',e.message, type(e))

def get_cities():
	response_api = api_call.getAPICities()
	result = {}
	if response_api:
		result = response_api

	return result

@csrf_exempt
@login_required
def getAreaDetail(request):
	print "Start Area Search"
	city= request.POST['cityName']
	area= request.POST['area']
	areaData =api_call.getAPIAreaByCity(city,area)
	#print areaData
	return HttpResponse(json.dumps(areaData))
    #return render(request, "hello1.html", {'names': names})

@csrf_exempt
@login_required
def getPropertyDetail(request):
	print "Start Property Search"
	cityName= request.POST['cityName']
	areaName= request.POST['areaZone']
	propertyData =api_call.getAPIPropertyByArea(cityName,areaName)
	return HttpResponse(json.dumps(propertyData))

def getUnitData(unit_id):
	get_unit_info = api_call.getUnitInfo(unit_id)
	if 'error' in get_unit_info:
		print getUnitInfo['error_message']
		return None
	return get_unit_info

@token_required
def getPropertyURL(property_id):
	povp_url =api_call.getPropertyURL(property_id)
	return HttpResponse(json.dumps(povp_url))

@token_required
def addUnit(request):
	try:
		if request.method == 'POST':
			try:
				booking_engine_unit = booking_engine_units.objects.get(unit_id=request.POST['unit_id'])
			except booking_engine_units.DoesNotExist:
				booking_engine_unit = booking_engine_units()

			project_id = request.POST['project_id']
			default_payment_plan_id = None
			default_price_sheet_id = None
			
			try:
				payment_plan = booking_engine_payment_plan.objects.get(project_id=project_id, is_default=True)
				default_payment_plan_id = payment_plan.payment_plan_id
			except booking_engine_payment_plan.DoesNotExist:
				default_payment_plan_id = None

			try:
				price_sheet = booking_engine_pricesheet.objects.get(project_id=project_id, is_default=True)
				default_price_sheet_id = price_sheet.pricesheet_id
			except booking_engine_pricesheet.DoesNotExist:
				default_price_sheet_id = None

			booking_engine_unit.unit_id = request.POST['unit_id']
			booking_engine_unit.unit_name = request.POST['unit_name']
			booking_engine_unit.project_id = project_id
			booking_engine_unit.booking_amount = 20000
			booking_engine_unit.payment_plan_id = default_payment_plan_id
			booking_engine_unit.price_sheet_id = default_price_sheet_id
			booking_engine_unit.save()

			return HttpResponse("SUCCESS")
		else:
			return HttpResponse("FAILURE")

	except Exception as e:
		print '%s %s (%s)' % ('addUnit Error',e.message, type(e))

@token_required
def deleteUnit(request):
	try:
		if request.method == 'POST':
			booking_engine_all_units = booking_engine_units.objects.filter(unit_id=request.POST['unit_id'])
			for booking_engine_unit in booking_engine_all_units:
				booking_engine_unit.delete()

			return HttpResponse("SUCCESS")
		else:
			return HttpResponse("FAILURE")

	except Exception as e:
		print '%s %s (%s)' % ('deleteUnit Error',e.message, type(e))
		return HttpResponse("FAILURE")

@login_required
def update_payment_plan_for_project(project_id, payment_plan_id):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		booking_engine_all_units = booking_engine_units.objects.filter(project_id=project_id)

		for booking_engine_unit in booking_engine_all_units:
			booking_engine_unit.payment_plan_id = payment_plan_id
			booking_engine_unit.save()

		return "SUCCESS"
	except Exception as e:
		print '%s %s (%s)' % ('update_payment_plan_for_project Error',e.message, type(e))
		return "FAILURE"

@login_required
def update_price_sheet_for_project(project_id, price_sheet_id):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		booking_engine_all_units = booking_engine_units.objects.filter(project_id=project_id)

		for booking_engine_unit in booking_engine_all_units:
			booking_engine_unit.price_sheet_id = price_sheet_id
			booking_engine_unit.save()

		return "SUCCESS"
	except Exception as e:
		print '%s %s (%s)' % ('update_price_sheet_for_project Error',e.message, type(e))
		return "FAILURE"

def test_token(request):
	if request.method == 'POST':
		data = {'test1': 49,'test2': 'awesome',}
		return JsonResponse(data)
	else:
		return JsonError("Only POST is allowed")

@login_required
def builder_contact(request):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		projects = booking_engine_projects.objects.all()
	except booking_engine_projects.DoesNotExist:
		projects = None

	return render_to_response("builder_contact.html", 
									locals(), 
									context_instance = RequestContext(request))

@login_required
@csrf_exempt
def project_builder_contact(request, project_id):
	if 'user_role' not in request.session:
		user_detail = booking_engine_users.objects.get(user_id=request.user.id)
		request.session['user_role'] = user_detail.role
	user_role = request.session['user_role']
	if(user_role != 'Admin' and user_role != 'Project Team'):
		return redirect("/access_error")
	try:
		project = booking_engine_projects.objects.get(project_id=project_id)
	except booking_engine_projects.DoesNotExist:
		project = None

	try:
		project_contact_info = booking_engine_project_contacts.objects.filter(project_id=project_id).order_by('id')
	except booking_engine_project_contacts.DoesNotExist:
		project_contact_info = None

	try:
		if request.method == 'POST':
			if 'builder_contact_create' in request.POST:
				builder_contact = booking_engine_project_contacts()
				builder_contact.contact_id = id_generator()
				builder_contact.contact_name = request.POST['builder_contact_name']
				builder_contact.contact_phone = request.POST['builder_contact_phone']
				builder_contact.contact_email = request.POST['builder_contact_email']
				builder_contact.contact_designation = request.POST['builder_contact_designation'];
				builder_contact.project_id = project_id
				builder_contact.is_primary = int(request.POST['is_primary'])
				builder_contact.save()
				messages.add_message(request, messages.SUCCESS, 'Contact has been created successfully.')
			if 'builder_contact_edit' in request.POST:
				builder_contact = booking_engine_project_contacts.objects.get(contact_id=request.POST['contact_id'])
				builder_contact.contact_name = request.POST['builder_contact_name']
				builder_contact.contact_phone = request.POST['builder_contact_phone']
				builder_contact.contact_email = request.POST['builder_contact_email']
				builder_contact.contact_designation = request.POST['builder_contact_designation'];
				builder_contact.is_primary = int(request.POST['is_primary'])
				builder_contact.save()
				messages.add_message(request, messages.SUCCESS, 'Contact has been edited successfully.')
			if 'building_contact_delete' in request.POST:
				builder_contact = booking_engine_project_contacts.objects.get(contact_id=request.POST['contact_id'])
				builder_contact.delete()
				messages.add_message(request, messages.SUCCESS, 'Contact has been deleted successfully.')
	except Exception as e:
		messages.add_message(request, messages.ERROR, 'Some problem happened.')
		print e.message

	return render_to_response("project_builder_contact.html",
									locals(), 
									context_instance = RequestContext(request))

@login_required
def get_project_units(request):
	try:
		if request.method == 'GET':
			project_id = request.GET['project_id']
			units = booking_engine_units.objects.filter(project_id=project_id)

			if(request.GET['project_type_id']!="0"):
				units = units.filter(project_type_id = request.GET['project_type_id'])
			if(request.GET['tower_id']!="0"):
				units = units.filter(tower_id = request.GET['tower_id'])
			if(request.GET['unit_variant_id']!="0"):
				units = units.filter(unit_variant_id = request.GET['unit_variant_id'])

			project_units = {}
			index = 0;
			for unit in units:
				index = index + 1;
				project_unit = {}
				project_unit['unit_id'] = unit.unit_id
				project_unit['unit_name'] = unit.unit_name
				project_units[index] = project_unit
			return HttpResponse(json.dumps(project_units))
	except Exception as e:
		return None

@login_required
def get_project_plan_units(request):
	try:
		if request.method == 'GET':
			project_id = request.GET['project_id']
			units = booking_engine_units.objects.filter(project_id=project_id)
			pricesheets = booking_engine_pricesheet.objects.filter(project_id=project_id)

			if(request.GET['project_type_id']!="0"):
				units = units.filter(project_type_id = request.GET['project_type_id'])
			if(request.GET['tower_id']!="0"):
				units = units.filter(tower_id = request.GET['tower_id'])
			if(request.GET['unit_variant_id']!="0"):
				units = units.filter(unit_variant_id = request.GET['unit_variant_id'])

			project_units_price_sheets = {}

			project_units = {}
			index = 0;
			for unit in units:
				index = index + 1;
				project_unit = {}
				project_unit['unit_id'] = unit.unit_id
				project_unit['unit_name'] = unit.unit_name
				project_units[index] = project_unit

			project_units_price_sheets['project_units'] = project_units

			price_sheets = {}
			index = 0;
			for price_sheet in pricesheets:
				index = index + 1;
				project_price_sheet = {}
				project_price_sheet['price_sheet_id'] = price_sheet.pricesheet_id
				project_price_sheet['price_sheet_name'] = price_sheet.name
				price_sheets[index] = project_price_sheet

			project_units_price_sheets['price_sheets'] = price_sheets			
			return HttpResponse(json.dumps(project_units_price_sheets))
	except Exception as e:
		return None