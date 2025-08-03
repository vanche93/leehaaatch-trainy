from django.urls import path
from django.shortcuts import render
from .views import create_training_request, create_student, OpenTrainings

urlpatterns = [
    path("", OpenTrainings.as_view(), name="list_open_trainings"),
    path(
        "training-request/<int:training_id>/",
        create_training_request,
        name="create_training_req",
    ),
    path("create_student/", create_student, name="create_student"),
]
