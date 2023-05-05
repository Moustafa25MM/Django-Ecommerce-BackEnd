from rest_framework import serializers
from users.models import CustomUser , Address
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = '__all__'
        
    

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email' , 'username' , 'password' , 'confirm_password' , 'image' ,'phone' ,'date_of_birth']
        extra_kwargs = {
            'password':{'write_only':True},
            'confirm_password':{'write_only':True},
        }
    
    def create(self, validated_data):
        
        validated_data['is_active'] = True
        return CustomUser.objects.create_user(**validated_data)
        
    def validate(self,data):
        if CustomUser.objects.filter(email=data['email']).exists():
            raise ValidationError('This email is already exists!')
        
        if 'phone' not in data:
            # Handle missing phone number
            raise serializers.ValidationError('Phone number is required.')
        
        if CustomUser.objects.filter(phone=data['phone']).exists():
            raise serializers.ValidationError('Phone number already exists.')
        
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords don't match")
        
        return data    