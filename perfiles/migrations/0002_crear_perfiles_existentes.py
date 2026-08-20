from django.db import migrations


def crear_perfiles_existentes(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    PerfilUsuario = apps.get_model('perfiles', 'PerfilUsuario')

    for usuario in User.objects.all():
        PerfilUsuario.objects.get_or_create(
            usuario_id=usuario.pk,
            defaults={'rol': 'ADMIN' if usuario.is_superuser else 'DONANTE'},
        )


class Migration(migrations.Migration):
    dependencies = [
        ('perfiles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_perfiles_existentes, migrations.RunPython.noop),
    ]