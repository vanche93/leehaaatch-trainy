from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import TrainingReqForm
from .models import Training, TrainingReq, Student
from django.contrib import messages
from datetime import date
from django.conf import settings
from telegram_webapp_auth.auth import TelegramAuthenticator


def get_or_create_student(auth_cred):
    telegram_authenticator = TelegramAuthenticator(settings.TELEGRAM_SECRET_KEY)
    init_data = telegram_authenticator.validate(auth_cred)
    name_parts = [init_data.user.first_name, init_data.user.last_name]
    name = " ".join(part for part in name_parts if part)
    student, created = Student.objects.update_or_create(
        tg_id=init_data.user.id,
        defaults={"tg_name": init_data.user.username, "name": name},
    )
    return student


def create_training_request(request, training_id):
    training = get_object_or_404(Training, id=training_id)
    if training.status != "open":
        messages.warning(request, "Запись на эту тренировку закрыта.")

    if request.method == "POST":
        form = TrainingReqForm(request.POST, training=training)

        if form.is_valid():
            if request.POST.get("tg_init_data"):
                student = get_or_create_student(request.POST.get("tg_init_data"))
                if TrainingReq.objects.filter(
                    student=student, training=training
                ).exists():
                    messages.warning(request, "Вы уже записаны на эту тренировку!")
                    return redirect(request.path)
                else:
                    training_req = form.save(commit=False)
                    training_req.training = training
                    training_req.student = student
                    training_req.save()
                    form.save_m2m()
                    messages.success(request, "Запрос на тренировку отправлен!")
                    return redirect(request.path)
            else:
                messages.warning(request, "Ошибка авторизации")
                return redirect(request.path)
    else:
        form = TrainingReqForm(training=training)

    return render(
        request, "training_req_form.html", {"form": form, "training": training}
    )


class OpenTrainings(ListView):
    model = Training
    template_name = "open_trainings.html"

    def get_queryset(self):
        return Training.objects.filter(status="open", date__gte=date.today())
