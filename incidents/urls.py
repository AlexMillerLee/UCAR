from django.urls import path
from . import views
app_name = "incidents"
urlpatterns = [
    path('get_all/', views.get_all_views, name='get_all'),
    path('update/', views.update_views, name='update'),
    path('create/', views.create_views, name='create'),

]
