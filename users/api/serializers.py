from rest_framework import serializers
from users.models import CustomUser , Address
from django.core.exceptions import ValidationError

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = '__all__'
        
    

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email' , 'username' , 'password' , 'confim_password','image' , 'date_of_birth']
        extra_kwargs = {
            'password':{'write_only':True},
            'confirm_password':{'write_only':True},
        }
        
    def create(self, validated_data):
        validated_data.pop('groups')
        validated_data.pop('user_permissions')
        validated_data['is_active'] = True
        return CustomUser.objects.create_user(**validated_data)
    
    def validate(self,data):
        if CustomUser.objects.filter(email=data['email']).exists():
            raise ValidationError('This email is already exists!')
        
        if CustomUser.objects.filter(phone=data['phone']).exists():
            raise ValidationError('This is phone is already registered!')
        
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords don't match")
        
        return data    