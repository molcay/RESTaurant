from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('<int:pk>/', views.RestaurantRetrieveUpdateDeleteView.as_view(), name='restaurant-retrieve-update-delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
