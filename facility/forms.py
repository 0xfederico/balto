from crispy_forms.helper import FormHelper
from django import forms

from facility.models import LegalInformation, Area, Box


class LegalInformationForm(forms.ModelForm):
    helper = FormHelper()  # enable graphic finishes

    class Meta:
        model = LegalInformation
        fields = ['email', 'name', 'region', 'city', 'province', 'address', 'mobile_phone', 'landline_phone',
                  'about_us', 'responsible']


class AreaForm(forms.ModelForm):
    helper = FormHelper()  # enable graphic finishes

    class Meta:
        model = Area
        fields = ['name']


class BoxForm(forms.ModelForm):
    helper = FormHelper()  # enable graphic finishes

    located_area = forms.ModelChoiceField(
        label='Located Area',
        widget=forms.RadioSelect,
        queryset=Area.objects.all().order_by('name'),
        help_text='Select the area where the box is located',
        required=True
    )

    class Meta:
        model = Box
        fields = ['name', 'located_area']


class AreaAddBoxesForm(forms.Form):
    helper = FormHelper()  # enable graphic finishes

    # The override is necessary to be able to pass as argument the boxes of the area and exclude them from the selection
    def __init__(self, *args, **kwargs):
        exclude_boxes = kwargs.pop('boxes')
        super(AreaAddBoxesForm, self).__init__(*args, **kwargs)
        self.fields['boxes'] = forms.ModelMultipleChoiceField(label='Boxes', widget=forms.CheckboxSelectMultiple,
                                                              queryset=Box.objects.all().exclude(
                                                                  pk__in=exclude_boxes).order_by('name'),
                                                              help_text='Select a box to add', required=True)
