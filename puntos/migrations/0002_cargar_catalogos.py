from django.db import migrations


TIPOS_PUNTO = (
    'Albergue',
    'Centro de acopio',
    'Edificio colapsado',
    'Rescate y logística',
)

CIUDADES = (
    'Cali',
    'Yumbo',
    'Dagua',
    'Buenaventura',
    'Calima',
    'San Bernardo',
)


def cargar_catalogos(apps, schema_editor):
    TipoPunto = apps.get_model('puntos', 'TipoPunto')
    Ciudad = apps.get_model('puntos', 'Ciudad')

    for nombre in TIPOS_PUNTO:
        TipoPunto.objects.get_or_create(nombre=nombre)
    for nombre in CIUDADES:
        Ciudad.objects.get_or_create(nombre=nombre)


class Migration(migrations.Migration):
    dependencies = [
        ('puntos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_catalogos, migrations.RunPython.noop),
    ]