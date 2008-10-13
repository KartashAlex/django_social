from django.contrib import admin

from models import Country, City

class CountryAdmin(admin.ModelAdmin):
    search_fields = ['translations__name']
    list_display = ['name_ru', 'name_ar', 'name_en']
admin.site.register(Country, CountryAdmin)

class CityAdmin(admin.ModelAdmin):
    search_fields = ['translations__name']
    list_display = ['name_ru', 'name_ar', 'name_en']
admin.site.register(City, CityAdmin)
