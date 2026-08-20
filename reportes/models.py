from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from puntos.models import PuntoAfectado


class CategoriaNecesidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'categoría de necesidad'
        verbose_name_plural = 'categorías de necesidad'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre


class SubcategoriaNecesidad(models.Model):
    categoria = models.ForeignKey(
        CategoriaNecesidad,
        on_delete=models.PROTECT,
        related_name='subcategorias',
    )
    nombre = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'subcategoría de necesidad'
        verbose_name_plural = 'subcategorías de necesidad'
        ordering = ('categoria__nombre', 'nombre')
        constraints = [
            models.UniqueConstraint(
                fields=('categoria', 'nombre'),
                name='subcategoria_unica_por_categoria',
            ),
        ]

    def __str__(self):
        return f'{self.categoria}: {self.nombre}'


class ReporteNecesidad(models.Model):
    class EstadoAtencion(models.TextChoices):
        SIN_ATENDER = 'SIN_ATENDER', 'Sin atender'
        EN_PROCESO = 'EN_PROCESO', 'En proceso'
        ATENDIDO_PARCIALMENTE = 'ATENDIDO_PARCIAL', 'Atendido parcialmente'
        ATENDIDO = 'ATENDIDO', 'Atendido'

    id_reporte = models.BigAutoField(primary_key=True)
    punto = models.ForeignKey(
        PuntoAfectado,
        on_delete=models.CASCADE,
        related_name='reportes_necesidades',
    )
    estado = models.CharField(
        'estado de atención',
        max_length=20,
        choices=EstadoAtencion.choices,
        default=EstadoAtencion.SIN_ATENDER,
    )
    categoria = models.ForeignKey(
        CategoriaNecesidad,
        on_delete=models.PROTECT,
        related_name='reportes',
    )
    subcategoria = models.ForeignKey(
        SubcategoriaNecesidad,
        on_delete=models.PROTECT,
        related_name='reportes',
    )
    necesidad_texto = models.TextField('necesidad')
    observacion = models.TextField('observación', blank=True)
    fecha_realizacion = models.DateTimeField('fecha de registro', auto_now_add=True)

    class Meta:
        verbose_name = 'reporte de necesidad'
        verbose_name_plural = 'reportes de necesidades'
        ordering = ('-fecha_realizacion', '-id_reporte')

    def clean(self):
        super().clean()
        if self.categoria_id and self.subcategoria_id:
            if self.subcategoria.categoria_id != self.categoria_id:
                raise ValidationError(
                    {'subcategoria': 'La subcategoría seleccionada no pertenece a la categoría.'}
                )

    def __str__(self):
        return f'{self.punto} - {self.subcategoria}'