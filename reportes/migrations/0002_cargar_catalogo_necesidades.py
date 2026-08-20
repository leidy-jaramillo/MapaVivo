from django.db import migrations


CATALOGO_NECESIDADES = (
    ('Alimentación', 'Alimentos no perecederos'),
    ('Alimentación', 'Comida preparada / refrigerios'),
    ('Alimentación', 'Agua potable'),
    ('Alimentación', 'Menaje de cocina'),
    ('Aseo e higiene', 'Aseo personal'),
    ('Aseo e higiene', 'Pañales'),
    ('Salud', 'Botiquín / insumos médicos'),
    ('Alojamiento temporal', 'Dotación de albergue'),
    ('Alojamiento temporal', 'Ropa de cama'),
    ('Vestuario', 'Ropa y calzado'),
    ('Iluminación', 'Linternas'),
    ('Energía', 'Equipos e instalaciones eléctricas'),
    ('Rescate / seguridad industrial', 'Elementos de protección personal'),
    ('Rescate / construcción', 'Herramientas de demolición y remoción'),
    ('Logística', 'Transporte de carga'),
    ('Comunicación / monitoreo', 'Equipos de comunicación y monitoreo'),
    ('Mobiliario', 'Mobiliario para comedor/punto'),
    ('Bienestar animal', 'Alimentación / rescate animal'),
    ('Infraestructura', 'Evaluación estructural'),
)


def cargar_catalogo_necesidades(apps, schema_editor):
    CategoriaNecesidad = apps.get_model('reportes', 'CategoriaNecesidad')
    SubcategoriaNecesidad = apps.get_model('reportes', 'SubcategoriaNecesidad')

    for categoria_nombre, subcategoria_nombre in CATALOGO_NECESIDADES:
        categoria, _ = CategoriaNecesidad.objects.get_or_create(nombre=categoria_nombre)
        SubcategoriaNecesidad.objects.get_or_create(
            categoria=categoria,
            nombre=subcategoria_nombre,
        )


class Migration(migrations.Migration):
    dependencies = [
        ('reportes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_catalogo_necesidades, migrations.RunPython.noop),
    ]