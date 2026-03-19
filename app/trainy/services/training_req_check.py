from ..models import TrainingReq, Training
from ..tg import telegram
from django.db import transaction


def check_reqs(training):
    with transaction.atomic():
        # блокируем строку training, чтобы параллельные worker не перекрывали друг друга
        training = Training.objects.select_for_update().get(pk=training.pk)

        # если уже закрыта/полная, больше ничего не делаем
        if training.status != "open":
            return

        pair_counter = {}
        # загружаем все заявки и связи
        all_reqs = (
            TrainingReq.objects.filter(training=training)
            .select_related("student")
            .prefetch_related("training_times", "topics")
        )

        # считаем количество заявок по (время, тема)
        for req in all_reqs:
            for time in req.training_times.all():
                for topic in req.topics.all():
                    key = (time.pk, topic.pk)
                    pair_counter[key] = pair_counter.get(key, 0) + 1

                    # если достигли max_participants, переводим тренировку в full
                    if pair_counter[key] >= training.max_participants:
                        training.status = "full"
                        training.final_time = time
                        training.final_topic = topic

                        # обновляем участников только для найденной пары время+тема
                        related_reqs = TrainingReq.objects.filter(
                            training=training,
                            training_times=time,
                            topics=topic,
                        ).select_related("student")

                        training.participants.clear()
                        for rr in related_reqs:
                            training.participants.add(rr.student)
                        training.save()
                        telegram.send_close_message(training)
                        telegram.send_close_message_participants(training)
                        telegram.send_notify_message_participants(training)
                        return
