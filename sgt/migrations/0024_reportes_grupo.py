# Generated by Django 4.1 on 2022-12-08 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0023_alter_reportes_fechadeenvio'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportes',
            name='grupo',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='sgt.grupo'),
            preserve_default=False,
        ),
    ]