from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE) 
  first_name = models.CharField(max_length=100, blank=True)
  last_name = models.CharField(max_length=100, blank=True)
  email = models.EmailField(max_length=150)
  signup_confirmation = models.BooleanField(default=False) 
  
  
  def __str__(self): 
    return self.user.username 
@receiver(post_save, sender=User) 
def create_user_profile(sender, instance, created, **kwargs):
    try:
      instance.profile.save()
    except ObjectDoesNotExist:
     Profile.objects.create(user=instance)