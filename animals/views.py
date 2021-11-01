from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib import messages
from django.views.generic import DeleteView, DetailView, ListView

from Configurations.mixins import NoPermissionMessageMixin
from animals.forms import AnimalForm, AnimalDescriptionForm, AnimalManagementForm, AnimalHealthForm
from animals.models import Animal


class AnimalCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, View):
    permission_required = 'animals.add_animal'
    permission_denied_message = "You don't have permission to add animals"
    template_name = 'animals/animal_create_or_update.html'  # |as_crispy_field instead of |crispy -> better graphics
    success_message = 'Animal created correctly!'

    # the template is rendered with 4 forms as context based on permissions
    def get(self, request: HttpRequest):
        context = {'form': AnimalForm(), "view_text": "Register"}
        if request.user.has_perm('animals.add_animaldescription'):
            context['description_form'] = AnimalDescriptionForm()
        if request.user.has_perm('animals.add_animalmanagement'):
            context['management_form'] = AnimalManagementForm()
        if request.user.has_perm('animals.add_animalhealth'):
            context['health_form'] = AnimalHealthForm()
        return render(request, self.template_name, context)

    # based on permissions, the allowed forms are retrieved, if they are valid all objects are saved
    def post(self, request: HttpRequest):
        forms = [AnimalForm(request.POST, request.FILES)]
        if request.user.has_perm('animals.add_animaldescription'):
            forms.append(AnimalDescriptionForm(request.POST))
        if request.user.has_perm('animals.add_animalmanagement'):
            forms.append(AnimalManagementForm(request.POST))
        if request.user.has_perm('animals.add_animalhealth'):
            forms.append(AnimalHealthForm(request.POST))

        if all(map(lambda f: f.is_valid(), forms)):
            main_form = forms.pop(0)

            saved_other_form = dict()
            for form in forms:
                saved_other_form[
                    form.__class__.__name__.replace('Form', '').replace('Animal', '').lower()] = form.save()

            self.object = main_form.save(commit=False)
            self.object.photo = main_form.cleaned_data['photo']
            try:
                self.object.description = saved_other_form['description']
                self.object.management = saved_other_form['management']
                self.object.health = saved_other_form['health']
            except (KeyError, AttributeError):
                pass
            self.object.save()

            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse('animals:animal-info', kwargs={'pk': self.object.pk}))
        else:
            for form in forms:
                if not form.is_valid():
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, field + ': ' + error)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # return to the same url but with errors


class AnimalDeleteView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                       DeleteView):
    model = Animal
    template_name = 'animals/animal_delete.html'
    success_message = 'Animal deleted correctly!'
    permission_required = 'animals.delete_animal'
    permission_denied_message = "You don't have permission to delete animals"
    success_url = reverse_lazy('animals:animals-list')


class AnimalInfoView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                     DetailView):
    model = Animal
    template_name = 'animals/animal_info.html'
    permission_required = 'animals.view_animal'
    permission_denied_message = "You don't have permission to view animals"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.get_object()
        context['description'] = animal.description
        context['management'] = animal.management
        context['health'] = animal.health
        return context


class AnimalListView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                     ListView):
    model = Animal
    template_name = 'animals/animal_list.html'
    permission_required = 'animals.view_animal'
    permission_denied_message = "You don't have permission to view animals"
    ordering = ['name']


class AnimalUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, View):
    permission_required = 'animals.change_animal'
    permission_denied_message = "You don't have permission to edit animals"
    template_name = 'animals/animal_create_or_update.html'  # |as_crispy_field instead of |crispy -> better graphics
    success_message = 'Animal updated correctly!'

    # the template is rendered with 4 compiled forms as context based on permissions
    def get(self, request: HttpRequest, pk):
        animal = get_object_or_404(Animal, pk=pk)
        context = {'form': AnimalForm(instance=animal), "view_text": "Update"}
        if request.user.has_perm('animals.add_animaldescription'):
            context['description_form'] = AnimalDescriptionForm(instance=animal.description)
        if request.user.has_perm('animals.add_animalmanagement'):
            context['management_form'] = AnimalManagementForm(instance=animal.management)
        if request.user.has_perm('animals.add_animalhealth'):
            context['health_form'] = AnimalHealthForm(instance=animal.health)
        return render(request, self.template_name, context)

    # based on permissions, the allowed forms are retrieved, if they are valid all objects are saved
    def post(self, request: HttpRequest, pk):
        animal = get_object_or_404(Animal, pk=pk)
        forms = [AnimalForm(request.POST, request.FILES, instance=animal)]
        if request.user.has_perm('animals.add_animaldescription'):
            forms.append(AnimalDescriptionForm(request.POST, instance=animal.description))
        if request.user.has_perm('animals.add_animalmanagement'):
            forms.append(AnimalManagementForm(request.POST, instance=animal.management))
        if request.user.has_perm('animals.add_animalhealth'):
            forms.append(AnimalHealthForm(request.POST, instance=animal.health))

        if all(map(lambda f: f.is_valid(), forms)):
            main_form = forms.pop(0)
            if 'photo' in main_form.changed_data:
                self.object = main_form.save(commit=False)
                self.object.photo = main_form.cleaned_data['photo']
                self.object.save()
            else:
                self.object = main_form.save()

            for form in forms:
                form.save()

            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse('animals:animal-info', kwargs={'pk': self.object.pk}))
        else:
            for form in forms:
                if not form.is_valid():
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, field + ': ' + error)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # return to the same url but with errors
