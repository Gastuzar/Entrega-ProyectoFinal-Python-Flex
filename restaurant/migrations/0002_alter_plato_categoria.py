# Generated by Django 5.1.4 on 2024-12-10 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plato',
            name='categoria',
            field=models.CharField(choices=[('principal', 'Plato Principal'), ('guarnicion', 'Guarnicion'), ('postre', 'Postre')], max_length=20),
        ),
    ]
