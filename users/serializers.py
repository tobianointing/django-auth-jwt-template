from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import validate_phone_number


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    business_name = serializers.CharField(required=True)
    business_type = serializers.CharField(required=True)

    def validate_phone(self, phone):
        users = get_user_model()
        if users.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("Phone already exists")
        if not validate_phone_number(phone):
            raise serializers.ValidationError("Invalid phone number")

        return phone

    def validate_business_type(self, business_type):
        if business_type not in ["registered", "starter"]:
            raise serializers.ValidationError("Invalid business type")

        return business_type

    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get("first_name")
        user.last_name = self.data.get("last_name")
        user.phone = self.data.get("phone")
        user.business_name = self.data.get("business_name")
        user.business_type = self.data.get("business_type")
        user.save()

        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone",
            "business_name",
            "business_type",
        )
        read_only_fields = ("email",)
