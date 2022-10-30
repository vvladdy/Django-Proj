import logging
from django.views.generic import FormView, TemplateView
from django.contrib import messages # модуль для обмена сообщениями

from .forms import ContactForm
from . models import Contact

class ContactView(FormView):
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        Contact.objects.create(**form.cleaned_data)
        print('valid_form', form.cleaned_data)
        messages.add_message(   # из django.contrib
            self.request, messages.SUCCESS,
            'Ваше сообщение отправлено. Спасибо.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        logger = logging.getLogger('logit.log')
        logger.debug(form.cleaned_data)
        print('invalid_form', form.cleaned_data)
        messages.add_message(
            self.request, messages.WARNING,
            'Неверно заполнены поля'
        )
        return super().form_invalid(form)
