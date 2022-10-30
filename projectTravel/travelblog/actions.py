import logging

from django.db.models import Model

logger = logging.getLogger('logit')


def translation(modeladmin, request, queryset):
    for obj in queryset:
        print(obj.title)


def translate_obj(obj: Model):
    logger.info(obj)

translation.short_description = 'translate Info'
