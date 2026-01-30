from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import TrainingReq, Training
from .tg import telegram


@receiver(m2m_changed, sender=TrainingReq.training_times.through)
@receiver(m2m_changed, sender=TrainingReq.topics.through)
def update_training_status(sender, instance, action, **kwargs):
    if (
        instance.training_times.exists()
        and instance.topics.exists()
        and action == "post_add"
    ):
        training = instance.training

        # Словарь для подсчета пар (время, тема)
        pair_counter = {}

        # Все запросы на эту тренировку
        all_reqs = TrainingReq.objects.filter(training=training)

        for req in all_reqs:
            for time in req.training_times.all():
                for topic in req.topics.all():
                    key = (time.id, topic.id)
                    pair_counter[key] = pair_counter.get(key, 0) + 1

                    # Если найдена комбинация, у которой кол-во запросов ≥ лимита — закрываем
                    if pair_counter[key] >= training.max_participants:
                        training.status = "full"
                        training.final_time = time
                        training.final_topic = topic
                        # Получаем список запросов с текущем временем и темой
                        filter_reqs = TrainingReq.objects.filter(
                            training=training, training_times=time, topics=topic
                        )
                        # Удаляем участников из тренировки
                        training.participants.clear()
                        for freq in filter_reqs:
                            # Добавляем участников из запросы в тренировку
                            training.participants.add(freq.student)
                        training.save()
                        return True
    return False


@receiver(post_save, sender=Training)
def check_training_completion(sender, instance, **kwargs):
    if instance.status == "full":
        telegram.send_close_message(instance)
        telegram.send_close_message_participants(instance)


@receiver(m2m_changed, sender=Training.topics.through)
@receiver(m2m_changed, sender=Training.training_times.through)
@receiver(post_save, sender=Training)
def check_training_open(sender, instance, **kwargs):
    if (
        instance.status == "open"
        and instance.topics.exists()
        and instance.training_times.exists()
    ):
        telegram.send_open_message(instance)
