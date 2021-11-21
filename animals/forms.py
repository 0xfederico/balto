from crispy_forms.helper import FormHelper
from django import forms
from django.utils import timezone

from animals.models import Animal, AnimalDescription, AnimalHealth, AnimalManagement
from facility.models import Box


class AnimalForm(forms.ModelForm):
    helper = FormHelper()  # enable graphic finishes

    def clean_check_in_date(self):
        date = self.cleaned_data['check_in_date']
        if date > timezone.now().date():
            raise forms.ValidationError('The check-in date cannot be in the future.')
        return date

    def clean_birth_date(self):
        date = self.cleaned_data['birth_date']
        if date > timezone.now().date():
            raise forms.ValidationError('The birth date cannot be in the future.')
        return date

    box = forms.ModelChoiceField(
        label='Box',
        widget=forms.RadioSelect,
        queryset=Box.objects.all().order_by('name'),
        help_text='Select the box where the animal will stay',
        required=True
    )

    class Meta:
        model = Animal
        fields = ['name', 'breed', 'sex', 'photo', 'microchip', 'check_in_date', 'birth_date', 'box']

        # forcing input type https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AnimalDescriptionForm(forms.ModelForm):
    helper = FormHelper()  # enable graphic finishes

    class Meta:
        model = AnimalDescription
        fields = ['size', 'color', 'spots', 'ears', 'hair_length', 'tail', 'origin', 'particular_signs']


class AnimalManagementForm(forms.ModelForm):
    helper = FormHelper()  # enable graphic finishes

    class Meta:
        model = AnimalManagement
        fields = ['sociability_with_females', 'sociability_with_males', 'sociability_with_children',
                  'needs_another_dog', 'needs_garden', 'walk_equipment', 'flag_warning']


class AnimalHealthForm(forms.ModelForm):
    helper = FormHelper()  # enable graphic finishes

    class Meta:
        model = AnimalHealth
        fields = ['pathologies', 'diet', 'note']
