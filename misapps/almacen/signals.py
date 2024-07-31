from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth.models import User

# Importa tus modelos
from .models.History import History
from .models.Equipment import Equipment 

@receiver(post_save, sender=Equipment)  # Cambia Equipment al modelo que necesites
def create_update_history(sender, instance, created, **kwargs):
    if created:
        action = 'Created'
    else:
        action = 'Updated'

    # Obtén el usuario logueado
    user = kwargs.get('user', None)
    if not user:
        user = User.objects.first()  # O alguna otra lógica para obtener el usuario, si está disponible

    # Crea el registro de historial
    History.objects.create(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.idEquipment,
        action=action,
        user=user,
        timestamp=timezone.now()
    )
