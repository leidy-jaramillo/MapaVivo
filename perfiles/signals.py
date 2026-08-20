from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PerfilUsuario


@receiver(post_save, sender=get_user_model())
def crear_o_actualizar_perfil_usuario(sender, instance, created, **kwargs):
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=instance)

    if instance.is_superuser and perfil.rol != PerfilUsuario.Rol.ADMIN:
        perfil.rol = PerfilUsuario.Rol.ADMIN
        perfil.save(update_fields=['rol'])