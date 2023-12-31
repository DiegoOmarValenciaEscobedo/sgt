# Generated by Django 4.1 on 2022-12-07 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0020_merge_20221207_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='tipouser',
            field=models.CharField(choices=[('T_S', 'Tutorado sin perfil'), ('T_O', 'Tutorado'), ('T_R', 'Tutor'), ('JDE', 'Jefe de departamento academico'), ('CDT', 'Coordinador de tutoria (departamento academico)'), ('CIT', 'Coordinacion institucional de tutoria'), ('JDO', 'Jefe de docencia (Creditos complementarios)'), ('SUB', 'Subdirector'), ('PSI', 'Psicologo'), ('MED', 'Medico'), ('ADM', 'Administrador')], default='TU', max_length=3),
        ),
    ]
