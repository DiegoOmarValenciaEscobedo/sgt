# Generated by Django 4.1 on 2022-11-29 05:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0007_alter_entregas_fechadeenvio'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrera',
            name='nomenclatura',
            field=models.CharField(default=django.utils.timezone.now, max_length=3, verbose_name='Nomenclatura'),
            preserve_default=False,
        ),
    ]
