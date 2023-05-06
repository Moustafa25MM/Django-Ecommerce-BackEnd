from django.urls import path
from users.api.views import Registeration , LoginView , getUserProfile ,UserDetail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register/', Registeration.as_view(), name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/',getUserProfile,name='profile'),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path('', UserDetail.as_view(), name='user_detail'),
    path('<int:userId>/addresses/<int:addressId>', UserDetail.as_view(), name='user_detail'),

]
