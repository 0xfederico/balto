from django import forms
from animals.models import AnimalModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AnimalForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'animal_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit("submit", "Confirm"))

    class Meta:
        model = AnimalModel
        fields = ["name", "breed", "sex", "photo", "microchip", "particular_signs", "pathologies", "walk_equipment",
                  "check_in_date", "birth_date", "sociability_with_females", "sociability_with_males",
                  "sociability_with_children", "needs_another_dog", "needs_garden"]
