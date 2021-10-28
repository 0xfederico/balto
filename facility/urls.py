from django.urls import path

from facility.views import LegalInformationInfoView, LegalInformationUpdateView, \
    BoxCreateView, BoxDeleteView, BoxInfoView, BoxListView, BoxUpdateView, \
    AreaCreateView, AreaDeleteView, AreaInfoView, AreaListView, AreaUpdateView, AreaDeleteBoxView, AreaAddBoxesView, \
    AreaBoxesView, AreaDeleteAllBoxesView

app_name = "facility"

urlpatterns = [
    # LEGAL INFORMATION
    path('legalinformation-info', LegalInformationInfoView.as_view(), name='legalinformation-info'),
    path('legalinformation-update', LegalInformationUpdateView.as_view(), name='legalinformation-update'),
    # AREAS
    path('area-create', AreaCreateView.as_view(), name='area-create'),
    path('<int:pk>/area-delete', AreaDeleteView.as_view(), name='area-delete'),
    path('<int:pk>/<int:bpk>/area-delete-box', AreaDeleteBoxView.as_view(), name='area-delete-box'),
    path('<int:pk>/area-delete-all-boxes', AreaDeleteAllBoxesView.as_view(), name='area-delete-all-boxes'),
    path('<int:pk>/area-add-boxes', AreaAddBoxesView.as_view(), name='area-add-boxes'),
    path('<int:pk>/area-info', AreaInfoView.as_view(), name='area-info'),
    path('areas-list/', AreaListView.as_view(), name='areas-list'),
    path('<int:pk>/area-boxes', AreaBoxesView.as_view(), name='area-boxes'),
    path('<int:pk>/area-update', AreaUpdateView.as_view(), name='area-update'),
    # BOXES
    path('box-create', BoxCreateView.as_view(), name='box-create'),
    path('<int:pk>/box-delete', BoxDeleteView.as_view(), name='box-delete'),
    path('<int:pk>/box-info', BoxInfoView.as_view(), name='box-info'),
    path('boxes-list/', BoxListView.as_view(), name='boxes-list'),
    path('<int:pk>/box-update', BoxUpdateView.as_view(), name='box-update'),
]
