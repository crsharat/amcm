from django.core.validators import validate_email as vald_email
from django.core.exceptions import ValidationError
from rest_framework import serializers
from resident.models import Resident, Flat, PaymentMethod


class ResidentSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(read_only=True)
    state_name = serializers.CharField(read_only=True)
    country_name = serializers.CharField(read_only=True)
    dob = serializers.DateField(format="%d/%m/%Y", input_formats=["%Y-%m-%d"])

    def vaidate_email(self, value):
        try:
            vald_email(value)
            return True
        except ValidationError:
            return False

    class Meta:
        model = Resident
        exclude = ('password', 'last_login' )


class ResidentDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField(required=False)
    username = serializers.CharField()
    email = serializers.CharField()
    mobile_number = serializers.CharField()
    phone_number = serializers.CharField()
    location = serializers.SerializerMethodField(required=False)
    dob = serializers.DateField()
    active = serializers.BooleanField()
    owner = serializers.BooleanField()
    flat = serializers.SerializerMethodField()

    def get_flat(self, model):
        return None

    def get_name(self, model):
        return model.get_full_name

    def get_location(self, model):
        return model.get_location


class StateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class FlatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flat
        fields = '__all__'
        extra_kwargs = {
                    'amount': {'max_digits': 16, 'decimal_places': 2}
        }


class PaymentMethodSerializer(serializers.ModelSerializer):
    receipt_number = serializers.CharField(read_only=True)
    resident_name = serializers.SerializerMethodField(read_only=True)

    def get_resident_name(self, model):
        return model.flat.resident.get_full_name

    class Meta:
        model = PaymentMethod
        fields = '__all__'
