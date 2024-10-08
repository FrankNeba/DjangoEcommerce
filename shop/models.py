from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique = True, null=True)
    avatar = models.ImageField(upload_to="images", default="images/profile.jpeg", null=True)
    address = models.CharField(max_length=200, null=True)
    code = models.IntegerField(unique=False, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to="images", null=True)
    price = models.PositiveIntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.user.username






