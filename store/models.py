from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField



# Create your models here. 
class Book(models.Model):
   title = models.CharField(max_length=100)
   slug = models.SlugField(max_length=110)
   author = models.CharField(max_length=50, blank=True, null=True)
   image = models.ImageField(upload_to='bk_img')
   description = RichTextField(null=True, blank=True,)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   available = models.BooleanField(default=True)
   is_featured = models.BooleanField(default=False)
   is_new = models.BooleanField(default=False)
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)

   class Meta:
      ordering = ('title',)
      verbose_name = 'book'
      verbose_name_plural = 'books'
      
   def __str__(self):
      return '{}'.format(self.title)
   
   def get_absolute_url(self):
      return reverse("book-detail", kwargs={
         'slug': self.slug,
      })
      
   def add_to_cart_url(self):
      return reverse("add-to-cart", kwargs={
         'slug': self.slug
      })
   
   def get_remove_from_cart_url(self):
      return reverse("remove-from-cart", kwargs={
         'pk':self.pk,
         'slug': self.slug
      }) 


class OrderBook(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   book = models.ForeignKey(Book, on_delete=models.CASCADE)
   quantity = models.IntegerField(default=1)
   ordered = models.BooleanField(default=False)   
   
   def __str__(self):
      return f'{self.quantity} of {self.book.title}'
   
   def get_total_item_price(self):
      return self.quantity * self.book.price

   def get_total_discount_item_price(self):
      return self.quantity * self.book.discount_price
   
   def get_amount_saved(self):
      return self.get_total_item_price() - self.get_total_discount_item_price()

   def get_final_price(self):
      if self.book.discount_price:
         return self.get_total_discount_item_price()
      return self.get_total_item_price()
 
class Order(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   ref_code = models.CharField(max_length=50, blank=True, null=True)
   books = models.ManyToManyField(OrderBook)
   start_date = models.DateTimeField(auto_now_add=True)
   ordered_date = models.DateTimeField()
   ordered = models.BooleanField(default=False)
   shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
   being_delivered = models.BooleanField(default=False)
   received = models.BooleanField(default=False)

   def __str__(self):
      return '{}'.format(self.user.username)
    
   def sub_total(self):
      total = 0
      for order_item in self.books.all():
         total += order_item.get_final_price()
      return total
   
   def saved_total(self):
      total = 0
      for order_item in self.books.all():
         total += order_item.get_amount_saved()
      return total
   
   def get_total(self):
      total = 0
      discount = 0
      for order_item in self.books.all():
         total += order_item.get_final_price()
         if self.coupon:
            discount = total * self.coupon.amount
         total -= discount
      return total
   
   def discount_price(self):
      total = 0
      for order_item in self.books.all():
         total += order_item.get_final_price()
      if self.coupon:
         discount = total * self.coupon.amount
      return discount


class Address(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   street_address = models.CharField(max_length=100)
   apartment_address = models.CharField(max_length=50)
   address_2 =models.CharField(max_length=100)
   phone_number = PhoneNumberField(blank=True, help_text='Phone Number')
   city = models.CharField(max_length=50)
   state = models.CharField(max_length=50)
   zip_code = models.CharField(max_length=10)
   
   def __str__(self):
      return self.user.username


class Payment(models.Model):
   stripe_charge_id = models.CharField(max_length=50)
   user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
   amount = models.FloatField()
   timestamp = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.user.username
   
   def payment_option(self):
      return reverse("payment", kwargs={
         'payment_option':payment_option
      })
      