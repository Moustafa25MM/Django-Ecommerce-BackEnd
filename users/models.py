from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
import cloudinary.api
from cloudinary.models import CloudinaryField , CloudinaryResource 
from django.core.validators import MinLengthValidator
import re


class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        
        return user
    
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault('is_active', True)

        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser has to have the is_staff being True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser has to have the is_superuser being True")
        

        return self.create_user(email=email,password=password,**extra_fields)



def validateImage(image):
    if not isinstance(image, CloudinaryResource):
        # The image is not a Cloudinary resource, so we can't validate it
        return
    
    info = cloudinary.api.resource(image.public_id)
    file_size = info.get("bytes")
    if not file_size:
        raise ValidationError('Failed to get image size.')
    
    print(file_size)
    if file_size > 2 * 1024 * 1024:
        raise ValidationError('Image size should be less than 2MB.')
    
    file_extension = image.format.lower()
    if file_extension not in ['png', 'jpg', 'jpeg']:
        raise ValidationError('Only PNG, JPG, and JPEG images are allowed.')
    
    
def validate_phone_number(value):
    pattern = r'^(\+20\s)?(01)[012][0-9]{8}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid phone number format.')
        # +20 01033022410
        # 01033022410
    
    
class CustomUser(AbstractUser):
    
    email=models.EmailField(unique=True , max_length=80)
    username = models.CharField(max_length=45)
    date_of_birth = models.DateField(null=True , blank=True)
    image = CloudinaryField('images',validators=[validateImage])
    phone = models.CharField(max_length=15 , validators=[validate_phone_number], unique=True)
    confirm_password = models.CharField(max_length=16)
    
    # +20 01033022410
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']
    
    def clean(self):
        super().clean()
        if self.password != self.confirm_password:
            raise ValidationError('Passwords do not match')
    
    def __str__(self):
        return self.username
    
    

class Address(models.Model):
    city = models.CharField(validators=[MinLengthValidator(3)], max_length=50)
    country = models.CharField(validators=[MinLengthValidator(3)], max_length=50)
    street = models.CharField(validators=[MinLengthValidator(3)], max_length=50)
    building_number = models.CharField(validators=[MinLengthValidator(1)], max_length=50)
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE , related_name='addresses' , blank=True , null=True)

    
    
    def __str__(self):
        return f"{self.building_number} , {self.street} , {self.city} , {self.country}"
