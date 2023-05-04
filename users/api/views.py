from django.shortcuts import render
from rest_framework import generics, status
from users.api.serializers import Address, CustomUser
from users.api.serializers import AddressSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from ..tokens import create_jwt_pair_for_user
from rest_framework.views import APIView
from django.contrib.auth import authenticate





class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class AddressDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.user
        id = self.kwargs['id']
        address_object = get_object_or_404(queryset , id = id )
        if address_object.user != user :
            self.permission_denied(self.request)
            
        return address_object
        

class Registeration(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes=[AllowAny]
    
    def post(self,request:Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response={
                "message":"user created Successfully",
                "data":serializer.data
            }
            return Response(data=response , status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request:Request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email , password = password)
        
        if user is not None :
            tokens = create_jwt_pair_for_user(user)
            response = {
                'message':'Login Successfully',
                'tokens': tokens
            }
            
            return Response(data =response , status=status.HTTP_200_OK)
        
        else :
            return Response(data= {
                'message':'Invalid Email or Password'
            })
            
    
    def get(self,request:Request):
        content = {'user':str(request.user),
                   'auth':str(request.auth)}
        
        return Response(data=content , status=status.HTTP_200_OK)