from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,verbose_name=_('user'),on_delete= models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    join_date =models.DateTimeField(verbose_name=_('join date'), default=datetime.datetime.now)
    address = models.CharField(max_length=100)
    country = CountryField()
    image = models.ImageField(verbose_name=_('image'),upload_to='profile.img',blank=True,null=True)


    def __str__(self):

        return str(self.user)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
            super(Profile,self).save(*args, **kwargs)



    def get_absolute_url(self):
                return reverse('accounts:profile', kwargs={'slug':self.slug})


    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = Profile.objects.create(user=kwargs['instance'])
            print('instance')
    post_save.connect(create_profile, sender=User)




