# Generated by Django 4.2.5 on 2024-04-29 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelMVP', '0003_habitaciones_imagen_1_habitaciones_imagen_2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habitaciones',
            name='capacidad',
        ),
        migrations.RemoveField(
            model_name='habitaciones',
            name='imagen_1',
        ),
        migrations.RemoveField(
            model_name='habitaciones',
            name='imagen_2',
        ),
        migrations.RemoveField(
            model_name='habitaciones',
            name='imagen_3',
        ),
        migrations.AddField(
            model_name='habitaciones',
            name='ubicacion',
            field=models.CharField(choices=[('Norponiente', 'Norponiente'), ('Nororiente', 'Nororiente'), ('Surponiente', 'Surponiente'), ('Suroriente', 'Suroriente')], default='Norponiente', max_length=20),
            preserve_default=False,
        ),
    ]