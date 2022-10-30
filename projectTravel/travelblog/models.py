from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=250, blank=False, null=True)
    slug = models.SlugField(max_length=250, unique=True)
    country = models.ForeignKey('travelblog.Blog',
                                   null=True,
                                   on_delete=models.RESTRICT)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    base_url = models.URLField(max_length=200)
    blog = models.ForeignKey('Blog', # обращение к несуществ.модели
                             # или 'travelblog.Blog',
                             blank=False,
                             null=True,
                             related_name='images',
                             on_delete=models.CASCADE)
    # ForeignKey in my tables is  Many(images)-TO-One(Blog)
    def __str__(self):
        return self.image.url


class Blog(models.Model):
    image = models.ImageField(upload_to='media/images', null=True,
                              blank=False)
    base_url = models.URLField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    text = models.TextField()
    slug = models.SlugField(max_length=250, unique=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def __str__(self):
        return self.title
