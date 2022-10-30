import random

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from .models import Blog, Image, Category

def index(request):
    article = Category.objects.all()[:]
    info_date = Blog.objects.all()
    title_img = Image.objects.all()[:]

    blogs = Blog.objects.prefetch_related()
    pict = Image.objects.prefetch_related()

    context = {
        'article': article,
        'info_date': info_date,
        'pict': random.choices(pict, k=21),
        'title_img': title_img[5:41],
        'featured_blogs': random.choices(blogs, k=5)
    }

    return render(request, 'index.html', context)


def gallery(request):
    info_date = Blog.objects.all()
    title_img = Image.objects.all()
    item = Blog.objects.prefetch_related('images')

    context = {
        'blog': item,
        'info_date': info_date,
        'title_img': title_img
    }
    return render(request, 'gallery.html', context)


def singlepost(request, **kwargs):
    blogs = Blog.objects.prefetch_related('images') # related name
    item = Blog.objects.prefetch_related('images').get(slug=kwargs['slug'])
    info_date = Blog.objects.all()
    context = {
        'featured_blogs': random.choices(blogs, k=5),
        'blog': item,
        'info_date': info_date[1:4]
    }
    return render(request, 'singlepost.html', context)

# def contact(request):
#     context = {}
#     return render(request, 'contact.html', context)


class GallerPhoto(ListView):
    template_name = 'gallery.html'
    model = Image
    paginate_by = 10
    queryset = Image.objects.all()
    context_object_name = 'title_img'


class TitlePagin(ListView):
    template_name = 'index.html'
    model = Blog
    paginate_by = 5
    queryset = Blog.objects.all()
    context_object_name = 'info_date'
