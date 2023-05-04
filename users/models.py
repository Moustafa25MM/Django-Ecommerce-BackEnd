from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
from django.utils import timezone
import re


def validateImage(image):
    if image.size > 5 * 1024 * 1024 :
        raise ValidationError('Image size should be less than 5MB.')
    
    file_extension = image.name.split('.')[-1].lower()
    if file_extension not in ['png', 'jpg', 'jpeg']:
        raise ValidationError('Only PNG, JPG, and JPEG images are allowed.')

def validate_phone_number(value):
    pattern = r'^(\+20\s)?(01)[012][0-9]{8}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid phone number format.')
        # +20 01033022410
        # 01033022410
    
    
class CustomUser(AbstractUser):
    
    email=models.EmailField(unique=True)
    image = CloudinaryField('images',validators=[validateImage])
    phone = models.CharField(max_length=15 , validators=[validate_phone_number], unique=True)
    confirm_password = models.CharField(max_length=16)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # +20 01033022410
    # def clean(self):
    #     super().clean()
    #     if self.password != self.confirm_password:
    #         raise ValidationError('Passwords do not match')
    
    def __str__(self):
        return self.username
    
    



# Create your models here.
