from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TipoPunto(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tipo de punto'
        verbose_name_plural = 'tipos de punto'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'ciudad'
        verbose_name_plural = 'ciudades'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre


class PuntoAfectado(models.Model):
    class EstadoVerificacion(models.TextChoices):
        CONFIRMADO = 'CONFIRMADO', 'Confirmado'
        PENDIENTE = 'PENDIENTE', 'Pendiente de confirmar'

    class PoblacionVulnerable(models.TextChoices):
        NINGUNA = 'NINGUNA', 'Ninguna'
        ADULTO_MAYOR = 'ADULTO_MAYOR', 'Adulto mayor'
        INFANTES = 'INFANTES', 'Infantes'
        AMBOS = 'AMBOS', 'Adulto mayor e infantes'

    id_punto = models.BigAutoField(primary_key=True)
    gestor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='puntos_gestionados',
        limit_choices_to={'perfil__rol': 'GESTOR'},
    )
    tipo_punto = models.ForeignKey(TipoPunto, on_delete=models.PROTECT, related_name='puntos')
    estado_verificacion = models.CharField(
        max_length=12,
        choices=EstadoVerificacion.choices,
        default=EstadoVerificacion.PENDIENTE,
    )
    poblacion_vulnerable = models.CharField(max_length=20, choices=PoblacionVulnerable.choices)
    poblacion_total = models.PositiveIntegerField('Población total', null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, related_name='puntos')
    nombre = models.CharField('Punto afectado nombre', max_length=150)
    descripcion = models.TextField('Punto afectado descripción', blank=True)
    direccion = models.CharField('Dirección', max_length=255)
    barrio = models.CharField(max_length=100, blank=True)
    comuna = models.CharField(max_length=50, blank=True)
    latitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    nombre_contacto = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'punto afectado'
        verbose_name_plural = 'puntos afectados'
        ordering = ('nombre',)

    def clean(self):
        super().clean()
        perfil = getattr(self.gestor, 'perfil', None) if self.gestor_id else None
        if self.gestor_id and (not perfil or perfil.rol != 'GESTOR'):
            raise ValidationError({'gestor': 'El usuario seleccionado debe tener el rol Gestor de albergue.'})

    def __str__(self):
        return self.nombre