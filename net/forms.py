# -*- coding: UTF-8 -*-

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from net.models import User, Place, NetGroup as Group, DATA_FIELDS, PlaceTemplate, Country, City, PlaceType

import datetime

year = datetime.date.today().year

class DataFieldsForm(forms.ModelForm):
    data_fields = None
    
    def __init__(self, data_fields={}, *args, **kwargs):
        self.data_fields = self.data_fields or data_fields
        if self._meta.exclude:
            self._meta.exclude += self.data_fields.keys()
        super(DataFieldsForm, self).__init__(*args, **kwargs)

        for field, items in self.data_fields.items():
            for item in items:
                self.fields[item] = forms.CharField(required=False, initial=self.instance.get_data(field).get(item, ''))
            
    def save(self, *args, **kwargs):
        super(DataFieldsForm, self).save(*args, **kwargs)
        
        for field, items in self.data_fields.items():
            data = {}
            for item in items:
                data[item] = self.cleaned_data[item]
            self.instance.set_data(field, data)
            
    def as_fs(self):
        "Returns this form rendered as HTML <fieldset>s."
        return self._html_output(u'<fieldset>%(label)s %(field)s%(help_text)s</fieldset>', u'%s', '</fieldset>', u' %s', True)

class SearchForm(forms.ModelForm):
    place = forms.CharField(max_length=255)
    age_from = forms.IntegerField()
    age_to = forms.IntegerField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for k in self.fields.keys():
            self.fields[k].required = False

    def get_query(self):
        if self.is_valid():
            result = {}
            if self.cleaned_data['place']:
                result['places__template__translations__name__icontains'] = self.cleaned_data['place']
            if self.cleaned_data['first_name']:
                result['first_name__icontains'] = self.cleaned_data['first_name']
            if self.cleaned_data['last_name']:
                result['first_name__icontains'] = self.cleaned_data['last_name']
            if self.cleaned_data['age_from']:
                result['birthdate__lte'] = datetime.datetime.now() - 366 * datetime.timedelta(self.cleaned_data['age_from'])
            if self.cleaned_data['age_to']:
                result['birthdate__gte'] = datetime.datetime.now() - 366 * datetime.timedelta(self.cleaned_data['age_to'])
            return result
        else:
            return {}
        
    def as_fs(self):
        "Returns this form rendered as HTML <fieldset>s."
        return self._html_output(u'<fieldset>%(label)s %(field)s%(help_text)s</fieldset>', u'%s', '</fieldset>', u' %s', True)
        
class PlaceForm(DataFieldsForm):
    country = forms.ChoiceField(choices=[(c.pk, c.name) for c in Country.objects.all()])
    type = forms.ChoiceField(choices=[(t.pk, t.name) for t in PlaceType.objects.all()])
    
    city = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255)
    
    class Meta:
        model = Place
        exclude = ['user', 'template']
        
    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        
        self.fields['from_date'].widget = SelectDateWidget(years=range(year, year-100, -1))
        self.fields['to_date'].widget = SelectDateWidget(years=range(year, year-100, -1))
        
        try:
            self.fields['title'].initial = self.instance.template.name
        except:
            pass

    def save(self, user, *args, **kwargs):
        kwargs.update({"commit":False})
        super(PlaceForm, self).save(*args, **kwargs)
        city, created = City.objects.get_or_create(name=self.cleaned_data['city'], country__pk=self.cleaned_data['country'])
        self.instance.template, created = PlaceTemplate.objects.get_or_create(
            name=self.cleaned_data['title'],
            city=city,
            type=PlaceType.objects.get(pk=self.cleaned_data['type'])
        )
        self.instance.user = user
        self.instance.save()
        return self.instance
        
class ProfileForm(DataFieldsForm):
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    
    data_fields = DATA_FIELDS

    class Meta:
        model = User
        exclude = [
            'user_data', 'username', 'password', 
            'is_staff', 'is_active', 'is_superuser', 
            'user_ptr', 'groups', 'user_permissions',
            'date_joined', 'last_login', 'politics', 
            'about', 'writer', 
            'professional', 'contacts', 'site',
            'private',
        ] + DATA_FIELDS.keys()

    def __init__(self, *args, **kwargs):

        super(ProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['birthdate'].widget = SelectDateWidget(years=range(year, year-100, -1))
        
    def clean_password1(self):
        if self.data.get('password1') and self.data.get('password2'):
            if self.data.get('password1') == self.data.get('password2'):
                if len(self.data.get('password1')) > 6:
                    return self.data.get('password1')
                raise forms.ValidationError(_('Password must be longer than 6 letters'))
            raise forms.ValidationError(_('Passwords do not match'))
        return None

    def save(self):
        super(ProfileForm, self).save(commit=False)
        
        if self.cleaned_data.get('password1') and len(self.cleaned_data.get('password1')) > 0:
            self.instance.set_password(self.cleaned_data['password1'])
        
        self.instance.save()
        
class InterestsForm(DataFieldsForm):
    data_fields = None
    list_fields = {
        'school': {
            'title': forms.CharField(),
            'from_date': forms.DateTimeField(widget=SelectDateWidget(years=range(year, year-100, -1))),
            'to_date': forms.DateTimeField(widget=SelectDateWidget(years=range(year, year-100, -1))),
        },
    }

    class Meta:
        model = User
        fields = ['interest']

    def __init__(self, *args, **kwargs):
        super(InterestsForm, self).__init__(*args, **kwargs)
        
        for field in self.list_fields.keys():
            if field != 'school':
                values = self.instance.get_data(field)

            idx = 0
            for value in values:
                for subfield in self.list_fields[field].keys():
                    self.fields[field + '_' + subfield + '_' + str(idx)] = self.list_fields[field][subfield]
                    try:
                        val = value.get(subfield)
                    except AttributeError:
                        val = value.__getattribute__(subfield)
                    self.fields[field + '_' + subfield + '_' + str(idx)].initial = val
                idx += 1
            for subfield in self.list_fields[field].keys():
                self.fields[field + '_' + subfield + '_' + str(idx)] = self.list_fields[field][subfield]

    def save(self, *args, **kwargs):
        super(InterestsForm, self).save(commit=False, *args, **kwargs)
        
        print self.cleaned_data
        
        for field in self.list_fields.keys():
            if field != 'school':
                values = self.instance.get_data(field)
                for idx in xrange(0, len(values) + 1):
                    if not idx in values:
                        values[idx] = {}
                    for subfield in self.list_fields[field].keys():
                        values[idx][subfield] = self.cleaned_data[field + '_' + subfield + '_' + str(idx)]
                        self.instance.set_data(field, values)
            else:
                for idx in xrange(0, len(self.instance.get_schools()) + 1):
                    School.objects.get_or_create(user=self.instance, 
                        title = self.cleaned_data[field + '_' + 'title' + '_' + str(idx)],
                        from_date = self.cleaned_data[field + '_' + 'from_date' + '_' + str(idx)],
                        to_date = self.cleaned_data[field + '_' + 'to_date' + '_' + str(idx)]
                    )

        self.instance.save()

class FieldsetFormSet(forms.formsets.BaseFormSet):
    def as_fs(self):
        "Returns this formset rendered as HTML <tr>s -- excluding the <table></table>."
        # XXX: there is no semantic division between forms here, there
        # probably should be. It might make sense to render each form as a
        # table row with each field as a td.
        forms = u' '.join([form.as_fs() for form in self.forms])
        return mark_safe(u'\n'.join([unicode(self.management_form.as_p()), forms]))

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'interest']
