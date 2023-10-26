# Generated by Django 4.1 on 2022-11-30 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0008_carrera_nomenclatura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='tipouser',
            field=models.CharField(choices=[('T_O', 'Tutorado'), ('T_S', 'Tutorado sin perfil'), ('T_R', 'Tutor'), ('JDE', 'Jefe de departamento academico'), ('CDT', 'Coordinador de tutoria (departamento academico)'), ('CIT', 'Coordinacion institucional de tutoria'), ('JDO', 'Jefe de docencia (Creditos complementarios)'), ('SUB', 'Subdirector'), ('PSI', 'Psicologo'), ('MED', 'Medico')], default='TU', max_length=3),
        ),
    ]
