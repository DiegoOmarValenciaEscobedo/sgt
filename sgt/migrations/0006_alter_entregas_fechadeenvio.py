# Generated by Django 4.1.2 on 2022-11-12 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0005_alter_entregas_fechadeenvio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregas',
            name='fechaDeEnvio',
            field=models.DateField(blank=True),
        ),
    ]
