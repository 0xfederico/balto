from django.urls import path, re_path

from activities.views import ActivityCreateView, ActivityDeleteView, ActivityInfoView, ActivityListView, \
    ActivityUpdateView, EventCreateView, EventDeleteView, EventInfoView, DayActivitiesView, EventUpdateView, SearchView

app_name = 'activities'

urlpatterns = [
    # ACTIVITIES
    path('activity-create', ActivityCreateView.as_view(), name='activity-create'),
    path('<int:pk>/activity-delete', ActivityDeleteView.as_view(), name='activity-delete'),
    path('<int:pk>/activity-info', ActivityInfoView.as_view(), name='activity-info'),
    path('activities-list/', ActivityListView.as_view(), name='activities-list'),
    path('<int:pk>/activity-update', ActivityUpdateView.as_view(), name='activity-update'),

    # EVENTS
    path('event-create', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/event-delete', EventDeleteView.as_view(), name='event-delete'),
    path('<int:pk>/event-info', EventInfoView.as_view(), name='event-info'),
    path('events-list/', DayActivitiesView.as_view(), name='events-list-day'),
    re_path(r'^events-list/(?P<date>\d{4}-\d{2}-\d{2})$', DayActivitiesView.as_view(), name='events-list-day'),
    path('<int:pk>/event-update', EventUpdateView.as_view(), name='event-update'),

    # SEARCH
    path('search', SearchView.as_view(), name='search'),
]
