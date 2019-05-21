from django.views.generic import TemplateView
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from resident.models import Resident, State, Country, City, Flat, PaymentMethod
from resident.serializers import (ResidentSerializer, ResidentDetailSerializer, StateSerializer,
								  CountrySerializer, CitySerializer, FlatSerializer, PaymentMethodSerializer)
from resident.persmissions import IsStaff


class QuietBasicAuthentication(BasicAuthentication):
    def authenticate_header(self, request):
        return 'xBasic realm="%s"' % self.www_authenticate_realm

class LoginAPI(APIView):
    authentication_classes = (QuietBasicAuthentication,)

    def get(self, request):
        redirect_uri = request.build_absolute_uri(f'/accounts/google/login/?next={request.GET.get("next","/")}')
        return redirect(redirect_uri)

    def post(self, request):
        details = request.data
        user = authenticate(username=details['username'], password=details['password'])
        if user is not None:
            login(request, user)
            return redirect(reverse("home_page"))
        else:
            return Response({'success': False, 'message': 'Authentication failed.'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        """
        Logout a session.

        """
        logout(request)
        return Response({'success': True, 'message': 'User logged out.'})


class ResidentAPI(viewsets.ModelViewSet):
	authentication_class = (SessionAuthentication, TokenAuthentication)
	queryset = Resident.objects.order_by('-id')
	http_methods = ['get', 'patch', 'post']

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		page = self.paginate_queryset(queryset)
		if page is not None:
		    serializer = self.get_serializer(page, many=True)
		    return self.get_paginated_response(serializer.data)

	def get_all(self, request, *args, **kwargs):
		data = Resident.objects.filter(flat__isnull=True).order_by('-id')\
							   .annotate(full_name=Concat('first_name', Value(' '), 'last_name'))\
							   .values("id", "full_name")
		return Response(data)

	def get_serializer_class(self):
		if self.action in ["retrieve", "list"]:
			return ResidentDetailSerializer
		elif self.action in ["partial_update", "create", "update"]:
			return ResidentSerializer


class StateAPI(viewsets.ModelViewSet):
	authentication_class = (SessionAuthentication, TokenAuthentication)
	permissions_class = IsStaff
	queryset = State.objects.order_by('name')
	http_methods = ['get']
	serializer_class = StateSerializer


class CountryAPI(viewsets.ModelViewSet):
	authentication_class = (SessionAuthentication, TokenAuthentication)
	queryset = Country.objects.order_by('name')
	http_methods = ['get']
	serializer_class = CountrySerializer


class CityAPI(viewsets.ModelViewSet):
	authentication_class = (SessionAuthentication, TokenAuthentication)
	queryset = City.objects.order_by('name')
	http_methods = ['get']
	serializer_class = CitySerializer
	pagination_class = None


class FlatAPI(viewsets.ModelViewSet):
	authentication_class = (SessionAuthentication, TokenAuthentication)
	queryset = Flat.objects.order_by('number')
	http_methods = ['get', 'post', 'patch']
	serializer_class = FlatSerializer

	def get_all(self, request, *args, **kwargs):
		queryset = Flat.objects.values('id', 'number')
		return Response(queryset)

class PaymentAPI(viewsets.ModelViewSet):
	authentication_class = (SessionAuthentication, TokenAuthentication)
	queryset = PaymentMethod.objects.order_by('-id')
	http_methods = ['get', 'post']
	serializer_class = PaymentMethodSerializer


class HomePageView(TemplateView):
    template_name = "index.html"


class ResidentListPage(TemplateView):
	template_name = "list_residents.html"


class AddResidentPage(TemplateView):
	template_name = "add_resident.html"


class AddFlatPage(TemplateView):
	template_name = 'add_flat.html'


class FlatListPage(TemplateView):
	template_name = "list_flats.html"


class AcceptPayment(TemplateView):
	template_name = "add_payment.html"


class PaymentHistory(TemplateView):
	template_name = "payment_history.html"


class LoginPage(TemplateView):
	template_name = "login.html"