from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
      
    def __str__(self):
       return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    desc = models.TextField(max_length=500)
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to = "shop/images",default="")
   
    def __str__(self):
       return self.name
   


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50,default="")
    desc = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.IntegerField()
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product.name
    

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default=0)
    update_desc = models.CharField(max_length=50)
    timestemp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7]+"......"

# class Order(models.Model):
#     order_id = models.AutoField(primary_key=True)
#     #itemJson = models.CharField(max_length=50)
#     name = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     address = models.CharField(max_length=200)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     phone = models.CharField(max_length=50)
#     def __str__(self):
#         return self.name  
# # 