"""ethshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *

app_name = 'site_mgt'

urlpatterns = [
    path('', home, name='home'),
    path('redirect_user', redirect_user, name='redirect_user'),
    path('estate_manager_dashboard', estate_manager_dashboard, name='estate_manager_dashboard'),
    path('resident_dashboard', tenant_dashboard, name='tenant_dashboard'),
    path('security_dashboard', security_dashboard, name='security_dashboard'),
    path('estate_members', estate_members, name='estate_members'),
    path('visitor_log', visitor_log, name='visitor_log'),
    path('add_member', add_member, name='add_member'),
    path('estate_visitors_log', estate_visitor_log, name='estate_visitor_log'),
    path('profile', profile, name='profile'),
    path('my_buildings', my_buildings, name='my_buildings'),
    path('my_estates', my_estates, name='my_estates'),
    path('my_streets', my_streets, name='my_streets'),
    path('my_apartments', my_apartments, name='my_apartments'),
    path('update_estate/<pk>/edit/', estate_edit, name='update_estate'),
    path('my_estates/<pk>/delete/', delete_estate, name='delete_estate'),
    path('update_street/<pk>/edit/', street_edit, name='update_street'),
    path('update_resident/<pk>/edit/', resident_edit, name='update_resident'),
    path('my_streets/<pk>/delete/', delete_street, name='delete_street'),
    path('update_building/<pk>/edit/', building_edit, name='update_building'),
    path('my_buildings/<pk>/delete/', delete_building, name='delete_building'),
    path('update_apartment/<pk>/edit/', apartment_edit, name='update_apartment'),
    path('my_apartments/<pk>/delete/', delete_apartment, name='delete_apartment'),
    path('estate_members/<pk>/delete/', delete_resident, name='delete_resident'),
    path('add_estate_manager', add_estate_manager, name='add_estate_manager'),
    path('get_details/', get_details, name='get_details'),
    path('get_details_apartment/', get_details_apartment, name='get_details_apartment'),
    path('profile_status/', profile_status, name='profile_status'),
    path('add_street/', add_street, name='add_street'),
    path('get_all_streets/', get_all_streets, name='get_all_streets'),
    path('add_building/', add_building, name='add_building'),
    path('add_apartment/', add_apartment, name='add_apartment'),
    path('userEstateReg/', userEstateReg, name='userEstateReg'),
    path('get_details_build/', get_details_build, name='get_details_build'),
    path('add_residents/', add_residents, name='add_residents'),
    # path('street_dashboard/', street_dashboard, name='street_dashboard'),
    # path('building_dashboard/', building_dashboard, name='building_dashboard'),
    # path('apartment_dashboard/', apartment_dashboard, name='apartment_dashboard'),
    path('salutation/', salutation, name='salutation'),
]
