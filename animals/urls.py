from django.urls import path
from animals.views import RegisterNewAnimal, RemoveAnimal, InfoAnimal, ListAnimals, UpdateInfoAnimal

app_name = "animals"

urlpatterns = [
    path('register', RegisterNewAnimal.as_view(), name='animal-register'),
    path('<int:pk>/remove', RemoveAnimal.as_view(), name='animal-remove'),
    path('<int:pk>/info', InfoAnimal.as_view(), name='animal-info'),
    path('list', ListAnimals.as_view(), name='animals-list'),
    path('<int:pk>/update', UpdateInfoAnimal.as_view(), name='animal-update'),
]
