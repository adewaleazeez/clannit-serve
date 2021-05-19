from django.contrib import admin
from .models import *

# Register your models here.
class EstateDetailAdmin(admin.ModelAdmin):
    list_display = ['estate_name','estate_address','estate_logo']

admin.site.register(EstateDetail,EstateDetailAdmin)

