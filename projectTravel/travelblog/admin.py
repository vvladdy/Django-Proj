from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from . actions import translation

from .models import Category, Image, Blog


class ImageInlineAdmin(admin.TabularInline):
    model = Image
    fields = ('picture', 'image')
    readonly_fields = fields
    extra = 0

    @staticmethod
    def picture(obj):
        return format_html(
            '<img src="{}" style="max-width: 50px">', obj.image.url
        )


class BlogAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    actions = (translation, )
    summernote_fields = ('text', )
    inlines = (ImageInlineAdmin, )
    list_display = ('title', 'image', 'base_url')
    prepopulated_fields = {'slug': ('title',)}

    @staticmethod
    def image(obj):
        return format_html(
            '<img src="{}" style="max-width: 50px">', obj.images.image.url)

class ImageAdmin(admin.ModelAdmin):
    actions = (translation,)
    list_display = ('picture', 'blog')

    @staticmethod
    def picture(obj):
        return format_html(
            '<img src="{}" style="max-width: 50px">', obj.image.url
        )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'country')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)