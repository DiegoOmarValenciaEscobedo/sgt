# Generated by Django 4.1 on 2022-12-05 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0015_remove_creditostutorado_folio_curso_folio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditostutorado',
            name='valor',
        ),
        migrations.AddField(
            model_name='curso',
            name='valor',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='curso',
            name='encargado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sgt.personal'),
        ),
    ]
