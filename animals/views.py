from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from Configurations.mixins import NoPermissionMessageMixin
from animals.forms import AnimalForm
from animals.models import AnimalModel


class AnimalCreateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                       CreateView):
    model = AnimalModel
    form_class = AnimalForm
    template_name = 'animals/animal_create.html'
    success_message = 'Animal created correctly!'
    permission_required = 'animal.add_animal'
    permission_denied_message = "You don't have permission to add animals"

    def get_success_url(self):
        return reverse_lazy('animals:animal-info', kwargs={"pk": self.object.pk})


class AnimalDeleteView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                       DeleteView):
    model = AnimalModel
    template_name = 'animals/animal_delete.html'
    success_message = 'Animal deleted correctly!'
    permission_required = 'animal.delete_animal'
    permission_denied_message = "You don't have permission to delete animals"
    success_url = reverse_lazy('animals:animals-list')


class AnimalInfoView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = AnimalModel
    template_name = 'animals/animal_info.html'


class AnimalListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AnimalModel
    template_name = "animals/animal_list.html"
    ordering = ['name']


class AnimalUpdateView(LoginRequiredMixin, NoPermissionMessageMixin, PermissionRequiredMixin, SuccessMessageMixin,
                       UpdateView):
    model = AnimalModel
    form_class = AnimalForm
    template_name = 'animals/animal_update.html'
    success_message = 'Animal updated correctly!'
    permission_required = 'animal.update_animal'
    permission_denied_message = "You don't have permission to edit animals"

    def get_success_url(self):
        return reverse_lazy('animals:animal-info', kwargs={"pk": self.object.pk})
