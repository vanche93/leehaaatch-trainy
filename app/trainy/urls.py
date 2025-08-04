from django.urls import path
from .views import create_training_request, OpenTrainings

urlpatterns = [
    path("", OpenTrainings.as_view(), name="list_open_trainings"),
    path(
        "training-request/<int:training_id>/",
        create_training_request,
        name="create_training_req",
    ),
]
