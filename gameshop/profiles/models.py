from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
import uuid


def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code


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

    # def save(self, *args, **kwargs):
        # to_slug = str(self.user)
        # self.slug = to_slug
        # super().save(*args, **kwargs)

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug == "":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



