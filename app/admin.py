from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(vendor)
admin.site.register(purchaseOrder)
admin.site.register(Performance)