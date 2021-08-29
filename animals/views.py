from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from animals.forms import AnimalForm
from animals.models import Animal


class RegisterNewAnimal(CreateView):

    model = Animal
    form_class = AnimalForm
    template_name = "animals/register.html"
    success_url = reverse_lazy("animals:animals-list")
    success_message = 'Animal registered correctly!'

    def handle_no_permission(self):
        messages.error(self.request, "You must authenticate first!")
        return super(RegisterNewAnimal, self).handle_no_permission()


class RemoveAnimal(DeleteView):

    model = Animal
    template_name = "animals/remove.html"
    success_url = reverse_lazy("animals:animals-list")

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to remove this content!")
        return super(RemoveAnimal, self).handle_no_permission()


class InfoAnimal(DetailView):

    model = Animal
    template_name = "animals/info.html"


class ListAnimals(ListView):

    model = Animal
    template_name = "animals/list.html"


class UpdateInfoAnimal(UpdateView):

    model = Animal
    form_class = AnimalForm
    template_name = "animals/update.html"
    success_url = reverse_lazy("animals:animals-list")

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to remove this content!")
        return super(UpdateInfoAnimal, self).handle_no_permission()

