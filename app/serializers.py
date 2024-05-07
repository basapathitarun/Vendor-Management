from rest_framework import serializers
from .models import vendor,purchaseOrder,Performance

from django.contrib.auth.models import  User

class RegisterSerilizer(serializers.Serializer):

    """RegisterSerilizer"""
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """Validation"""
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username is taken')
        return data

    def create(self, validated_data):
        """create User"""
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.Serializer):

    """LoginSerializer"""
    username = serializers.CharField()
    password = serializers.CharField()

class VendorSerializers(serializers.ModelSerializer):

    """VendorSerializers"""
    class Meta:
        model = vendor
        fields = '__all__'    """Return all elements of Tabel"""

class PurchaseOrderSerializers(serializers.ModelSerializer):

    """PurchaseOrderSerializers"""
    class Meta:
        model =  purchaseOrder
        fields = '__all__'       """Return all elements of Tabel"""


class PerformanceSerializers(serializers.ModelSerializer):

    """PerformanceSerializers"""
    class Meta:
        model = Performance
        fields = ['on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']