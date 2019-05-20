from resident import views
from django.conf.urls import url
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'api/v1/resident', views.ResidentAPI)
router.register(r'api/v1/state', views.StateAPI)
router.register(r'api/v1/city', views.CityAPI)
router.register(r'api/v1/country', views.CountryAPI)

urlpatterns = [
        url(r'^$', views.HomePageView.as_view(), name='home'),
        url(r'^residents/$', views.ResidentListPage.as_view(), name='show_residents'),
        url(r'^add/resident/$', views.AddResidentPage.as_view(), name='add_resident')
] + router.urls
