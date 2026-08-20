from django.contrib import admin

from .models import Ciudad, PuntoAfectado, TipoPunto


@admin.register(TipoPunto)
class TipoPuntoAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(PuntoAfectado)
class PuntoAfectadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_punto', 'ciudad', 'gestor', 'estado_verificacion')
    list_filter = ('tipo_punto', 'ciudad', 'estado_verificacion', 'poblacion_vulnerable')
    search_fields = ('nombre', 'direccion', 'barrio', 'nombre_contacto')
    autocomplete_fields = ('gestor', 'tipo_punto', 'ciudad')