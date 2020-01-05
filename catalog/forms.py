from catalog.models import BookInstance
from django.forms import ModelForm
import datetime

from django import forms
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(widget=DatePickerInput(),
                                   help_text='Enter a date between today and 4 weeks later (default 3).',)

    renewal_date.widget.attrs.update(
        {'class': 'date date-field', 'id': 'renewal-date'})

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        is_in_past = False
        # check if the date is not in the past
        if data < datetime.date.today():
            is_in_past = True
            raise ValidationError(_('Invalid date - date in the past.'))
        # check if the date is not 4 weeks far
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - date is more than 4 weeks ahead.'))

        return data


class renew_book_ModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=3):
            raise ValidationError(_('Invalid date - too fare in the future'))
        return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        help_texts = {'due_back': _(
            'Enter a date between now and 4 weeks (default 3).'), }
        labels = {'due_back': _('Renewal Date:'), }
        widgets = {'due_back': DatePickerInput(), }
