from django.conf.urls import patterns, include, url
from django.contrib import admin
# from booking_engine.api import WhateverResource

import settings

admin.autodiscover()

# whatever_resource = WhateverResource()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'booking_engine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^api/', include(whatever_resource.urls)),
    (r'', include('tokenapi.urls')),

    url(r'^$', 'booking_engine.views.account_info', name='homepage'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),


    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    
    (r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password/reset/done/'}),
	(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
	(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
	        {'post_reset_redirect' : '/accounts/password/done/'}),
	(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),



    url(r'^register/$', 'booking_engine.views.register', name='register'),
    url(r'^users/$', 'booking_engine.views.users', name='users'),
    url(r'^account_info/$', 'booking_engine.views.account_info', name='account_info'),
    url(r'^bookings/$', 'booking_engine.views.bookings', name='bookings'),
    url(r'^booking-info/(?P<booking_id>\S+)$', 'booking_engine.views.booking_info', name='booking-info'),
    url(r'^buyer-list/$', 'booking_engine.views.buyer_list', name='buyer-list'),

    url(r'^payment_plan/$', 'booking_engine.views.payment_plan', name='payment_plan'),
    url(r'^project_payment_plan/(?P<project_id>\S+)$$', 'booking_engine.views.project_payment_plan', name='project_payment_plan'),
    url(r'^project_payment_plan_edit/(?P<payment_plan_id>\S+)$', 'booking_engine.views.project_payment_plan_edit', name='project_payment_plan_edit'),

    url(r'^pricing_structure/$', 'booking_engine.views.pricing_structure', name='pricing_structure'),
    url(r'^project_pricing_structure/(?P<project_id>\S+)$', 'booking_engine.views.project_pricing_structure', name='project_pricing_structure'),
    url(r'^project_price_sheet_edit/(?P<price_sheet_id>\S+)$', 'booking_engine.views.project_price_sheet_edit', name='project_price_sheet_edit'),

    url(r'^unit_price_sheet/$', 'booking_engine.views.unit_price_sheet', name='unit_price_sheet'),
    url(r'^unit_payment_plan/$', 'booking_engine.views.unit_payment_plan', name='unit_payment_plan'),

    url(r'^unit_project_price_sheet/$', 'booking_engine.views.unit_project_price_sheet', name='unit_project_price_sheet'),
    url(r'^unit_project_payment_plan/$', 'booking_engine.views.unit_project_payment_plan', name='unit_project_payment_plan'),

    url(r'^booked_unit_price_sheet/$', 'booking_engine.views.booked_unit_price_sheet', name='booked_unit_price_sheet'),
    url(r'^booked_unit_payment_plan/$', 'booking_engine.views.booked_unit_payment_plan', name='booked_unit_payment_plan'),

    url(r'^book_payment_structure/$', 'booking_engine.views.book_payment_structure', name='book_payment_structure'),
    url(r'^check_payment_status/$', 'booking_engine.views.check_payment_status', name='check_payment_status'),
    url(r'^refund_payment/$', 'booking_engine.views.refund_payment', name='refund_payment'),
    url(r'^update_payment_status/$', 'booking_engine.views.update_payment_status', name='update_payment_status'),

    url(r'^get_booking_amount/$', 'booking_engine.views.get_booking_amount', name='get_booking_amount'),
    url(r'^get_total_sale_value/$', 'booking_engine.views.get_total_sale_value', name='get_total_sale_value'),

    url(r'^add_project/$', 'booking_engine.views.add_project', name='add_project'),

    url('^getPropertyDetail/$', 'booking_engine.views.getPropertyDetail', name='getPropertyDetail'),
    url('^getAreaDetail/$', 'booking_engine.views.getAreaDetail', name='getAreaDetail'),

    url('^getUnitData/$', 'booking_engine.views.getUnitData', name='getUnitData'),
    url('^addUnit/$', 'booking_engine.views.addUnit', name='addUnit'),
    url('^deleteUnit/$', 'booking_engine.views.deleteUnit', name='deleteUnit'),

    # url('^update_payment_plan_for_project/$', 'booking_engine.views.update_payment_plan_for_project', name='update_payment_plan_for_project'),
    # url('^update_price_sheet_for_project/$', 'booking_engine.views.update_price_sheet_for_project', name='update_price_sheet_for_project'),
    
    url(r'^payments/$', 'booking_engine.views.payments', name='payments'),

    url(r'^test_token/$', 'booking_engine.views.test_token', name='test_token'),
    url(r'^access_error/$', 'booking_engine.views.access_error', name='access_error'),

    url(r'^add_broker/$', 'booking_engine.views.add_broker', name='add_broker'),

    url(r'^towers/$', 'booking_engine.views.towers', name='towers'),
    url(r'^project_towers/(?P<project_id>\S+)$', 'booking_engine.views.project_towers', name='project_towers'),
    url('^getPropertyTowers/$', 'booking_engine.views.getPropertyTowers', name='getPropertyTowers'),

    url(r'^unit_variants/$', 'booking_engine.views.unit_variants', name='unit_variants'),
    url(r'^project_unit_variants/(?P<project_id>\S+)$', 'booking_engine.views.project_unit_variants', name='project_unit_variants'),
    
    url(r'^builder_contact/$', 'booking_engine.views.builder_contact', name='builder_contact'),
    url(r'^project_builder_contact/(?P<project_id>\S+)$', 'booking_engine.views.project_builder_contact', name='project_builder_contact'),
    
    url('^get_project_units/$', 'booking_engine.views.get_project_units', name='get_project_units'),
    url('^get_project_plan_units/$', 'booking_engine.views.get_project_plan_units', name='get_project_plan_units'),
)   

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)

handler404 = 'group_buying.views.handler404'
handler500 = 'group_buying.views.handler500'
