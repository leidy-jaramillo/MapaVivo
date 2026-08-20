from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class PerfilUsuario(models.Model):
    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        GESTOR = 'GESTOR', 'Gestor de albergue'
        DONANTE = 'DONANTE', 'Donante'

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
    )
    rol = models.CharField(
        max_length=10,
        choices=Rol.choices,
        default=Rol.DONANTE,
    )

    class Meta:
        verbose_name = 'perfil de usuario'
        verbose_name_plural = 'perfiles de usuario'

    def clean(self):
        if self.rol == self.Rol.ADMIN and not self.usuario.is_superuser:
            raise ValidationError(
                {'rol': 'El rol Administrador solo puede asignarse a un superusuario.'}
            )

    def __str__(self):
        return f'{self.usuario.get_username()} - {self.get_rol_display()}'