from django.contrib import admin
from .models import *
# Register your models here.


class EstateAdmin(admin.ModelAdmin):
    list_display = ['estate_id','estate_name','estate_address','date_created']


class StreetAdmin(admin.ModelAdmin):
    list_display = ['street_id', 'estate', 'street_name', 'date_created']


class BuildingAdmin(admin.ModelAdmin):
    list_display = ['building_id', 'building_number', 'street', 'building_type', 'date_created']


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['apartment_id', 'building_id', 'apartment_number', 'date_created']


class SalutationAdmin(admin.ModelAdmin):
    list_display = ['title_id', 'title_name', 'date_created']


admin.site.register(Estate, EstateAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Salutation, SalutationAdmin)
