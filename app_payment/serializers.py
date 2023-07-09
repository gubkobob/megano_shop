from rest_framework import serializers

from app_payment.models import PayUserModel


class PayUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayUserModel
        fields = ['number']