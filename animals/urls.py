from django.urls import path
from animals.views import AnimalCreateView, AnimalDeleteView, AnimalInfoView, AnimalListView, AnimalUpdateView

app_name = "animals"

urlpatterns = [
    path('animal-create', AnimalCreateView.as_view(), name='animal-create'),
    path('<int:pk>/animal-delete', AnimalDeleteView.as_view(), name='animal-delete'),
    path('<int:pk>/animal-info', AnimalInfoView.as_view(), name='animal-info'),
    path('animals-list/', AnimalListView.as_view(), name='animals-list'),
    path('<int:pk>/animal-update', AnimalUpdateView.as_view(), name='animal-update'),
]
