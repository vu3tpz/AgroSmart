from django.contrib import admin
from .models import *

# Register your models here.

class VisitorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Visitor, VisitorAdmin)

class OfficerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Officer, OfficerAdmin)

class AdminAdmin(admin.ModelAdmin):
    pass
admin.site.register(Admin, AdminAdmin)

class SellerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Seller, SellerAdmin)

admin.site.register(District)
admin.site.register(Region)
admin.site.register(Soil)
admin.site.register(SoilLocationDetail)
admin.site.register(SoilDetail)
admin.site.register(RainfallDetail)
admin.site.register(Year)
admin.site.register(Crop)
admin.site.register(RequestSeed)
admin.site.register(RequestFertilizer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Pay)