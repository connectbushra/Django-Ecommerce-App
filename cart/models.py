from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.forms import ModelForm
from django.db.models import Avg, Count
# from mptt.models import MPTTModel


class Person(models.Model):
    id=models.AutoField(primary_key=True)
    type =models.CharField(max_length=30)
    def __str__(self):
         return self.type
    class Meta:
        verbose_name_plural ="person"



class Color(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    code=models.CharField(max_length=100)
    def __str__(self):
         return self.name
    class Meta:
        verbose_name_plural ="color"


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    slug= models.SlugField(null=False,default=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "brand"

    def get_absolute_url(self):
        return reverse("cart:brands",args=[self.slug])

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, db_index=True,null=True)
    slug = models.SlugField(null=False,default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("cart:categories", args=[self.slug])


class items(models.Model):
    LABEL = [
        ('P', 'primary'),
        ('s', 'secondary'),
        ('D', 'danger'),
        ('Sc', 'success'),
        ('w', 'warning'),
    ]
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to="pics", null=True, blank=True)
    title = models.CharField(max_length=100)
    offer = models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='')
    lable = models.CharField(choices=LABEL, max_length=2, default='')
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,null=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    person = models.ForeignKey(Person,on_delete=models.CASCADE,null=True)
    price = models.PositiveIntegerField(default=0)
    slug = models.SlugField(null=False)
    Description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("cart:product", kwargs={'slug': self.slug})

    def get_home_add_item_url(self):
        return reverse("cart:home_add_item", kwargs={
            'slug': self.slug})

    def get_cart_add_item_url(self):
        return reverse("cart:cart_add_item", kwargs={
            'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("cart:delete_item", kwargs={
            'slug': self.slug
        })

    def get_remove_qty(self):
        return reverse("cart:remove_qty", kwargs={
            'slug': self.slug
        })
    def averagereview(self):
        reviews = Review.objects.filter(item=self).aggregate(average=Avg('rate'))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg

    def countreview(self):
        reviews = Review.objects.filter(item=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    quantity=models.IntegerField(default=1)
    item=models.ForeignKey(items,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ManyToManyField(OrderItem)
    create_date = models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    Bill_address=models.ForeignKey('Address',on_delete=models.SET_NULL,blank=True,null=True)
    payment=models.ForeignKey('payment',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        return self.user.username

    def get_total(self):
        total=0
        for i in self.product.all():
            total+=i.get_total_item_price()
        return total

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=30,default=True)
    address=models.CharField(max_length=100)
    address2=models.CharField(max_length=100,default=True)
    # home_address=models.CharField(max_length=100)
    country = CountryField(multiple=False)
    state=models.CharField(max_length=100,null=False,default=True)
    city =models.CharField(max_length=100,null=False,default=True)
    zip=models.CharField(max_length=6)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    # stripe_charges_id=models.CharField(max_length=50)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    amount=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.user.username


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(items,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment = models.CharField(max_length=250,blank=True)
    status = models.CharField(max_length=10, default='New')
    rate = models.IntegerField(default=1)
    # ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rate']

# class Coupon(models.Model):
#     code = models.CharField(max_length=15)
#
#     def __str__(self):
#         return self.code
