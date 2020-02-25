from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models



# Create your models here.


# The Cart
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

#@receiver(post_save, sender=User)
#def create_or_update_user_userprofile(sender, instance, created, **kwargs):
    #if created:
       # UserProfile.objects.create(user=instance)
#@receiver(post_save, sender=User)
#def save_user_userprofile(sender, instance, **kwargs):
    #instance.userprofile.save()
@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kwargs):
    user=instance
    if created:
        profile=UserProfile(user=user)
        profile.save()






class Item(models.Model):
    title = models.CharField(max_length=100)
    PRDPrice = models.FloatField()
    PRDDiscountPrice = models.FloatField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    description = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Item, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_details', kwargs={'slug': self.slug})




class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    orderd = models .BooleanField(default=False,blank=True,null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.PRDPrice

    def get_total_discount_item_price(self):
        return self.quantity * self.item.PRDDiscountPrice

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.PRDDiscountPrice:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()






class Order(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     ref_code = models.CharField(max_length=3, blank=True, null=True)
     item = models.ManyToManyField(OrderItem)
     start_date = models.DateTimeField(auto_now_add=True)
     orderd_date = models.DateTimeField()
     orderd = models.BooleanField(default=False)
     billing_address = models.ForeignKey('BillingAddress',on_delete= models.SET_NULL, blank =True, null=True)
     shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL,related_name='shipping_address', blank=True, null=True)
     payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
     coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
     being_delivered = models.BooleanField(default=False)
     received = models.BooleanField(default=False)
     refund_requested = models.BooleanField(default=False)
     refund_granted = models.BooleanField(default=False)

     def __str__(self):
         return self.user.username


     def get_total(self):
         total=0
         for order_item in self.item.all():
             total += order_item.get_final_price()
         if self.coupon:
             total -= self.coupon.amount
         return total

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)


    def __str__(self):
        return self.user.username

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    email = models.EmailField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"





