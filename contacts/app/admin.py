from django.contrib import admin

#for removing authentications and authorizations
from django.contrib.auth.models import Group
# Register your models here.

#we import the Contact models that we wrote so.
from .models import Contact, Car


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','sl_no' ,'number_plate','avalibility','info' ) #we can add 'date_added'
    list_display_links = ('id' ,)
    list_editable = ('info','avalibility','number_plate')
    list_per_page = 10
    search_fields = ('number_plate','avalibility')
    list_filter = ('number_plate','avalibility')

class CarAdmin(admin.ModelAdmin):
    list_display = ('id' , 'number_plate', 'entry_time', 'status' ,'sl_no','service_used','name' ,'phone', 'email' ) #we can add 'date_added'
    list_display_links = ('id',)
    list_editable = ('number_plate','service_used','status','sl_no','name' ,'phone', 'email')
    list_per_page = 10
    search_fields = ('id' , 'number_plate')
    list_filter = ('id' , 'number_plate')

admin.site.register(Contact,ContactAdmin)
admin.site.register(Car,CarAdmin)

admin.site.unregister(Group)
