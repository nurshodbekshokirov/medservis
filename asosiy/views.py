from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login,logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from rest_framework import status,filters
from rest_framework.viewsets import ModelViewSet


class EMLASHMODELVIEW(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Emlama.objects.all()
    serializer_class = EMlamaSerializers

class MIjozMODELVIEW(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Mijoz.objects.all()
    serializer_class = MIJOZSERIALIZERS
    http_method_names = ['get', 'put', 'patch']
    filter_backends = [filters.SearchFilter]
    search_fields = ['jsshir']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Mijoz.objects.all()
        return Mijoz.objects.filter(user=user)


class RegisterAPIView(APIView):
    # Agar siz APIView'da autentifikatsiya va ruxsatlarni ham tekshirmoqchi bo'lsangiz,
    # quyidagi satrlarni qo'shishingiz mumkin. Lekin asosan tekshiruvni `post` metodida amalga oshiramiz.
    permission_classes = [IsAdminUser]  # Faqat admin foydalanuvchilarga ruxsat berish

    def post(self, request, *args, **kwargs):
        # Foydalanuvchi superuser ekanligini tekshirish
        if not request.user.is_superuser:
            return Response({'xabar': 'Faqat superuserlar ro\'yxatdan o\'ta oladi.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = MIJOZSERIALIZERS(data=request.data)
        if serializer.is_valid():
            mijoz = serializer.save()
            # Foydalanuvchi uchun JWT tokenlarini yaratish
            refresh = RefreshToken.for_user(mijoz.user)
            tokenlar = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            # Mijoz ma'lumotlari va tokenlarni qaytarish
            data = {
                'mijoz': MIJOZSERIALIZERS(mijoz).data,
                'tokenlar': tokenlar,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'xabar': "Tizimga kiritildi"
            }, status=status.HTTP_200_OK)
        else:
            return Response({"xabar": "Login yoki parol noto'g'ri"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutApiview(APIView):
    def get(self,request):
        logout(request)
        return Response({"xabar":"Tizimdan chiqarildi"})
# Create your views here.
