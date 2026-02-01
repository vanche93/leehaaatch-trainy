from django.urls import path
from .views import create_training_request

urlpatterns = [
    path(
        "",
        create_training_request,
        name="create_training_req",
    ),
    path(
        "training-request/<int:training_id>/",
        create_training_request,
        name="create_training_req",
    ),
]
