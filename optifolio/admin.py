from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)
admin.site.register(VisData)
admin.site.register(Portfolio)
