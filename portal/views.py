from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from perfiles.models import PerfilUsuario
from puntos.models import PuntoAfectado
from reportes.models import ReporteNecesidad, SubcategoriaNecesidad
from .forms import DatosPuntoForm, RegistroNecesidadForm, RegistroPuntoForm

class InicioView(View):
    template_name = 'portal/inicio.html'
    def get(self, request):
        activos = ReporteNecesidad.objects.exclude(estado=ReporteNecesidad.EstadoAtencion.ATENDIDO).select_related('categoria', 'subcategoria')
        puntos = PuntoAfectado.objects.select_related('ciudad', 'tipo_punto').prefetch_related(Prefetch('reportes_necesidades', queryset=activos))
        datos = []
        for p in puntos:
            necesidades = [{
                'categoria': r.categoria.nombre,
                'subcategoria': r.subcategoria.nombre,
                'detalle': r.necesidad_texto,
                'observacion': r.observacion,
                'estado': r.get_estado_display(),
                'fecha': r.fecha_realizacion.isoformat(),
            } for r in p.reportes_necesidades.all()[:3]]
            datos.append({'nombre': p.nombre, 'tipo': p.tipo_punto.nombre, 'direccion': p.direccion, 'barrio': p.barrio, 'comuna': p.comuna, 'ciudad': p.ciudad.nombre, 'latitud': float(p.latitud), 'longitud': float(p.longitud), 'estado': p.get_estado_verificacion_display(), 'necesidades': necesidades})
        return render(request, self.template_name, {'puntos_mapa': datos})

class RegistroPuntoView(View):
    template_name = 'portal/registro_punto.html'
    def get(self, request):
        if request.user.is_authenticated and request.user.perfil.rol == PerfilUsuario.Rol.GESTOR:
            return render(request, self.template_name, {'form': DatosPuntoForm(), 'crear_cuenta': False})
        return render(request, self.template_name, {'form': RegistroPuntoForm(), 'crear_cuenta': True})
    def post(self, request):
        if request.user.is_authenticated and request.user.perfil.rol == PerfilUsuario.Rol.GESTOR:
            form = DatosPuntoForm(request.POST)
            if form.is_valid():
                form.save(gestor=request.user); messages.success(request, 'El punto fue registrado y está pendiente de confirmación.'); return redirect('perfil')
            return render(request, self.template_name, {'form': form, 'crear_cuenta': False})
        form = RegistroPuntoForm(request.POST)
        if form.is_valid():
            usuario = form.save(); login(request, usuario); messages.success(request, 'Tu punto fue registrado y está pendiente de confirmación.'); return redirect('perfil')
        return render(request, self.template_name, {'form': form, 'crear_cuenta': True})

class EditarPuntoView(LoginRequiredMixin, View):
    template_name = 'portal/registro_punto.html'
    def get(self, request, punto_id):
        punto = get_object_or_404(PuntoAfectado, pk=punto_id, gestor=request.user)
        return render(request, self.template_name, {'form': DatosPuntoForm(instance=punto), 'crear_cuenta': False, 'modo_edicion': True})
    def post(self, request, punto_id):
        punto = get_object_or_404(PuntoAfectado, pk=punto_id, gestor=request.user)
        form = DatosPuntoForm(request.POST, instance=punto)
        if form.is_valid():
            form.save(gestor=request.user); messages.success(request, 'Los datos del punto fueron actualizados.'); return redirect('perfil')
        return render(request, self.template_name, {'form': form, 'crear_cuenta': False, 'modo_edicion': True})

class PerfilView(LoginRequiredMixin, View):
    template_name = 'portal/perfil.html'
    def get(self, request):
        reportes = ReporteNecesidad.objects.select_related('categoria', 'subcategoria').order_by('-fecha_realizacion')
        puntos = PuntoAfectado.objects.filter(gestor=request.user).select_related('tipo_punto', 'ciudad').prefetch_related(Prefetch('reportes_necesidades', queryset=reportes))
        return render(request, self.template_name, {'puntos': puntos, 'perfil': request.user.perfil, 'estados_necesidad': ReporteNecesidad.EstadoAtencion.choices})

class RegistroNecesidadView(LoginRequiredMixin, View):
    template_name = 'portal/registro_necesidad.html'
    def get(self, request):
        if not PuntoAfectado.objects.filter(gestor=request.user).exists():
            messages.info(request, 'Debes tener al menos un punto registrado para reportar una necesidad.'); return redirect('perfil')
        return render(request, self.template_name, {'form': RegistroNecesidadForm(gestor=request.user)})
    def post(self, request):
        form = RegistroNecesidadForm(request.POST, gestor=request.user)
        if form.is_valid(): form.save(); messages.success(request, 'La necesidad fue registrada correctamente.'); return redirect('perfil')
        return render(request, self.template_name, {'form': form})

class ActualizarEstadoNecesidadView(LoginRequiredMixin, View):
    def post(self, request, reporte_id):
        reporte = get_object_or_404(ReporteNecesidad, pk=reporte_id, punto__gestor=request.user)
        estado = request.POST.get('estado')
        if estado in {valor for valor, _ in ReporteNecesidad.EstadoAtencion.choices}:
            reporte.estado = estado; reporte.save(update_fields=['estado']); messages.success(request, 'El estado de la necesidad fue actualizado.')
        else: messages.error(request, 'El estado seleccionado no es válido.')
        return redirect('perfil')

def subcategorias_por_categoria(request, categoria_id):
    items = SubcategoriaNecesidad.objects.filter(categoria_id=categoria_id).order_by('nombre')
    return JsonResponse({'subcategorias': [{'id': item.id, 'nombre': item.nombre} for item in items]})