from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.products.models import Value


class Profile(models.Model):
    GBL_HIERAR_ID_GENDER = 13
    
    gender = models.ForeignKey(Value, related_name='profile_id_gender', limit_choices_to=Q(hierar_id=GBL_HIERAR_ID_GENDER) | Q(hierar_id=0), default=1, on_delete=models.PROTECT)
    image = models.ImageField(verbose_name='Imagen de Perfil', upload_to='user/img/', default='user/img/default-user.webp')
    user = models.OneToOneField(User, related_name='profile_user', on_delete=models.PROTECT)

    pdt_map = {
        'gender':GBL_HIERAR_ID_GENDER,
    }