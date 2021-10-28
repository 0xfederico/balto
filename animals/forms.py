from crispy_forms.helper import FormHelper
from django import forms
from django.forms import ModelChoiceField

from animals.models import Animal, AnimalDescription, AnimalHealth, AnimalManagement
from facility.models import Box


class AnimalForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "POST"

    class ChangedLabelCSMF(ModelChoiceField):
        def label_from_instance(self, box):
            return box.name

    box = ChangedLabelCSMF(
        label="Box",
        widget=forms.RadioSelect,
        queryset=Box.objects.all().order_by('name'),
        help_text='Select the box where the animal will stay',
        required=True
    )

    class Meta:
        model = Animal
        fields = ["name", "breed", "sex", "photo", "microchip", "check_in_date", "birth_date", "box"]

        # forcing input type https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AnimalDescriptionForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "animaldescription_crispy_form"
    helper.form_method = "POST"

    class Meta:
        model = AnimalDescription
        fields = ["size", "color", "spots", "ears", "hair_length", "tail", "origin", "particular_signs"]


class AnimalManagementForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "animalmanagement_crispy_form"
    helper.form_method = "POST"

    class Meta:
        model = AnimalManagement
        fields = ["sociability_with_females", "sociability_with_males", "sociability_with_children",
                  "needs_another_dog", "needs_garden", "walk_equipment", "flag_warning"]


class AnimalHealthForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "animalhealth_crispy_form"
    helper.form_method = "POST"

    class Meta:
        model = AnimalHealth
        fields = ["pathologies", "diet", "note"]
