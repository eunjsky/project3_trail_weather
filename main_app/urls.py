from django.urls import path
from . import views


urlpatterns = [
    path('about/', views.about, name='about'),
    path('weathers/', views.weathers_index, name='weather_index'),
    path('weathers/<int:city_id>/', views.weathers_detail, name='details'),
    path('trails/', views.trails_index, name='index'),
    path('trails/<int:trail_id>/', views.trails_detail, name='detail'),
    path('trails/create/', views.TrailCreate.as_view(), name='trails_create'),
    path('trails/<int:pk>/update/',
         views.TrailUpdate.as_view(), name='trails_update'),
    path('trails/<int:pk>/delete/',
         views.TrailDelete.as_view(), name='trails_delete'),
    path('trails/<int:trail_id>/assoc_activity/<int:activity_id>/',
         views.assoc_activity, name='assoc_activity'),
    path('trails/<int:trail_id>/unassoc_activity/<int:activity_id>/',
         views.unassoc_activity, name='unassoc_activity'),
    path('accounts/signup/', views.signup, name='signup'),

]
