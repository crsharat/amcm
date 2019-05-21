from django.contrib import admin
from resident.models import Resident, City


class ResidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'phone_number', 'mobile_number', 'state', 'country')
    search_fields = ['id', 'first_name', 'email']

class CityAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'state', 'country')
	search_fields = ['name', 'id']

	def country(self, model):
		return model.state.country.name

admin.site.register(Resident, ResidentAdmin)
admin.site.register(City, CityAdmin)