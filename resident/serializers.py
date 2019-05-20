from django.core.validators import validate_email as vald_email
from django.core.exceptions import ValidationError
from rest_framework import serializers
from resident.models import Resident



class ResidentSerializer(serializers.ModelSerializer):

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

    def get_name(self, model):
        print(model)
        return model.get_full_name

    def get_location(self, model):
        return model.get_location


class StateSerializer(serializers.Serializer):
    name = serializers.CharField()

class CountrySerializer(serializers.Serializer):
    name = serializers.CharField()

class CitySerializer(serializers.Serializer):
    name = serializers.CharField()
