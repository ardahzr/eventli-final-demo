from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.user.username
    

class Category(MPTTModel):
    name = models.CharField(max_length=40)
    slug = models.SlugField(default="", null=False, unique=True, max_length=50, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f"{self.name}"

class Etkinlik(models.Model):
    title = models.CharField(max_length=40)
    isActive = models.BooleanField()
    date = models.DateField()
    description = models.TextField()
    adress = models.CharField(max_length=255)
    slug = models.SlugField(default="", blank=True, null=False, primary_key=True, db_index=True)
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='etkinlik_images', blank=True, null=True)
    katilimcilar = models.ManyToManyField(User, through='EtkinlikKatilim', related_name='katildigi_etkinlikler')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    enlem = models.FloatField()
    boylam = models.FloatField()
    def __str__(self):
        return self.title

class EtkinlikKatilim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    etkinlik = models.ForeignKey(Etkinlik, on_delete=models.CASCADE)
    kayit_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'etkinlik']


class Comment(models.Model):
    etkinlik = models.ForeignKey('Etkinlik', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.text