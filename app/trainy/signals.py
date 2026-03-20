from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from .models import Training
from .tg import telegram

@receiver(pre_save, sender=Training)
def check_training_open(sender, instance, **kwargs):
    old_status = Training.objects.get(pk=instance.pk).status if instance.pk else None
    print(old_status, instance.status)
    if (
        old_status
        and instance.status == "open"
        and old_status != "open"
    ):
        telegram.send_open_message(instance)

@receiver(m2m_changed, sender=Training.topics.through)
@receiver(m2m_changed, sender=Training.training_times.through)
def check_training_open_m2m(sender, instance, **kwargs):
    if (
        instance.status == "open"
        and instance.topics.exists()
        and instance.training_times.exists()
    ):
        telegram.send_open_message(instance)
