from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Product(models.Model):
    PRDName=models.CharField(max_length=200, verbose_name=_('Product Name'))
    PRDCategory=models.ForeignKey('Category',on_delete=models.CASCADE, blank=True, null=True,verbose_name=_('Category'))
    PRDDesc=models.TextField(verbose_name=_('Product_Description'))
    PRDIImage = models.ImageField(upload_to='product/', verbose_name=_('Image'), blank=True, null=True)
    PRDPrice=models.DecimalField(max_digits=5 ,decimal_places=2, verbose_name=_('Price'))
    PRDDiscountPrice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('DiscountPrice'))
    PRDCost=models.DecimalField(max_digits=5 ,decimal_places=2, verbose_name=_('Cost'))
    PRDCreated=models.DateTimeField(verbose_name=_('Created At'))
    PRDSlug = models.SlugField(blank=True, null=True, verbose_name=_('Product URL'))
    PRDISNew = models.BooleanField(default=True, verbose_name=_('New Product'))
    PRDISSeller = models.BooleanField(default=False, verbose_name=_('Best seller'))





    def save(self, *args, **kwargs):
        if not self.PRDSlug:
            self.PRDSlug = slugify(self.PRDName)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.PRDName


    def get_absolute_url(self):
        return reverse('products:product_details', kwargs={'slug': self.PRDSlug})

    def get_add_to_cart_url(self):
        return reverse('Cart:add_to_cart', kwargs={'slug': self.PRDSlug})

    def get_remove_from_cart_url(self):
        return reverse('Cart:remove_from_cart', kwargs={'slug': self.PRDSlug})


class ProductImage(models.Model):
     PRDIProduct=models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
     PRDIImage= models.ImageField(upload_to='product/', verbose_name=_('Image'))

     def __str__(self):
         return str(self.PRDIProduct)





class Category(models.Model):
    CATName = models.CharField(choices=(('lap','laptop'),('TV', 'TV'),('M' , 'Mobile')),max_length=50, verbose_name=_('Name'))
    CATParent = models.ForeignKey('self',limit_choices_to={'CATParent__isnull':True},on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Main Category'))
    CATDes = models.TextField(verbose_name=_('Description'))
    CATImg = models.ImageField(upload_to='category/',verbose_name=_('Image'))
    CATLabel = models.CharField(choices= (('BR','badge red'),('BB', 'badge blue'),('BG' , 'badge green')), max_length=100)

    class Meta:
       verbose_name= _('Category')
       verbose_name_plural= _('Categories')

    def __str__(self):
       return self.CATName

class Product_Alternatives(models.Model):
   PALNProduct = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='main_product', verbose_name=_('Product'))
   PALNAlternatives = models.ManyToManyField(Product, related_name='alternative_products', verbose_name=_('Alternative'))
   def __str__(self):
      return str(self.PALNProduct)

class Product_Accessories(models.Model):
    PACCProduct= models.ForeignKey(Product,on_delete=models.CASCADE,related_name='mainAccessory_product',verbose_name=_('Product'))
    PACCAccessories = models.ManyToManyField(Product,related_name='accessories_products', verbose_name=_('Accessories'))
    def __str__(self):
       return str(self.PACCProduct)


