from django.contrib import admin
from .models import *

# Register your models here.
class GFGAdmin(admin.ModelAdmin):
    list_display = ['hotel_name', 'hotel_price', 'hotel_description']

admin.site.register(GFG, GFGAdmin)