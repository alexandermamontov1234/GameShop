from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    first_name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')
    number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True, )
    avatar = models.ImageField(default='avatar.pnj', upload_to='avatars', verbose_name='аватар')
    balance = models.DecimalField(max_digits=11, decimal_places=2, blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True, verbose_name='URL')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('profiles', kwargs={'profile_slug': self.slug})

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        self.slug = str(self.user)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



