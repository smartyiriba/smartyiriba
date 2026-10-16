from django.db import migrations


def retire_logistics(apps, schema_editor):
    database = schema_editor.connection.alias
    apps.get_model('catalog', 'Service').objects.using(database).filter(
        slug='logistique-services-operationnels',
    ).update(active=False)
    apps.get_model('catalog', 'Category').objects.using(database).filter(
        slug='location-services-operationnels',
    ).update(name='Location de salles & espaces')


class Migration(migrations.Migration):
    dependencies = [('catalog', '0001_initial')]
    operations = [migrations.RunPython(retire_logistics, migrations.RunPython.noop)]
