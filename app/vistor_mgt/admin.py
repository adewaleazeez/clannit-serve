from django.contrib import admin
from .models import NewVistor


class NewVistorAdmin(admin.ModelAdmin):
    list_display = ['vistor_first_name','vistor_last_name','vistor_mobile_number',
                    'whom_to_see','vistor_unique_code','unique_code_is_active','date_created','checked_in','checked_out','checked_in_date','checked_out_date']


admin.site.register(NewVistor,NewVistorAdmin)
