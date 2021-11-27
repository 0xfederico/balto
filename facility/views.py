from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, ListView

from Configurations.mixins import NoPermissionMessageMixin
from animals.models import Animal
from facility.forms import LegalInformationForm, AreaForm, BoxForm, AreaAddBoxesForm
from facility.models import LegalInformation, Area, Box


# ------------------- LEGAL INFORMATION -------------------
class LegalInformationInfoView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, DetailView):
    model = LegalInformation
    template_name = 'facility/legalinformation_info.html'
    permission_required = 'facility.view_legalinformation'
    permission_denied_message = "You don't have permission to view legal information"

    def dispatch(self, request, *args, **kwargs):
        if LegalInformation.objects.count() == 0:
            LegalInformation.load()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(LegalInformation, pk=1)


class LegalInformationUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin,
                                 SuccessMessageMixin, UpdateView):
    model = LegalInformation
    form_class = LegalInformationForm
    template_name = 'facility/legalinformation_update.html'
    success_message = 'Legal information updated correctly!'
    permission_required = 'facility.change_legalinformation'
    permission_denied_message = "You don't have permission to insert legal information"

    def dispatch(self, request, *args, **kwargs):
        if LegalInformation.objects.count() == 0:
            LegalInformation.load()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(LegalInformation, pk=1)

    def get_success_url(self):
        return reverse_lazy('facility:legalinformation-info')


# ------------------- AREAS -------------------
class AreaCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                     CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'facility/area_create_or_update.html'
    success_message = 'Area created correctly!'
    permission_required = 'facility.add_area'
    permission_denied_message = "You don't have permission to add areas"

    def get_success_url(self):
        return reverse_lazy('facility:area-info', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Create'
        return context


class AreaDeleteView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                     DeleteView):
    model = Area
    template_name = 'facility/area_delete.html'
    success_message = 'Area deleted correctly!'
    permission_required = 'facility.delete_area'
    permission_denied_message = "You don't have permission to delete areas"
    success_url = reverse_lazy('facility:areas-list')

    # an area cannot be canceled if it has boxes inside it
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            box_number = Box.objects.filter(located_area__pk=self.object.pk).count()
            message_error = f'There are {box_number} boxes' if box_number > 1 else 'There is a box'
            messages.error(request, message_error + ' in this area, it cannot be deleted!')
            return render(request, self.template_name, {}, status=200)
        else:
            return HttpResponseRedirect(self.get_success_url())


class AreaAddBoxesView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, View):
    permission_required = 'facility.area_add_boxes'
    permission_denied_message = "You don't have permission to add boxes to an area"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.area = Area.objects.filter(pk=kwargs['pk'])[0]
        del kwargs['pk']  # we just need it to retrieve the area
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request: HttpRequest):
        context = {'area': self.area,
                   # In the second argument it is passed the list of area boxes
                   'form': AreaAddBoxesForm(request.GET, boxes=[b.pk for b in self.area.composedby.all()])}
        return render(request, 'facility/area_add_boxes.html', context, status=200)

    def post(self, request: HttpRequest):
        # In the second argument it is passed the list of area boxes
        form = AreaAddBoxesForm(request.POST, boxes=[b.pk for b in self.area.composedby.all()])
        if form.is_valid():
            boxes = form.cleaned_data.get('boxes')
            for b in boxes:
                self.area.composedby.add(b)
            messages.success(request, 'Boxes added to Area correctly!')
            return HttpResponseRedirect(reverse('facility:area-boxes', kwargs={'pk': self.area.pk}))
        else:
            returned_data_form = dict()
            returned_data_form['area'] = self.area
            returned_data_form['form'] = form
            if 'boxes' in form.errors.as_data():  # check if the error is in the boxes field
                returned_data_form['boxes_error'] = form.fields['boxes'].error_messages['required']
            return render(self.request, 'facility/area_add_boxes.html', returned_data_form)


class AreaDeleteAllBoxesView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, View):
    permission_required = 'facility.area_delete_boxes'
    permission_denied_message = "You don't have permission to delete boxes from area"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.area = Area.objects.filter(pk=kwargs['pk'])[0]
        del kwargs['pk']  # we just need it to retrieve the area
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request: HttpRequest):
        context = {'area': self.area}
        return render(request, 'facility/area_delete_all_boxes.html', context, status=200)

    def post(self, request: HttpRequest):
        boxes = self.area.composedby.all()
        for b in boxes:
            b.located_area = None
            b.save()
        messages.success(request, 'Removed all boxes from the area!')
        return HttpResponseRedirect(reverse('facility:area-boxes', kwargs={'pk': self.area.pk}))


class AreaDeleteBoxView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                        DeleteView):
    model = Area
    form_class = AreaForm
    template_name = 'facility/area_delete_box.html'
    success_message = 'Box removed from Area correctly!'
    permission_required = 'facility.area_delete_boxes'
    permission_denied_message = "You don't have permission to delete boxes from area"

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {'area': self.object,
                   'delete_box': get_object_or_404(Box, pk=kwargs['bpk'])}
        return self.render_to_response(context)

    def delete(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        box = self.object.composedby.get(pk=kwargs['bpk'])
        box.located_area = None
        box.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('facility:area-boxes', kwargs={'pk': self.object.pk})


class AreaBoxesView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, DetailView):
    model = Area
    template_name = 'facility/area_boxes.html'
    permission_required = 'facility.area_view_boxes'
    permission_denied_message = "You don't have permission to see area boxes"

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = {'area': self.object,
                   'boxes': Box.objects.filter(located_area__pk=self.object.pk).order_by('name')}
        return self.render_to_response(context)


class AreaInfoView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, DetailView):
    model = Area
    template_name = 'facility/area_info.html'
    permission_required = 'facility.view_area'
    permission_denied_message = "You don't have permission to view this area"


class AreaListView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, ListView):
    model = Area
    template_name = 'facility/area_list.html'
    permission_required = 'facility.view_area'
    permission_denied_message = "You don't have permission to view areas"
    ordering = ['name']


class AreaUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                     UpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'facility/area_create_or_update.html'
    success_message = 'Area updated correctly!'
    permission_required = 'facility.change_area'
    permission_denied_message = "You don't have permission to edit areas"

    def get_success_url(self):
        return reverse_lazy('facility:area-info', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Update'
        return context


# ------------------- Boxes -------------------
class BoxCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                    CreateView):
    model = Box
    form_class = BoxForm
    template_name = 'facility/box_create_or_update.html'
    success_message = 'Box created correctly!'
    permission_required = 'facility.add_box'
    permission_denied_message = "You don't have permission to add boxes"

    def get_success_url(self):
        return reverse_lazy('facility:box-info', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Create'
        return context

    def form_invalid(self, form):
        returned_data_form = dict()
        returned_data_form['form'] = form
        if 'located_area' in form.errors.as_data():  # check if the error is in the located_area field
            returned_data_form['located_area_error'] = form.fields['located_area'].error_messages['required']
        return render(self.request, self.template_name, {**self.get_context_data(), **returned_data_form})


class BoxDeleteView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                    DeleteView):
    model = Box
    template_name = 'facility/box_delete.html'
    success_message = 'Box deleted correctly!'
    permission_required = 'facility.delete_box'
    permission_denied_message = "You don't have permission to delete boxes"
    success_url = reverse_lazy('facility:boxes-list')

    # a box cannot be canceled if it has an animal inside it
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            animal_number = Animal.objects.filter(box__pk=self.object.pk).count()
            message_error = f'There are {animal_number} animals' if animal_number > 1 else f'There is an animal'
            messages.error(request, message_error + ' in this box, it cannot be deleted!')
            return render(request, self.template_name, {}, status=200)
        else:
            return HttpResponseRedirect(self.get_success_url())


class BoxInfoView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, DetailView):
    model = Box
    template_name = 'facility/box_info.html'
    permission_required = 'facility.view_box'
    permission_denied_message = "You don't have permission to view this box"


class BoxListView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, ListView):
    model = Box
    template_name = 'facility/box_list.html'
    permission_required = 'facility.view_box'
    permission_denied_message = "You don't have permission to view boxes"
    ordering = ['name']


class BoxUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                    UpdateView):
    model = Box
    form_class = BoxForm
    template_name = 'facility/box_create_or_update.html'
    success_message = 'Box updated correctly!'
    permission_required = 'facility.change_box'
    permission_denied_message = "You don't have permission to edit boxes"

    def get_success_url(self):
        return reverse_lazy('facility:box-info', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_text'] = 'Update'
        return context

    def form_invalid(self, form):
        returned_data_form = dict()
        returned_data_form['form'] = form
        if 'located_area' in form.errors.as_data():  # check if the error is in the located_area field
            returned_data_form['located_area_error'] = form.fields['located_area'].error_messages['required']
        return render(self.request, self.template_name, {**self.get_context_data(), **returned_data_form})
