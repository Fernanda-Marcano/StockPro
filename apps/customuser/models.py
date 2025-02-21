from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.products.models import Value


class Profile(models.Model):
    GBL_HIERAR_ID_GENDER = 13
    
    gender = models.OneToOneField(Value, related_name='profile_id_gender', limit_choices_to=Q(hierar_id=GBL_HIERAR_ID_GENDER), on_delete=models.PROTECT, null=True)
    image = models.ImageField(verbose_name='Imagen de Perfil', upload_to='user/img/', default='user/img/default-user.webp')
    user = models.OneToOneField(User, related_name='profile_user', on_delete=models.PROTECT)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile_user.save()
