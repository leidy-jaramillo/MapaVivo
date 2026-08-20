from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from perfiles.models import PerfilUsuario
from puntos.models import Ciudad, PuntoAfectado, TipoPunto
from reportes.models import ReporteNecesidad, SubcategoriaNecesidad


class DatosPuntoForm(forms.ModelForm):
    class Meta:
        model = PuntoAfectado
        fields = ('tipo_punto', 'nombre', 'descripcion', 'ciudad', 'poblacion_vulnerable', 'poblacion_total', 'direccion', 'barrio', 'comuna', 'latitud', 'longitud', 'nombre_contacto', 'telefono')
        widgets = {
            'latitud': forms.NumberInput(attrs={'step': '0.000001', 'readonly': True}),
            'longitud': forms.NumberInput(attrs={'step': '0.000001', 'readonly': True}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, gestor, commit=True):
        punto = super().save(commit=False)
        punto.gestor = gestor
        if commit:
            punto.save()
        return punto


class RegistroPuntoForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')
    nombre = forms.CharField(label='Nombre del punto', max_length=150)
    descripcion = forms.CharField(label='Descripción', required=False, widget=forms.Textarea(attrs={'rows': 3}))
    tipo_punto = forms.ModelChoiceField(label='Tipo de punto', queryset=TipoPunto.objects.all())
    ciudad = forms.ModelChoiceField(label='Ciudad', queryset=Ciudad.objects.all())
    poblacion_vulnerable = forms.ChoiceField(label='Población vulnerable', choices=PuntoAfectado.PoblacionVulnerable.choices)
    poblacion_total = forms.IntegerField(label='Población total', required=False, min_value=0)
    direccion = forms.CharField(label='Dirección', max_length=255)
    barrio = forms.CharField(label='Barrio', max_length=100, required=False)
    comuna = forms.CharField(label='Comuna', max_length=50, required=False)
    latitud = forms.DecimalField(label='Latitud', max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'step': '0.000001', 'readonly': True}))
    longitud = forms.DecimalField(label='Longitud', max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'step': '0.000001', 'readonly': True}))
    nombre_contacto = forms.CharField(label='Nombre de contacto', max_length=150)
    telefono = forms.CharField(label='Teléfono', max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {'username': 'Nombre de usuario'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Será usado para iniciar sesión.'

    @transaction.atomic
    def save(self):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data['email']
        usuario.save()
        perfil = usuario.perfil
        perfil.rol = PerfilUsuario.Rol.GESTOR
        perfil.save(update_fields=['rol'])
        PuntoAfectado.objects.create(
            gestor=usuario,
            tipo_punto=self.cleaned_data['tipo_punto'],
            estado_verificacion=PuntoAfectado.EstadoVerificacion.PENDIENTE,
            nombre=self.cleaned_data['nombre'], descripcion=self.cleaned_data['descripcion'],
            direccion=self.cleaned_data['direccion'], barrio=self.cleaned_data['barrio'], comuna=self.cleaned_data['comuna'],
            ciudad=self.cleaned_data['ciudad'], poblacion_vulnerable=self.cleaned_data['poblacion_vulnerable'], poblacion_total=self.cleaned_data['poblacion_total'],
            latitud=self.cleaned_data['latitud'], longitud=self.cleaned_data['longitud'],
            nombre_contacto=self.cleaned_data['nombre_contacto'], telefono=self.cleaned_data['telefono'],
        )
        return usuario

class RegistroNecesidadForm(forms.ModelForm):
    class Meta:
        model = ReporteNecesidad
        fields = ('punto', 'categoria', 'subcategoria', 'necesidad_texto', 'observacion')
        widgets = {
            'necesidad_texto': forms.Textarea(attrs={'rows': 4}),
            'observacion': forms.Textarea(attrs={'rows': 3}),
            'fecha_realizacion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, gestor, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['punto'].queryset = PuntoAfectado.objects.filter(gestor=gestor).order_by('nombre')
        categoria_id = self.data.get('categoria') or self.initial.get('categoria')
        if categoria_id:
            self.fields['subcategoria'].queryset = SubcategoriaNecesidad.objects.filter(
                categoria_id=categoria_id
            ).order_by('nombre')
        else:
            self.fields['subcategoria'].queryset = SubcategoriaNecesidad.objects.none()
