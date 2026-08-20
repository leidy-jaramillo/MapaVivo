from django.contrib import admin

from .models import CategoriaNecesidad, ReporteNecesidad, SubcategoriaNecesidad


@admin.register(CategoriaNecesidad)
class CategoriaNecesidadAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(SubcategoriaNecesidad)
class SubcategoriaNecesidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)
    autocomplete_fields = ('categoria',)


@admin.register(ReporteNecesidad)
class ReporteNecesidadAdmin(admin.ModelAdmin):
    list_display = ('id_reporte', 'punto', 'categoria', 'subcategoria', 'estado', 'fecha_realizacion')
    list_filter = ('estado', 'categoria', 'subcategoria', 'fecha_realizacion')
    search_fields = ('punto__nombre', 'necesidad_texto', 'observacion')
    autocomplete_fields = ('punto', 'categoria', 'subcategoria')