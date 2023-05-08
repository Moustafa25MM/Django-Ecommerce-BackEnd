from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from cloudinary.models import CloudinaryField ,CloudinaryResource 
import cloudinary.api



def validateImage(image):
    if not isinstance(image, CloudinaryResource):
        # The image is not a Cloudinary resource, so we can't validate it
        return

    info = cloudinary.api.resource(image.public_id)
    file_size = info.get("bytes")
    if not file_size:
        raise ValidationError('Failed to get image size.')

    print(file_size)
    if file_size > 5 * 1024 * 1024:
        raise ValidationError('Image size should be less than 5MB.')

    file_extension = image.format.lower()
    if file_extension not in ['png', 'jpg', 'jpeg']:
        raise ValidationError('Only PNG, JPG, and JPEG images are allowed.')


class Category(models.Model):
    name = models.CharField(max_length=30, validators=[MinLengthValidator(3)])

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=20 , validators=[MinLengthValidator(3)])
    description = models.TextField(max_length=200 , validators=[MinLengthValidator(3)])
    price = models.DecimalField(max_digits=10, decimal_places=2 , validators=[MinValueValidator(0.01)])
    available_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    # image = CloudinaryField('images', validators=[validate_image_size, validate_image_extension])

    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name='product') 


    def __str__(self):
        return self.name