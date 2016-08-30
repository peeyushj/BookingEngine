from django.db import models

# Create your models here.

class booking_engine_users(models.Model):
	user_id = models.CharField(max_length=50, null=True)
	role = models.CharField(max_length=100, null=True)
	create_date = models.CharField(max_length=100, null=True)
	
	class Meta:
		db_table = "booking_engine_users"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_buyers(models.Model):
	buyer_id = models.CharField(max_length=50)
	buyer_name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	pan_card_number = models.CharField(max_length=100)
	buyer_type = models.CharField(max_length=100)
	address_line_1 = models.CharField(max_length=300)
	address_line_2 = models.CharField(max_length=300)
	city = models.CharField(max_length=300)
	state = models.CharField(max_length=300)
	country = models.CharField(max_length=300)
	pincode = models.CharField(max_length=300)

	class Meta:
		db_table = "booking_engine_buyers"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_projects(models.Model):
	project_id = models.CharField(max_length=50)
	project_name = models.CharField(max_length=100)
	project_type = models.CharField(max_length=100, null=True)
	builder_name = models.CharField(max_length=100, null=True)
	project_area = models.CharField(max_length=100, null=True)
	project_city = models.CharField(max_length=100, null=True)
	default_payment_plan_id = models.CharField(max_length=50, null=True)
	default_price_sheet_id = models.CharField(max_length=50, null=True)

	class Meta:
		db_table = "booking_engine_projects"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_project_contacts(models.Model):
	contact_id = models.CharField(max_length=50)
	contact_name = models.CharField(max_length=100)
	contact_phone = models.CharField(max_length=100)
	contact_email = models.CharField(max_length=100)
	contact_designation = models.CharField(max_length=100)
	is_primary = models.BooleanField(max_length=100, default=True)
	project_id = models.CharField(max_length=100)

	class Meta:
		db_table = "booking_engine_project_contacts"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_towers(models.Model):
	tower_id = models.CharField(max_length=50)
	project_id = models.CharField(max_length=50)
	tower_name = models.CharField(max_length=100)
	no_of_floors = models.CharField(max_length=100)
	total_units = models.CharField(max_length=100)
	total_units_in_floor = models.CharField(max_length=100)

	class Meta:
		db_table = "booking_engine_towers"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_unit_variants(models.Model):
	unit_variant_id = models.CharField(max_length=50)
	project_id = models.CharField(max_length=50)
	unit_variant_name = models.CharField(max_length=100)

	class Meta:
		db_table = "booking_engine_unit_variants"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_brokers(models.Model):
	broker_id = models.CharField(max_length=50)
	broker_name = models.CharField(max_length=100)

	class Meta:
		db_table = "booking_engine_brokers"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_project_types(models.Model):
	project_type_id = models.CharField(max_length=50)
	project_type_name = models.CharField(max_length=100)

	class Meta:
		db_table = "booking_engine_project_types"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_units(models.Model):
	unit_id = models.CharField(max_length=50)
	unit_name = models.CharField(max_length=100, null=True)
	project_id = models.CharField(max_length=50)
	booking_amount = models.CharField(max_length=100)
	total_sale_value = models.CharField(max_length=100, null=True)
	payment_plan_id = models.CharField(max_length=100, null=True)
	price_sheet_id = models.CharField(max_length=100, null=True)
	project_type_id = models.CharField(max_length=100, null=True)
	tower_id = models.CharField(max_length=100, null=True)
	unit_variant_id = models.CharField(max_length=100, null=True)

	class Meta:
		db_table = "booking_engine_units"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_bookings(models.Model):
	booking_id = models.CharField(max_length=50)
	buyer_id = models.CharField(max_length=50)
	unit_id = models.CharField(max_length=50)
	status = models.CharField(max_length=100)
	price_sheet_id = models.CharField(max_length=50, null=True)
	payment_plan_id = models.CharField(max_length=50, null=True)
	booking_date = models.CharField(max_length=100, null=True)

	class Meta:
		db_table = "booking_engine_bookings"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_booking_history(models.Model):
	booking_history_id = models.CharField(max_length=50)
	booking_id = models.CharField(max_length=50)
	old_status = models.CharField(max_length=100)
	new_status = models.CharField(max_length=100)
	comments = models.CharField(max_length=50)
	updated_on = models.DateTimeField()
	updated_by = models.CharField(max_length=100)

	class Meta:
		db_table = "booking_engine_booking_history"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_payment_history(models.Model):
	payment_id = models.CharField(max_length=50)
	booking_id = models.CharField(max_length=50)
	mihpayid = models.CharField(max_length=50, null=True)
	payment_status = models.CharField(max_length=100)
	is_active = models.BooleanField(max_length=100, default=True)
	updated_on = models.DateTimeField(null=True)

	class Meta:
		db_table = "booking_engine_payment_history"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_project_payment_plan(models.Model):
	project_payment_plan_id = models.CharField(max_length=50)
	payment_plan_id = models.CharField(max_length=50)
	project_id = models.CharField(max_length=100)
	broker_id = models.CharField(max_length=100)

	class Meta:
		db_table = "booking_engine_project_payment_plan"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_payment_plan(models.Model):
	payment_plan_id = models.CharField(max_length=50)
	payment_plan_name = models.CharField(max_length=100, null=True)
	payment_plan_description = models.CharField(max_length=100, null=True)
	project_type_id = models.CharField(max_length=50, null=True, default=0)
	tower_id = models.CharField(max_length=50, null=True, default=0)
	unit_variant_id = models.CharField(max_length=50, null=True, default=0)
	broker_id = models.CharField(max_length=50, null=True, default=0)
	as_of_date = models.DateField(max_length=100)
	is_active = models.BooleanField(default=True)
	project_id = models.CharField(max_length=50, null=True)
	is_default = models.BooleanField(default=False)

	class Meta:
		db_table = "booking_engine_payment_plan"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_payment_plan_milestones(models.Model):
	payment_plan_milestone_id = models.CharField(max_length=50)
	payment_plan_id = models.CharField(max_length=50)
	milestone = models.CharField(max_length=100)
	milestone_free_text = models.CharField(max_length=100)
	milestone_date = models.DateField(null=True, blank=True)
	cost_type = models.CharField(max_length=100)
	amount = models.CharField(max_length=100)
	formula = models.CharField(max_length=100)

	class Meta:
		db_table = "booking_engine_payment_plan_milestones"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_project_pricesheet(models.Model):
	project_pricesheet_id = models.CharField(max_length=50)
	project_id = models.CharField(max_length=50)
	pricesheet_id = models.CharField(max_length=50)
	broker_id = models.CharField(max_length=100)
	is_active = models.CharField(max_length=100)

	class Meta:
		db_table = "booking_engine_project_pricesheet"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_pricesheet(models.Model):
	pricesheet_id = models.CharField(max_length=50)
	as_of_date = models.DateField(max_length=100)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=300, null=True)
	project_id = models.CharField(max_length=6, null=True)
	project_type_id = models.CharField(max_length=50, null=True, default=0)
	tower_id = models.CharField(max_length=50, null=True, default=0)
	unit_variant_id = models.CharField(max_length=50, null=True, default=0)
	broker_id = models.CharField(max_length=50, null=True, default=0)
	is_active = models.BooleanField(default=True)
	is_default = models.BooleanField(default=False)

	class Meta:
		db_table = "booking_engine_pricesheet"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booking_engine_pricesheet_component(models.Model):
	pricesheet_component_id = models.CharField(max_length=50)
	pricesheet_id = models.CharField(max_length=50)
	price_type = models.CharField(max_length=100)
	price_sub_type = models.CharField(max_length=100)
	price_type_free_text = models.CharField(max_length=100)
	price_sub_type_free_text = models.CharField(max_length=100)
	cost_type = models.CharField(max_length=100)
	amount = models.CharField(max_length=100)
	formula = models.CharField(max_length=100)

	class Meta:
		db_table = "booking_engine_pricesheet_component"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booked_pricesheet(models.Model):
	pricesheet_id = models.CharField(max_length=50)
	as_of_date = models.DateField(max_length=100)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=300, null=True)
	project_id = models.CharField(max_length=300, null=True)
	booking_id = models.CharField(max_length=50, null=True)

	class Meta:
		db_table = "booked_pricesheet"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booked_pricesheet_component(models.Model):
	pricesheet_component_id = models.CharField(max_length=50)
	pricesheet_id = models.CharField(max_length=50)
	price_type = models.CharField(max_length=100)
	price_sub_type = models.CharField(max_length=100)
	price_type_free_text = models.CharField(max_length=100)
	price_sub_type_free_text = models.CharField(max_length=100)
	cost_type = models.CharField(max_length=100)
	entered_value = models.CharField(max_length=100, null=True) 
	total_amount = models.CharField(max_length=100)
	formula = models.CharField(max_length=100)
	booking_id = models.CharField(max_length=50, null=True)

	class Meta:
		db_table = "booked_pricesheet_component"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booked_payment_plan(models.Model):
	payment_plan_id = models.CharField(max_length=50)
	payment_plan_name = models.CharField(max_length=100, null=True)
	payment_plan_description = models.CharField(max_length=100, null=True)
	as_of_date = models.DateField(max_length=100)
	project_id = models.CharField(max_length=50, null=True)
	booking_id = models.CharField(max_length=50, null=True)

	class Meta:
		db_table = "booked_payment_plan"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)

class booked_payment_plan_milestones(models.Model):
	payment_plan_milestone_id = models.CharField(max_length=50)
	payment_plan_id = models.CharField(max_length=50)
	milestone = models.CharField(max_length=100)
	milestone_free_text = models.CharField(max_length=100)
	milestone_date = models.DateField(null=True, blank=True)
	cost_type = models.CharField(max_length=100)
	entered_value = models.CharField(max_length=100, null=True) 
	total_amount = models.CharField(max_length=100)
	formula = models.CharField(max_length=100)
	booking_id = models.CharField(max_length=50, null=True)

	class Meta:
		db_table = "booked_payment_plan_milestones"

	def save(self, *args, **kwargs):
		models.Model.save(self, *args, **kwargs)