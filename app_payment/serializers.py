from app_payment.models import PayUserModel
from rest_framework import serializers


class PayUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayUserModel
        fields = ["number"]
