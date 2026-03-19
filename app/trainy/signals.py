from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Training
from .tg import telegram

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
