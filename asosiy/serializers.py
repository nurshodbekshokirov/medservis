from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from rest_framework import serializers
from .models import Mijoz


class MIJOZSERIALIZERS(serializers.ModelSerializer):
    emlamalar = serializers.SerializerMethodField()

    class Meta:
        model = Mijoz
        fields = ['ism', 'fam', 'jsshir', 'manzil', 'tel', 'user', 'emlamalar']

    def get_emlamalar(self, obj):
        # Mijozga tegishli barcha Emlama ma'lumotlarini olish
        emlamalar = Emlama.objects.filter(mijoz=obj)
        # Emlama ma'lumotlarini serializatsiya qilish
        serializer = EMlamaSerializers(emlamalar, many=True)
        return serializer.data

    def create(self, validated_data):
        # Foydalanuvchi uchun avtomatik parol yaratish
        random_password = get_random_string(length=10)

        # Foydalanuvchi yaratish
        user = User.objects.create_user(username=validated_data['jsshir'],
                                        password=random_password)

        # Mijoz objektini yaratish va qaytarish
        mijoz = Mijoz.objects.create(user=user, **validated_data)
        return mijoz


class EMlamaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Emlama
        fields = "__all__"

