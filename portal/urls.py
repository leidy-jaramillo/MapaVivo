from django.urls import path
from .views import ActualizarEstadoNecesidadView, EditarPuntoView, InicioView, PerfilView, RegistroNecesidadView, RegistroPuntoView, subcategorias_por_categoria
urlpatterns = [
    path('', InicioView.as_view(), name='inicio'), path('perfil/', PerfilView.as_view(), name='perfil'),
    path('registro-punto/', RegistroPuntoView.as_view(), name='registro_punto'), path('puntos/<int:punto_id>/editar/', EditarPuntoView.as_view(), name='editar_punto'),
    path('registro-necesidad/', RegistroNecesidadView.as_view(), name='registro_necesidad'), path('necesidades/<int:reporte_id>/estado/', ActualizarEstadoNecesidadView.as_view(), name='actualizar_estado_necesidad'),
    path('api/categorias/<int:categoria_id>/subcategorias/', subcategorias_por_categoria, name='subcategorias_por_categoria'), path('registro-albergue/', RegistroPuntoView.as_view(), name='registro_albergue'),
]