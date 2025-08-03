from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import TrainingReqForm
from .models import Training, TrainingReq, Student
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date


def create_training_request(request, training_id):
    training = get_object_or_404(Training, id=training_id)
    if training.status != "open":
        messages.warning(request, "Запись на эту тренировку закрыта.")

    if request.method == "POST":
        form = TrainingReqForm(request.POST, training=training)

        if form.is_valid():
            telegram_id = request.POST.get("telegram_id")
            student = Student.objects.get(tg_id=telegram_id)
            if TrainingReq.objects.filter(student=student, training=training).exists():
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
        form = TrainingReqForm(training=training)

    return render(
        request, "training_req_form.html", {"form": form, "training": training}
    )


@csrf_exempt
def create_student(request):
    if request.method == "POST":
        data = json.loads(request.body)
        telegram_id = data.get("id")
        name = data.get("first_name", "") + data.get("last_name", "")
        username = data.get("username", "")

        student, created = Student.objects.get_or_create(
            tg_id=telegram_id, tg_name=username, name=name
        )

        return JsonResponse({"created": created, "student_id": student.id})
    return JsonResponse({"error": "Invalid method"}, status=405)


class OpenTrainings(ListView):
    model = Training
    template_name = "open_trainings.html"

    def get_queryset(self):
        return Training.objects.filter(status="open", date__gte=date.today())
