from email.policy import default
from enum import unique
from random import choices
from secrets import choice
from tabnanny import verbose
from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import datetime
from PIL import Image

from django.dispatch import receiver
from django.db.models.signals import post_save

class MyUserManager(BaseUserManager):
    def create_user(self, email, idTec, password=None):
        if "@morelia.tecnm.mx" in email:
            user = self.model(
                email=self.normalize_email(email)
            )
        else:
            raise ValueError('Error: El correo debe tener morelia.tecnm.mx de dominio.')
        user.set_password(password)

        user.idTec = idTec
        user.date_created= datetime.now()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, idTec, nombre, aPaterno, aMaterno, password=None):
        if "@morelia.tecnm.mx" in email:
            user = self.model(
                email=self.normalize_email(email)
            )
        else:
            raise ValueError('Error: El correo debe tener morelia.tecnm.mx de dominio.')
        user.set_password(password)

        user.idTec = idTec
        user.nombre = nombre
        user.aPaterno = aPaterno
        user.aMaterno = aMaterno
        user.tipouser = 'ADM'

        user.date_created= datetime.now()

        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='Correo electronico', max_length=128, unique=True)
    date_created = models.CharField(max_length = 30)
    idTec = models.CharField(verbose_name='No. Control o RFC', max_length = 13)
    nombre = models.CharField(verbose_name='Nombre(s)', max_length = 35, null=True)
    aPaterno = models.CharField(verbose_name='Apellido Paterno', max_length = 35, null=True)
    aMaterno = models.CharField(verbose_name='Apellido Materno', max_length = 35, null=True)
    telefono = models.CharField(verbose_name='Telefono', max_length = 10, null=True)
    fotoDePerfil = models.ImageField(default='default_pic.jpg', upload_to='profile_pics')

    GENEROS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('NB', 'No Binario'),
    )
    genero = models.CharField(max_length=2, choices=GENEROS, null=True)
    TIPOUSER = (
        ('T_S', 'Tutorado sin perfil'),
        ('T_O', 'Tutorado'),
        ('T_R', 'Tutor'),
        ('JDE', 'Jefe de departamento academico'),
        ('CDT', 'Coordinador de tutoria (departamento academico)'),
        ('CIT', 'Coordinacion institucional de tutoria'),
        ('JDO', 'Jefe de docencia (Creditos complementarios)'),
        ('SUB', 'Subdirector'),
        ('PSI', 'Psicologo'),
        ('MED', 'Medico'),
        ('ADM', 'Administrador'),
    )
    tipouser = models.CharField(max_length=3, choices=TIPOUSER, default='TU')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['idTec', 'nombre', 'aPaterno', 'aMaterno'] #Quitar si da error al crear usuarios sin nombres y apellidos

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.fotoDePerfil.path)

        if img.height > img.width:
            half = img.height / 2
            upPoint = half - img.width / 2
            doPoint = half + img.width / 2
            (left, upper, right, lower) = (0, upPoint, img.width, doPoint)
        else:
            half = img.width / 2
            lePoint = half - img.height / 2
            riPoint = half + img.height / 2
            (left, upper, right, lower) = (lePoint, 0, riPoint, img.height)

        img = img.crop((left, upper, right, lower))
        output_size = (256,256)
        img = img.resize(output_size, reducing_gap=1)
        img.filename = self.email
        #Agregar metodo para borrar foto anterior
        img.save(self.fotoDePerfil.path)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

ENTIDADES = (
    ('AGU', 'Aguascalientes'),
    ('BCN', 'Baja California'),
    ('BCS', 'Baja California Sur'),
    ('CAM', 'Campeche'),
    ('CHP', 'Chiapas'),
    ('CHH', 'Chihuahua'),
    ('COA', 'Coahuila'),
    ('COL', 'Colima'),
    ('DIF', 'Distrito Federal'),
    ('DUR', 'Durango'),
    ('GUA', 'Guanajuato'),
    ('GRO', 'Guerrero'),
    ('HID', 'Hidalgo'),
    ('JAL', 'Jalisco'),
    ('MIC', 'Michoacán'),
    ('MOR', 'Morelos'),
    ('MEX', 'Estado de México'),
    ('NAY', 'Nayarit'),
    ('NLE', 'Nuevo León'),
    ('OAX', 'Oaxaca'),
    ('PUE', 'Puebla'),
    ('QUE', 'Querétaro'),
    ('ROO', 'Quintana Roo'),
    ('SLP', 'San Luis Potosí'),
    ('SIN', 'Sinaloa'),
    ('SON', 'Sonora'),
    ('TAB', 'Tabasco'),
    ('TAM', 'Tamaulipas'),
    ('TIA', 'Tlaxcala'),
    ('VER', 'Veracruz'),
    ('YUC', 'Yucatán'),
    ('ZAC', 'Zacatecas'),
)

ESTADO = (
    ('P', 'Pendiente'),
    ('E', 'Enviado'),
    ('R', 'Retrasado'),
)

class Tecnologico(models.Model):
    nombre = models.CharField(verbose_name = "Nombre del Tecnologico", max_length = 100, unique = True)
    entidadFed = models.CharField(max_length=3, choices=ENTIDADES, null=True, verbose_name = 'Entidad Federativa')

    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    tecnologico = models.ForeignKey(Tecnologico, on_delete = models.CASCADE, verbose_name='Tecnologico al que pertenece')
    nombre = models.CharField(max_length = 75, verbose_name='Depertamento')

    def __str__(self):
        return self.nombre

class Carrera(models.Model):
    tecnologico = models.ForeignKey(Tecnologico, on_delete = models.CASCADE, verbose_name='Tecnologico')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, verbose_name='Departamento')
    nombre = models.CharField(max_length = 75, verbose_name='Carrera')
    nomenclatura = models.CharField(max_length = 3, verbose_name='Nomenclatura')

    def __str__(self):
        return self.nombre

class Personal(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, verbose_name='Email')
    campus = models.CharField(max_length=50, null=True)
    localizacion = models.CharField(max_length=50, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.user.nombre:
            return self.user.idTec + " - " + self.user.nombre
        else:
            return self.user.idTec

class Archivo(models.Model):
    ruta = models.CharField(max_length = 75)

class Reportes(models.Model):
    personal = models.ForeignKey(Personal, on_delete = models.CASCADE)
    archivo = models.ForeignKey(Archivo, on_delete = models.CASCADE)
    estado = models.CharField(max_length=1, choices=ESTADO)
    fechaLimite = models.DateField()
    fechaDeEnvio = models.DateField()

class Grupo(models.Model):
    nombre = models.CharField(max_length=13)    
    constancia = models.ForeignKey(Archivo, on_delete = models.SET_NULL, null=True)
    reporte = models.ForeignKey(Reportes, on_delete = models.SET_NULL, null= True)

class Personal_Carrera(models.Model):
    personal = models.ForeignKey(Personal, on_delete = models.SET_NULL, null = True)
    carrera = models.ForeignKey(Carrera, on_delete = models.SET_NULL, null = True)
    grupo = models.ForeignKey(Grupo, on_delete = models.SET_NULL, null = True)
    activo = models.BooleanField(default=True)

class Tutorado(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    fechaDeNacimiento = models.DateField(null = True)
    curp = models.CharField(max_length=18, null = True)
    ESTADOCIVIL = (
        ('SO', 'Soltero'),
        ('CA', 'Casado'),
    )
    estadoCivil = models.CharField(max_length=2, choices=ESTADOCIVIL, null=True)
    nss = models.CharField(max_length=15, null=True)
    observaciones = models.TextField(null=True)
    carrera = models.ForeignKey(Carrera, on_delete = models.SET_NULL, null=True, default=7)
    semestre = models.IntegerField(null=True)
    ESTATUS = (
        ('ACT', 'Activo'),
        ('EXP', 'Expulsado'),
    )
    estatus = models.CharField(max_length=3, choices=ESTATUS, null=True)
    entidadFed = models.CharField(max_length=3, choices=ENTIDADES, null=True)
    municipio = models.CharField(max_length=50, null=True)
    domicilio = models.CharField(max_length=50, null=True)
    cp = models.IntegerField(null=True)
    contactConfianza = models.CharField(max_length=50, null=True)
    tecDeProcedencia = models.IntegerField(null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.user.nombre:
            return self.user.idTec + " - " + self.user.aPaterno + " " + self.user.aMaterno + " " + self.user.nombre
        else:
            return self.user.idTec

class Actividad(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE)
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    fechaDeAsignacion = models.DateField()
    fechaDeCierre = models.DateField()

class Actividad_Archivo(models.Model):
    archivo = models.ForeignKey(Archivo, on_delete = models.SET_NULL, null=True)
    actividad = models.ForeignKey(Actividad, on_delete = models.CASCADE)

class Entregas(models.Model):
    tutorado = models.ForeignKey(Tutorado, on_delete=models.SET_NULL, null=True)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    estado = models.CharField(max_length=1, choices=ESTADO)
    fechaDeEnvio = models.DateField(null=True, blank=True)

class Entregas_Archivo(models.Model):
    archivo = models.ForeignKey(Archivo, on_delete = models.SET_NULL, null=True)
    entregas = models.ForeignKey(Entregas, on_delete = models.CASCADE)

class Citas(models.Model):
    tutorado = models.ForeignKey(Tutorado, on_delete=models.SET_NULL, null=True)
    personal = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True)
    TIPOCITAS = (
        ('P', 'Psicologo'),
        ('M', 'Medico'),
    )
    tipo = models.CharField(max_length=1, choices=TIPOCITAS)
    motivos = models.CharField(max_length=256)
    descripcion = models.TextField()
    descripcionCita = models.TextField(null=True)
    fechaDeCita = models.DateField(null=True)
    fechaDeCreacion = models.DateField()

class Curso(models.Model):
    nombre = models.CharField(max_length=75)
    fecha = models.DateField()
    encargado = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True)
    cantTutorados = models.IntegerField()
    folio = models.CharField(max_length=20, default=0)
    valor = models.FloatField(default=0)

class CursoPendiente(models.Model):
    folio = models.CharField(max_length=20, default=0)

class CreditosTutorado(models.Model):    
    tutorado = models.ForeignKey(Tutorado, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)
    cursoPendiente = models.ForeignKey(CursoPendiente, on_delete=models.SET_NULL, null=True)
    ruta = models.ForeignKey(Archivo, on_delete = models.SET_NULL, null=True)
    ESTADOCREDITO = (
        ('1', 'En espera'),
        ('2', 'Aceptado'),
        ('3', 'Rechazado'),
    )
    estado = models.CharField(max_length=1, choices=ESTADOCREDITO)
    fechaDeEnvio = models.DateField()

class Creditos(models.Model):
    creditostutorado = models.OneToOneField(CreditosTutorado, on_delete = models.CASCADE)
    fechaDeValidacion = models.DateField()
    personal = models.ForeignKey(Personal, on_delete = models.SET_NULL, null=True, verbose_name='Quien valido')
    
class QuejaSugerencia(models.Model):
    texto = models.TextField()
    ESTADOQUEJA = (
        ('L', 'Leido'),
        ('N', 'No Leido'),
    )
    estado = models.CharField(max_length = 1, choices=ESTADOQUEJA)
    fechaDeCreacion = models.DateField()

class Periodo(models.Model):
    fechaInicio = models.DateField()
    fechaTermina = models.DateField()
    TIPODEPERIODO = (
        ('1', 'Invierno'),
        ('2', 'Otoño'),
        ('3', 'Verano'),
    )
    tipoPeriodo = models.CharField(max_length= 1, choices=TIPODEPERIODO)

class ReporteTutor(models.Model):
    noControl = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, null=True)
    Tutor = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.SET_NULL, null=True)
    tutoGrupal =  models.IntegerField(null=True)
    tutoIndividual =  models.IntegerField(null=True)
    canalizados =  models.IntegerField(null=True)
    observaciones = models.CharField(max_length=200, null=True)
    asistencia = models.IntegerField(null=True)

class ReporteJDA(models.Model):
    tutor = models.ForeignKey(Personal_Carrera, on_delete= models.SET_NULL, null=True)
    jda = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True)
    tutoGrupal =  models.IntegerField()
    tutoIndividual =  models.IntegerField()
    canalizados =  models.IntegerField()
    area = models.CharField(max_length=30, null=True)

@receiver(post_save, sender=MyUser)
def create_user_profile(sender, instance, created, **kwargs): #Funcion para crear tipo de usuario
    if created:
        if instance.tipouser == 'T_O' or instance.tipouser == 'T_S':
            Tutorado.objects.create(user=instance, estatus='ACT')
        else:
            Personal.objects.create(user=instance)