from django.contrib import admin

from models import Country, City

class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(Country, CountryAdmin)

class CityAdmin(admin.ModelAdmin):
    search_fields = ['country__name', 'name']
admin.site.register(City, CityAdmin)
