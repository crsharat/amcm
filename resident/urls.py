from resident import views
from django.conf.urls import url
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'api/v1/resident', views.ResidentAPI)
router.register(r'api/v1/state', views.StateAPI)
router.register(r'api/v1/city', views.CityAPI)
router.register(r'api/v1/country', views.CountryAPI)
router.register(r'api/v1/flat', views.FlatAPI)
router.register(r'api/v1/payment', views.PaymentAPI)

urlpatterns = [
        url(r'^$', views.HomePageView.as_view(), name='home_page'),
        url(r'^api/v1/login/$', views.LoginAPI.as_view(), name='login_api'),
        url(r'^login/$', views.LoginPage.as_view(), name='login'),
        url(r'^api/v1/resident/all/$', views.ResidentAPI.as_view({"get": "get_all"}), name="all_residents"),
        url(r'^api/v1/flat/all/$', views.FlatAPI.as_view({"get": "get_all"}), name="all_flats"),
        url(r'^residents/$', views.ResidentListPage.as_view(), name='list_residents'),
        url(r'^add/resident/$', views.AddResidentPage.as_view(), name='add_resident'),
        url(r'^add/flat/$', views.AddFlatPage.as_view(), name='add_flat'),
        url(r'^flats/', views.FlatListPage.as_view(), name='list_flats'),
        url(r'^add/payment/', views.AcceptPayment.as_view(), name='add_payment'),
        url(r'^payment/history/', views.PaymentHistory.as_view(), name='payment_history'),

] + router.urls
