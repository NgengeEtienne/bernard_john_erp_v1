from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('', views.task_home, name='task-home'),
    path('add-task/', views.add_task.as_view(), name='add-task'),
    path('task-detail/<slug:slug>/',views.task_detail, name='task-detail'),
    path('edit-task/<int:pk>/', views.edit_task.as_view(), name='edit-task'),

]
