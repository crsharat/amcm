from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from resident.models import Resident, State, Country, City
from resident.serializers import ResidentSerializer, ResidentDetailSerializer, StateSerializer, CountrySerializer, CitySerializer
from resident.persmissions import IsStaff


class ResidentAPI(viewsets.ModelViewSet):
	authentication_class = (SessionAuthentication, TokenAuthentication)
	permission_class = IsStaff
	queryset = Resident.objects.order_by('-id')
	http_methods = ['get', 'patch', 'post']

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		page = self.paginate_queryset(queryset)
		if page is not None:
		    serializer = self.get_serializer(page, many=True)
		    return self.get_paginated_response(serializer.data)

	def get_serializer_class(self):
		if self.action in ["retrieve", "list"]:
			return ResidentDetailSerializer
		elif self.action in ["partial_update", "create", "update"]:
			return ResidentSerializer

class StateAPI(viewsets.ModelViewSet):
	authentication_class = (SessionAuthentication, TokenAuthentication)
	persmissions_class = IsStaff
	queryset = State.objects.order_by('name')
	http_methods = ['get']
	serializer_class = StateSerializer


class CountryAPI(viewsets.ModelViewSet):
	authentication_class = (SessionAuthentication, TokenAuthentication)
	persmissions_class = IsStaff
	queryset = Country.objects.order_by('name')
	http_methods = ['get']
	serializer_class = CountrySerializer


class CityAPI(viewsets.ModelViewSet):
	authentication_class = (SessionAuthentication, TokenAuthentication)
	persmissions_class = IsStaff
	queryset = City.objects.order_by('name')
	http_methods = ['get']
	serializer_class = CitySerializer


class HomePageView(TemplateView):
    template_name = "index.html"


class ResidentListPage(TemplateView):
	template_name = "list_residents.html"


class AddResidentPage(TemplateView):
	template_name = "add_resident.html"
