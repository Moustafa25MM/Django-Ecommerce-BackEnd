from rest_framework import serializers
from users.models import CustomUser , Address
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from django.contrib.auth.hashers import make_password




class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'city', 'country', 'street', 'building_number']
        read_only_fields = ['id']
    
    
    def update(self, instance, validated_data):
        instance.street = validated_data.get('street', instance.street)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.building_number = validated_data.get('building_number', instance.building_number)
        instance.save()
        return instance
    

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['email' , 'username' , 'password' , 'confirm_password' , 'image'  , 'phone' ,'date_of_birth' , 'addresses']
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
            raise serializers.ValidationError('Phone number is required.')
        
        if CustomUser.objects.filter(phone=data['phone']).exists():
            raise serializers.ValidationError('Phone number already exists.')
        
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords don't match")
        
        if len(data['password']) > 16 or len(data['confirm_password']) > 16:
            raise ValidationError("Password should not be more than 16 characters")
        
        return data    
    
    
    def to_representation(self, instance):
        if isinstance(instance, get_user_model()):
            return super().to_representation(instance)
        else:
            # Handle anonymous user
            return {'id': None, 'username': 'Anonymous', 'email': None}
        
        
class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    phone=serializers.CharField(required=False)
    image=CloudinaryField()
    password = serializers.CharField(required=False, write_only=True)
    confirm_password = serializers.CharField(required=False, write_only=True)
    addresses = AddressSerializer(many=True)
    
    class Meta:
        model = CustomUser
        fields = ['email' , 'username' , 'password' , 'confirm_password' , 'image' ,'phone' ,'date_of_birth' , 'addresses']
        extra_kwargs = {
        'password': {'write_only': True},
        'confirm_password': {'write_only': True},
    }

    def validate(self, attrs):
        if not any(attrs.values()):
            raise serializers.ValidationError("At least one field must be updated")

        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password and not confirm_password:
            raise serializers.ValidationError("Please confirm your new password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        if len(password) > 16 or len(confirm_password) > 16:
            raise serializers.ValidationError("Password should not be more than 16 characters")

        return attrs
    
    def update(self, instance, validated_data):
        if 'email' in validated_data:
            instance.email = validated_data['email']
        if 'username' in validated_data:
            instance.username = validated_data['username']
        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])
        if 'confirm_password' in validated_data:
            instance.confirm_password = make_password(validated_data['confirm_password'])
        if 'date_of_birth' in validated_data:
            instance.date_of_birth = validated_data['date_of_birth']
        if 'phone' in validated_data:
            instance.phone = validated_data['phone']
        instance.save()

        addresses_data = validated_data.get('addresses', [])
        address_ids = [address['id'] for address in addresses_data if 'id' in address]
        addresses_to_delete = Address.objects.filter(user=instance).exclude(id__in=address_ids)
        addresses_to_delete.delete()

        for address_data in addresses_data:
            if 'id' in address_data:
                address = Address.objects.get(id=address_data['id'])
                address_serializer = AddressSerializer(instance=address, data=address_data)
                address_serializer.is_valid(raise_exception=True)
                address_serializer.save()
            else:
                address_data['user'] = instance
                address_serializer = AddressSerializer(data=address_data)
                address_serializer.is_valid(raise_exception=True)
                address_serializer.save()

        return instance