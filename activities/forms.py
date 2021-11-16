from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError

from activities.models import Activity, Event, custom_slugify
from animals.models import Animal
from users.models import User


class ActivityForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    class Meta:
        model = Activity
        fields = ['name', 'action_to_be_performed', 'icon']
        help_texts = {'name': 'A permission with the same name will be created to be assigned to groups to carry out '
                              'this activity',
                      'action_to_be_performed': 'In the permission\'s name it will become "Can do Something"'}
        widgets = {'action_to_be_performed': forms.TextInput(attrs={'placeholder': 'Do something'})}


class ActivityFormCreate(ActivityForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if Permission.objects.filter(codename=custom_slugify(name)).exists():
            raise ValidationError('A permission with this name already exists')
        return name


class ActivityFormUpdate(ActivityForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if 'name' in self.changed_data and Permission.objects.filter(codename=custom_slugify(name)).exists():
            raise ValidationError('A permission with this name already exists')
        return name


class EventForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'

    # The override is necessary to be able to pass as argument the current logged in user
    def __init__(self, *args, **kwargs):
        currentuser = kwargs.pop('currentuser')
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.ModelMultipleChoiceField(label='Users', widget=forms.CheckboxSelectMultiple,
                                                              queryset=User.objects.all().order_by('username'),
                                                              help_text='Select at least one user involved in the event',
                                                              required=True, initial=currentuser)

    animals = forms.ModelMultipleChoiceField(
        label='Animals',
        widget=forms.CheckboxSelectMultiple,
        queryset=Animal.objects.all().order_by('name'),
        help_text='Select at least one animal involved in the event',
        required=True
    )

    activity = forms.ModelChoiceField(
        label='Activity',
        widget=forms.RadioSelect,
        queryset=Activity.objects.all().order_by('name'),
        help_text='Select the activity',
        required=True
    )

    class Meta:
        model = Event
        fields = ['datetime', 'animals', 'users', 'activity', 'note']

        # forcing input type https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/datetime-local
        widgets = {'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'})}
