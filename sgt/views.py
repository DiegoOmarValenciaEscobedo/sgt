from multiprocessing import connection
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import transaction
from urllib import response
from django import template
from django.forms import formset_factory
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
#from django.contrib.auth.forms import AuthenticationForm
from sgt.formularios.accountManage import UserLoginForm
from sgt.formularios.coordInstitDeTutorias import crearPeriodo, crearCarrera, crearDepartamento
from django.contrib.auth import login, logout, authenticate
#Importar el formulario para el buzon de sugerencias
from .forms import AgregarQuejaSugerencia, agendarCitaPsicologo, TutoradoFirstLogin, cambiarFoto, enviarTarea, verDatosSolcitante, Eval_Diag, gruposDisponibles, crearGrupo, RechazarCursoPendiente, AgregarNuevoCurso
from sgt.models import Tecnologico, Tutorado, Personal , MyUser, Carrera, QuejaSugerencia, Grupo, Actividad, CreditosTutorado, Curso, Archivo, Entregas, Actividad_Archivo, Departamento,Personal_Carrera, Reportes, Citas, Entregas_Archivo, Periodo, CursoPendiente, Creditos, ReporteTutor, ReporteJDA
import calendar, os, zipfile
from os import remove
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit
from weasyprint import HTML
from calendar import HTMLCalendar
import re
from datetime import datetime
from .forms import CreateDate, AssignGroup, CreateActivity, CambiarPassword, CreditosComplementarios_tutorado, ReporteSemestral, ReporteJDA, editTutor, AddDocente, editTutorado, AddAl, cargarArchivo

# Create your views here.

@login_required
def index(request):
    if request.user.tipouser == 'T_S': #Cambiar por permisos
        return redirect('fill_profile/')
    else:
        return render(request, "index.html")

def iniciarSesion(request):
    if request.method == 'GET':
        return render(request, "login.html",{
            "form": UserLoginForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "login.html",{
                "form": UserLoginForm,
                "error": "Usuario o contraseña incorrectos."
            })
        else:
            login(request, user)
            return redirect('index')

def cerrarSesion(request):
    logout(request)
    return redirect('index')

@login_required
def first_login(request):
    if request.user.tipouser == 'T_S':
        if request.method == 'GET':
            return render(request, 'first_login.html', {
                'form': TutoradoFirstLogin()
            })
        else:
            #Guardamos datos en la tabla MyUser
            myuser = MyUser.objects.get(id=request.user.id)
            myuser.nombre = request.POST['nombre']
            myuser.aPaterno = request.POST['aPaterno']
            myuser.aMaterno = request.POST['aMaterno']
            myuser.genero = request.POST['genero']
            myuser.telefono = request.POST['telefono']
            myuser.tipouser = 'T_O'
            myuser.save()
            #Guardamos datos en la tabla Tutorado
            tutorado = Tutorado.objects.get(user_id=request.user.id)
            tutorado.fechaDeNacimiento = request.POST['fechaDeNacimiento']
            tutorado.curp = request.POST['curp']
            tutorado.estadoCivil = request.POST['estadoCivil']
            tutorado.nss = request.POST['nss']
            tutorado.entidadFed = request.POST['entidadFed']
            tutorado.municipio = request.POST['municipio']
            tutorado.domicilio = request.POST['domicilio']
            tutorado.cp = request.POST['cp']
            tutorado.contactConfianza = request.POST['contactConfianza']
            tutorado.estatus = 'ACT'
            tutorado.save()
            return redirect('/')
    else:
        return redirect('/')

@login_required
def perfil(request):
    if request.user.tipouser != 'T_S':
        if request.user.tipouser == 'T_O':
            tutorado = Tutorado.objects.get(user_id=request.user.id)
            return render(request, 'usr_tutorado/perfilTutorado.html', {
                'genero': request.user.get_genero_display(),
                'estadoCivil': tutorado.get_estadoCivil_display(),
                'carrera': Carrera.objects.get(id=tutorado.carrera_id),
                'estatus': tutorado.get_estatus_display(),
                'entidadFed': tutorado.get_entidadFed_display(),
            })
        else:
            return render(request, 'perfil.html', {
                'genero': request.user.get_genero_display(),
                'tipouser': request.user.get_tipouser_display(),
            })
    else:
        return redirect('/')


def changePass(request):
    form = CambiarPassword()
    #Expresion regular para la contraseña
    regex = "(?=.*[A-Z]+)(?=.*[a-z]+)(?=.*[!¡?¿@#$%&/-_.;:]+)(?=.*[0-9]+).{8,}"
    if request.user.tipouser != 'T_S':
        if request.method == 'POST':
            #Agarrar las cosas del form
            actual = request.POST['actual']
            nueva = request.POST['nueva']
            rnueva = request.POST['repetirNueva']
            # print("Actual: "+ str(make_password(actual))+ ". Base"+ str(request.user.password))
            # print(check_password(actual, request.user.password))
            #Checar que la contraseña actual y la que exite en la base de datos sea igual
            if check_password(actual, request.user.password):
                #Checar que el campo actual es diferente al campo de la contraseña nueva
                if actual != nueva:
                    #Checar que las contraseñas nueva y la repeticion sean la misma
                    if nueva == rnueva:
                        #Checar que la contraseña nueva tenga los caracteres necesarios con la expresion regular
                        if re.search(regex, nueva):
                            user = MyUser.objects.get(id=request.user.id)
                            user.password = make_password(nueva)
                            user.save()                            
                        else: 
                            print("incorrecto")
                    else:
                        print("incorrecto desigual")
                else:
                    print("incorrecto igual")
            else:
                print("incorrecto actual")                    
            if form.is_valid():
                return render(request, 'contrasenia.html')
            else:
                return render(request, 'contrasenia.html', {'form':form})
        else:
            return render(request, 'contrasenia.html', {
                'form':form
            })
    else:
        return redirect('/')


@login_required
def changeProfilePic(request):
    if request.user.tipouser != 'T_S':
        if request.method == 'GET':
            form = cambiarFoto()
            return render(request, 'profilePic.html', {
                'form': form
            })
        else:
            form = cambiarFoto(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
            return redirect('/changeProfilePicture/')
    else:
        return redirect('/')

@login_required
def buzon(request):
    if request.user.tipouser != 'T_S':
        if request.method == 'GET':
            return render(request, 'buzon.html', {
                'form': AgregarQuejaSugerencia()
            })
        else:
            QuejaSugerencia.objects.create(texto = request.POST['hint'], estado = 'N', fechaDeCreacion = datetime.now())
            return redirect('/')
    else:
        return redirect('/')

@login_required
def documentacion(request):
    if request.user.tipouser != 'T_S':
        rutaD = os.path.join(settings.MEDIA_ROOT, 'Documentos\\Instituto Tecnológico de Morelia\\')
        os.makedirs(rutaD, exist_ok=True)
        dirPIT = ""
        dirPAT = ""
        dirAP = ""
        if os.path.isfile(rutaD + 'PIT.pdf'):
            dirPIT = "../media/Documentos/Instituto Tecnológico de Morelia/PIT.pdf"
        if os.path.isfile(rutaD + 'PAT.pdf'):
            dirPAT = "../media/Documentos/Instituto Tecnológico de Morelia/PAT.pdf"
        if os.path.isfile(rutaD + 'AP.pdf'):
            dirAP = "../media/Documentos/Instituto Tecnológico de Morelia/AP.pdf"
        return render(request, "documentacion/documentacion.html",{
            "dirPIT":dirPIT,
            "dirPAT":dirPAT,
            "dirAP":dirAP
        })
    else:
        return redirect('/')

#Desarrollado por
def developBy(request):
    return render(request, "developBy.html")

#Pantallas Psicologo
def cita(request):
    if request.user.tipouser == 'PSI':
        form = agendarCitaPsicologo()
        citasNuevas = Citas.objects.filter(fechaDeCita__isnull = True).select_related('personal','tutorado', 'tutorado__user','tutorado__carrera','tutorado__carrera__tecnologico')
        citasAgendadas = Citas.objects.filter(fechaDeCita__isnull = False).select_related('personal','tutorado', 'tutorado__user','tutorado__carrera','tutorado__carrera__tecnologico')    
        if request.method == "POST":
            form = agendarCitaPsicologo(request.POST)
            if form.is_valid():
                idCita = request.POST['idCita']
                citaAgendar = Citas.objects.get(id = idCita)          
                citaAgendar.fechaDeCita = request.POST['fecha']
                citaAgendar.descripcionCita = request.POST['descripcion']
                citaAgendar.save()         

                citasNuevas = Citas.objects.filter(fechaDeCita__isnull = True).select_related('personal','tutorado', 'tutorado__user','tutorado__carrera','tutorado__carrera__tecnologico')
                citasAgendadas = Citas.objects.filter(fechaDeCita__isnull = False).select_related('personal','tutorado', 'tutorado__user','tutorado__carrera','tutorado__carrera__tecnologico')       
                form = agendarCitaPsicologo()
                return render(request, "usr_psicologo/citas.html", {"form":form, 'citasNuevas':citasNuevas, 'citasAgendadas':citasAgendadas})
        # elif request.method == "GET" and 'datosAlumno' in request.GET:
        return render(request, "usr_psicologo/citas.html", {"form":form, 'citasNuevas':citasNuevas, 'citasAgendadas':citasAgendadas})
    else:
        return redirect('/')

#Pantallas Tutor views
@login_required
def grupos(request):
    #valida que el usuario sea de tipo tutor
    if request.user.tipouser == 'T_R':
        #obtengo el id de usuario para consultar 
        grupos = Personal_Carrera.objects.filter(personal_id=request.user.personal.id).select_related('grupo')
        return render(request, 'usr_tutor/grupos.html', {'grupos': grupos})
    else:
        return redirect('/')

@login_required
def verGrupo(request, id):
    #valida que el usuario sea de tipo tutor
    if request.user.tipouser == 'T_R':
        #obtengo el id de grupo para consultar 
        #cuantos alumnos tiene registrados en el grupo
        alumnos = Tutorado.objects.filter(grupo_id=id)
        return render(request, 'usr_tutor/verGrupo.html', {"alumnos":alumnos, "grupo": id})
    else:
        return redirect('/')

@login_required
def perfilTutorado_tutor(request, id):
    if request.user.tipouser == 'T_R':
        #obtiene info del tutorado
        try:
            infoalumno = Tutorado.objects.get(id=id)
        except:
            return redirect('/')
        #formulario
        form = CreateDate(initial={'motive': '13'})
        #cuando se le manda el formulario lleno
        if request.method == "POST":
            motiveList = request.POST.getlist('motive') #Para obtener la lista de motivos
            listMotivos = ''
            contador = 1
            for motivo in motiveList:
                if(motivo == '1'):
                    listMotivos += ', Tristeza profunda o constante'
                elif(motivo == '2'):
                    listMotivos += ', Angustia'
                elif(motivo == '3'):
                    listMotivos += ', Ansiedad'
                elif(motivo == '4'):
                    listMotivos += ', Desesperación constante'
                elif(motivo == '5'):
                    listMotivos += ', Llanto súbito o continuo'
                elif(motivo == '6'):
                    listMotivos += ', Cambios bruscos de conducta'
                elif(motivo == '7'):
                    listMotivos += ', Cambios súbitos de estado de animo'
                elif(motivo == '8'):
                    listMotivos += ', Excitación o alteración psicomotriz'
                elif(motivo == '9'):
                    listMotivos += ', Irritabilidad constante sin motivo aparente'
                elif(motivo == '10'):
                    listMotivos += ', Consumo de drogas'
                elif(motivo == '11'):
                    listMotivos += ', Dificultades severas de aprendizaje'
                elif(motivo == '12'):
                    listMotivos += ', Auto agresiones'
                elif(motivo == '13'):
                    listMotivos += ', Otro'
                if contador == 1:
                    listMotivos = listMotivos[2:]
                    contador = 0
            cita = Citas(motivos=listMotivos, descripcion=request.POST['description'], fechaDeCreacion=datetime.now(), personal_id = request.user.personal.id, tutorado_id=id, 
            tipo='P')
            #se guarda en la base de datos
            cita.save()
            context = {
                "alumno": infoalumno,
                'entidadFed': infoalumno.get_entidadFed_display(),
                "form": form,
                "mensaje": True,
            }
            return render(request, "usr_tutor/perfilTutorado.html", context)
        else:
            context = {
                "alumno": infoalumno,
                'entidadFed': infoalumno.get_entidadFed_display(),
                "form": form,
            }
            return render(request, "usr_tutor/perfilTutorado.html", context)
    else:
        return redirect('/')

@login_required
def actividades(request, id):
    if request.user.tipouser == 'T_R':
        actividades = Actividad.objects.filter(grupo_id=id)    
        
        return render(request, "usr_tutor/actividades.html", {"grupo":id, "actividades":actividades})
    else:
        return redirect('/')

@login_required
def verActividad(request, id, actividad):
    if request.user.tipouser == 'T_R':
        verActividad = Actividad.objects.get(grupo_id=id, id = actividad) 
        ruta = Actividad_Archivo.objects.select_related('archivo').get(actividad_id = actividad)
        return render(request, "usr_tutor/verActividad.html", {
            "grupo":id, 
            "actividad":verActividad,
            "ruta":ruta
            })
    else:
        return render(request, 'accesoDenegado.html')

@login_required
def nuevaActivdad(request, id):
    if request.user.tipouser == 'T_R':
        if request.method == "POST":
            form = CreateActivity(request.POST, request.FILES)
            tecnologico = Tecnologico.objects.get(id = request.user.personal.departamento.tecnologico_id)
            if form.is_valid():
                folder = "Docentes/"+tecnologico.nombre+"/"+str(request.user.idTec)+'/Actividades'
                uploaded_filename = request.FILES['fileLoad'].name

                # save the uploaded file inside that folder.
                full_filename = os.path.join(settings.MEDIA_ROOT, folder, uploaded_filename)
                fout = open(full_filename, 'wb+')

                file_content = ContentFile( request.FILES['fileLoad'].read() )

                # Iterate through the chunks.
                for chunk in file_content.chunks():
                    fout.write(chunk)
                fout.close()

                archivo = "/media/Docentes/"+tecnologico.nombre+"/"+str(request.user.idTec)+'/Actividades/'+str(uploaded_filename)

                # Guardar la ruta del archivo para sacar su id
                arch = Archivo.objects.create(ruta=archivo)
                act = Actividad.objects.create(grupo_id=id, titulo=request.POST['tittle'], descripcion=request.POST['description'], fechaDeAsignacion=datetime.today().strftime('%Y-%m-%d'), fechaDeCierre=request.POST['date'])

                #Asigna la actividad a los alumnos
                # act = Actividad.objects.get(titulo=request.POST['tittle'])
                alumnos = Tutorado.objects.filter(grupo_id=id)
                for alumno in alumnos:
                    # Entregas.objects.create(tutorado_id = Tutorado.objects.get(id = alumno.id).id, actividad_id = Actividad.objects.get(id = act.id).id, estado='P', fechaDeEnvio= '2022-02-11')
                    Entregas.objects.create(tutorado_id = alumno.id, actividad_id = act.id, estado='P')

                #Crea la ruta del archivo de la actividad
                # arch = Archivo.objects.get(ruta=archivo)
                Actividad_Archivo.objects.create(archivo_id=arch.id, actividad_id=act.id)

                return HttpResponseRedirect('/actividades/'+str(id))
        else:
            form = CreateActivity()
        return render(request, "usr_tutor/actividadNueva.html", {"form":form, "grupo": id})
    else:
        return render(request, 'accesoDenegado.html')

@login_required
def verEntrega_tutor(request, id, actividad):
    if request.user.tipouser == 'T_R':

        #entregas = Entregas_Archivo.objects.select_related('archivo','entregas','entregas__tutorado','entregas__tutorado__user').filter(entregas__actividad_id = actividad)
        entregas = Entregas.objects.select_related('tutorado','tutorado__user').filter(actividad_id = actividad)
        entregasArch = Entregas_Archivo.objects.select_related('archivo').filter(entregas__actividad_id = actividad)

        # for al in sAlumnos:
        #     alumnos.append(MyUser.objects.get(id = al.user_id))

        # print(alumnos)
        return render(request, "usr_tutor/verEntregas.html",{
            "grupo":id,
            "entregas":entregas,
            "entregasArch":entregasArch,             
            })
    else:
        return redirect('/')

@login_required
def cargarGrupo_tutor(request, id):
    if request.user.tipouser == 'T_R':
        grupo = Grupo.objects.get(id = id)
        if request.method == "POST":
            #nombre del archivo
            name = request.FILES['lista_alumnos'].name
            file_content = ContentFile( request.FILES['lista_alumnos'].read() )
            #esta es la direccion solo usa media ya que el archivo es temporal
            #se borra al finalizar el proceso
            
            #fichero temporal para archivos auxiliares que se borran
            #tras finalizar el proceso
            temp = os.path.join(settings.MEDIA_ROOT,'temp\\')
            #si no existe la carpeta, la crea
            os.makedirs(temp, exist_ok=True)
            full_name = os.path.join(temp, name)
            fout = open(full_name, 'wb+')
            #le añade todo el contenido del archivo
            for chunk in file_content.chunks():
                fout.write(chunk)
            fout.close()
            #obtiene toda la informacion del excel 
            excel = pd.read_excel(full_name)

            #Funcion para acronimos de carreras
            #no se usa por el momento
            acronimos = []
            carreras = Carrera.objects.all()
            for x in carreras:
                y = str(x).split()
                partes=''
                for i in y:
                    if not (i=='en' or i=='y' or i=='la' or i=='de'):
                        partes += i[0]
                acronimos.append([partes, x.nombre])

            #itera en el excel mientras halla mas filas con informacion
            for a in excel.iterrows():
                ncontrol = str(a[1].loc['Nº de control']) 
                nom_carrera = str(a[1].loc['Carrera'])
                carrera = Carrera.objects.get(nomenclatura=nom_carrera)
                email = ncontrol + '@morelia.tecnm.mx'
                idtec = ncontrol
                #!!!Se ocupa el numero de control con la letra que tenga al inicio!!!
                #if idtec[0].isalpha():
                #    idtec = idtec[1:]
                apaterno = str(a[1].loc['Nombre alumno'].split()[0])
                amaterno = str(a[1].loc['Nombre alumno'].split()[1])
                nombre = str(a[1].loc['Nombre alumno'].split()[2])+' '
                if len(a[1].loc['Nombre alumno'].split()) == 4: 
                    nombre += str(a[1].loc['Nombre alumno'].split()[3])
                exist = MyUser.objects.filter(idTec=idtec)
                #hace una consulta a la base de datos para verificar que no exista el alumno
                if not exist:
                    usuario = MyUser.objects.create(password= make_password('sgt-'+idtec),
                    email=email, is_active=1, is_admin=0,
                    idTec=idtec, date_created=datetime.now(),
                    aMaterno=amaterno, aPaterno=apaterno,nombre=nombre.strip(),
                    fotoDePerfil='default_pic.jpg', tipouser='T_S')
                    alumno = Tutorado.objects.get(user_id = usuario.id)
                    alumno.grupo_id = id
                    alumno.carrera_id = carrera.id
                    alumno.tecDeProcedencia = request.user.personal.departamento.tecnologico.id
                    alumno.save()
                else:
                    alumno = Tutorado.objects.get(user_id = exist[0].id)
                    alumno.grupo_id = id
                    alumno.carrera_id = carrera.id
                    alumno.save()
            #se elimina el archivo
            remove(full_name)
            alumnos = Tutorado.objects.filter(grupo_id=id)
            return render(request, 'usr_tutor/verGrupo.html', {"alumnos":alumnos, "grupo": id, "mensaje":True})
        else:
            return render(request, "usr_tutor/cargarGrupo.html", {"grupo": grupo})
    else:
        return redirect('/')
    

@login_required
def constancia_tutor(request):
    if request.user.tipouser == 'T_R':
        constancias = Personal_Carrera.objects.select_related('grupo', 'grupo__constancia').filter(personal_id = request.user.personal.id) 
        print(constancias.query)
        return render(request, "usr_tutor/constancia.html",{
            'constancias':constancias
        })
    else:
        return redirect('/')

@login_required
#Marca error
def reporteSemestral_tutor(request):
    if request.user.tipouser == 'T_R':
        form = ReporteSemestral()
        grupos = Personal_Carrera.objects.get(personal_id=request.user.personal.id, activo= True)
        alumnos = ''
        if Tutorado.objects.filter(grupo_id=grupos.grupo_id).first() != None:
                alumnos = Tutorado.objects.filter(grupo_id=grupos.grupo_id)
                for a in alumnos:
                    # print("Control. " +str(request.user.id))
                    if(ReporteTutor.objects.filter(noControl= a.user.id).count()==0):
                        ReporteTutor.objects.create(noControl=MyUser.objects.get(id=a.user.id), Tutor=Personal.objects.get(user=request.user.id), grupo= Grupo.objects.get(id=grupos.grupo_id), periodo=None, tutoGrupal=0, tutoIndividual=0, canalizados=0, observaciones=None, asistencia=0)
        # print(ReporteTutor.objects.filter(Tutor=Personal.objects.get(id=grupos.personal_id).user_id, grupo= grupos.grupo_id).query)
        alumnos = ReporteTutor.objects.filter(Tutor=Personal.objects.get(id=grupos.personal_id), grupo= grupos.grupo_id)
        ###print(grupos.id)
        grupo = Grupo.objects.get(id=grupos.grupo_id)
        nombre = str(request.user.nombre) + ' ' + str(request.user.aPaterno) + ' ' + str(request.user.aMaterno)
        info = Personal.objects.filter(user_id=request.user.id).select_related('departamento').first()
        if request.method == 'POST':
            if request.POST['noControl'] != None:
                actualiza = ReporteTutor.objects.get(noControl=MyUser.objects.get(idTec=request.POST['noControl']).id)
                actualiza.tutoGrupal = request.POST['tutoriaGrupal']
                actualiza.tutoIndividual = request.POST['tutoriaIndividual']
                actualiza.canalizados = request.POST['estudiantes']
                actualiza.observaciones = request.POST['observaciones']
                actualiza.asistencia = request.POST['porcentaje']
                actualiza.save()
                alumnos = ReporteTutor.objects.filter(Tutor=Personal.objects.get(id=grupos.personal_id), grupo= grupos.grupo_id)
            else: 
                print('Vacio')
            # if form.is_valid():
            return render(request, 'usr_tutor/reporteSemestral.html', {'alumnos': alumnos, 'grupo': grupo.nombre, 'tutor': nombre, 'departamento': info.departamento.nombre, 'form':form})
        else:
            return render(request, 'usr_tutor/reporteSemestral.html', {
                'form':form,
                'alumnos': alumnos,
                'grupo': grupo.nombre,
                'tutor': nombre,
                'departamento': info.departamento.nombre,
        })
    else:
        return redirect('/')

#Pantallas Jefe de Departamento Academico
@login_required
def docentes(request):
    if request.user.tipouser == 'JDE':
        departamento = Personal.objects.filter(user_id = request.user.id).select_related('departamento')
        tecnologico = ""
        for i in departamento:
            tecnologico = str(i.departamento.tecnologico_id)
        docente = Personal.objects.select_related('departamento','user').filter(departamento__tecnologico_id = tecnologico, departamento_id = request.user.personal.departamento_id)
        return render(request, "usr_jefeDepAcad/docentes.html",{
            'docentes':docente
        })
    else:
        return redirect('/')

@login_required
def verTutor(request, id):
    if request.user.tipouser == 'JDE':
        form = gruposDisponibles(user=request.user)
        if Personal_Carrera.objects.select_related('personal','personal__user').filter(personal_id = id).count()> 0:
            docente = Personal_Carrera.objects.select_related('personal','personal__user').filter(personal_id = id).first()    
        else:
            docente = Personal.objects.select_related('user').get(id = id)            
        grupos = Personal_Carrera.objects.filter(personal_id = id).select_related('personal','grupo','personal__user')
        if request.method == 'POST':
            form = gruposDisponibles(request.POST, user=request.user)
            grupo = Personal_Carrera.objects.select_related('grupo').get(grupo__nombre = request.POST['grupos'])
            grupo.personal_id = id
            grupo.save()    
            form = gruposDisponibles(user=request.user)
            docente = Personal_Carrera.objects.select_related('personal','personal__user').filter(personal_id = id).first()    
            grupos = Personal_Carrera.objects.filter(personal_id = id).select_related('personal','grupo','personal__user')
        return render(request, "usr_jefeDepAcad/verTutor.html",{
            'docente':docente,
            'grupos':grupos,
            'form':form
        })  
    else:
        return redirect('/')

@login_required
def reporte(request):
    return render(request, "usr_jefeDepAcad/reporte.html")

def crear_nuevo_grupo(request):
    if request.user.tipouser == 'CDT':
        form = crearGrupo(user=request.user)
        if request.method == 'POST':
            form = crearGrupo(request.POST, user=request.user)
            now = datetime.now().date()

            periodo = datetime.strptime(request.POST['periodo'], "%Y-%m-%d").date()       
            carrera = Carrera.objects.get(nombre = request.POST['carrera'])

            if(periodo.year == now.year):
                nuevoGrupo = Grupo.objects.create(nombre = request.POST['nombre'], constancia_id = None, reporte = None)
                Personal_Carrera.objects.create(carrera_id = carrera.id, personal_id = None, grupo_id = nuevoGrupo.id, activo = True)
            else:
                nuevoGrupo = Grupo.objects.create(nombre = request.POST['nombre'], constancia_id = None, reporte = None)
                Personal_Carrera.objects.create(carrera_id = carrera.id, personal_id = None, grupo_id = nuevoGrupo.id, activo = False)

            form = crearGrupo(user=request.user)
            return render(request, "usr_jefeDepAcad/crearNuevoGrupo.html",{
                "form":form,
            }) 
        return render(request, "usr_jefeDepAcad/crearNuevoGrupo.html",{
            "form":form,
        })
    else:
        return redirect('/')

def reportes(request):
    if request.user.tipouser == 'CIT':
        #tipo de compresion
        try:
            import zlib
            compression = zipfile.ZIP_DEFLATED
        except:
            compression = zipfile.ZIP_STORED

        #consulta a la base de datos los reportes
        reportes = Reportes.objects.all()
        #ruta de zip, es en la carpeta de archivos temporales
        ruta= os.path.join(settings.MEDIA_ROOT,'temp\\')
        #si no existe la carpeta la crea
        os.makedirs(ruta, exist_ok=True)
        #El nombre del archivo zip
        archivo= os.path.join(ruta, 'Reportes.zip')
        remove(archivo)
        #el archivo zip
        comprimido = zipfile.ZipFile(archivo, mode="w")
        for a in reportes:
            if a.archivo:
                b= os.path.join(settings.MEDIA_ROOT + str(a.archivo.ruta).replace('\\media',''))
                if os.path.exists(b):
                    comprimido.write(b, compress_type=compression)
        comprimido.close()
        return render(request, "usr_coordInstTut/reportes.html", {"reportes":reportes, "zip": archivo})
    else:
        return redirect('/')

def eval_diag(request):
    if request.user.tipouser == 'CIT':
        evaluaciones = Actividad.objects.filter(titulo__contains='Evaluación Diagnostica')
        eval = Actividad_Archivo.objects.filter(actividad_id__in=evaluaciones)
        form = Eval_Diag()
        if request.method == "POST":
            #nombre del archivo
            name = request.FILES['Archivo'].name
            #se obtiene el grupo al que se le asigna
            grupo = Grupo.objects.get(id=request.POST['Grupo'])
            #de aqui se saca el nombre del tecnologico para la ruta
            tec = Personal_Carrera.objects.get(grupo_id=request.POST['Grupo'])
            #se obtiene el contenido del archivo
            file_content = ContentFile( request.FILES['Archivo'].read() )
            #se crea la ruta
            full_name = os.path.join(settings.MEDIA_ROOT + '\\evDiagnostica\\'+str(tec.personal.departamento.tecnologico.nombre))
            os.makedirs(full_name, exist_ok=True)
            full_name += '\\'+name
            #se rellena el archivo con todo el contenido
            fout = open(full_name, 'wb+')
            for chunk in file_content.chunks():
                fout.write(chunk)
            fout.close()
            #la ruta que se guradara el la BDD
            ruta = '\\media\\evDiagnostica\\'+str(tec.personal.departamento.tecnologico.nombre)+'\\'+name
            titulo = 'Evaluación Diagnostica - '
            titulo += str(grupo.nombre)
            archivo = Archivo.objects.create(ruta=ruta)
            actividad = Actividad.objects.create(titulo=titulo,
             descripcion = request.POST['Descripcion'],
             fechaDeAsignacion=datetime.now(),
             fechaDeCierre=request.POST['Fecha_de_cierre'],
             grupo_id=request.POST['Grupo'])
            Actividad_Archivo.objects.create(actividad_id=actividad.id, archivo_id=archivo.id)
            return render(request, "usr_coordInstTut/eval_diag.html", {"eval":eval, 'form':form})
        else:
            return render(request, "usr_coordInstTut/eval_diag.html", {"eval":eval, 'form':form, "mensaje":True})
    else:
        return redirect('/')

def borrar_eval(request, id):
    acti_ar = Actividad_Archivo.objects.get(id=id)
    if(acti_ar.archivo_id):
        archivo = Archivo.objects.get(id=acti_ar.archivo.id)
        ar = os.path.join(settings.MEDIA_ROOT.replace('\\media','')  + str(archivo.ruta))
        #se elimina el archivo
        os.remove(ar)
        archivo.delete()
    if(acti_ar.actividad_id):
        actividad = Actividad.objects.get(id=acti_ar.actividad.id)
        actividad.delete()
    acti_ar.delete()

    evaluaciones = Actividad.objects.filter(titulo__contains='Evaluación Diagnostica')
    eval = Actividad_Archivo.objects.filter(actividad_id__in=evaluaciones)
    return render(request, "usr_coordInstTut/eval_diag.html", {"eval":eval})

def nueva_eval(request):
    if request.user.tipouser == 'CIT':
        return render(request, "usr_coordInstTut/eval_diag_nva.html")
    else:
        return redirect('/')

def const_tutores(request):
    if request.user.tipouser == 'CIT':
        grupos = Personal_Carrera.objects.filter(activo=1)
        if request.method == "POST":
            #se declara la ruta de la plantilla a utilizar
            direc = Environment(loader=FileSystemLoader('sgt/templates/usr_coordInstTut'))
            plantilla = direc.get_template("plantilla_constancia_tutor.html")
            #consultas para rellenar el pdf
            tutor = Personal_Carrera.objects.get(id = request.POST['personal_grupo'])
            #ruta donde se guardaran los creditos
            ruta = os.path.join(settings.MEDIA_ROOT+'\\docentes\\'+tutor.personal.departamento.tecnologico.nombre+'\\'+tutor.personal.user.idTec+'\\documentos')
            #si no existe la carpeta la crea
            os.makedirs(ruta, exist_ok=True)
            info={
                'tec' : tutor.carrera.tecnologico.nombre,
                'ciudad' : tutor.carrera.tecnologico.entidadFed,
                'estado' : tutor.carrera.tecnologico.entidadFed,
                'fecha' : datetime.now(),
                'ap' : tutor.personal.user.aPaterno,
                'am' : tutor.personal.user.aMaterno,
                'nombre' : tutor.personal.user.nombre,
                'rfc' : tutor.personal.user.idTec,
                'curp' : tutor.personal.user.idTec,
                'carrera' : tutor.carrera.nombre,
                'semestre' : 'Agosto - diciembre 2022',
                'mes' : 'diciembre',
                'anio' : 'dos mil veintidos'
            }
            #se crea un objeto con la plantilla
            html = plantilla.render(info)
            #nombre del pdf
            pdf = os.path.join(ruta+'\\Constancia-'+str(tutor.grupo.nombre)+'.pdf')
            #crea el pdf
            HTML(string=html, base_url= request.build_absolute_uri()).write_pdf(target=pdf)
            #se crea el archivo y registros en la BD
            archivo = os.path.join('\\media\\docentes\\'+tutor.personal.departamento.tecnologico.nombre+'\\'+tutor.personal.user.idTec+'\\documentos\\''Constancia-'+str(tutor.grupo.nombre)+'.pdf')
            a = Archivo.objects.create(ruta = archivo)
            grupo = Grupo.objects.get(id = tutor.grupo_id)
            grupo.constancia_id = a.id
            grupo.save()
            return render(request, "usr_coordInstTut/const_tutores.html",{'grupos':grupos, 'mensaje':True})
        else:
            return render(request, "usr_coordInstTut/const_tutores.html",{'grupos':grupos})
    else:
        return redirect('/')

def creditos(request):
    if request.user.tipouser == 'CIT':
        grupos = Personal_Carrera.objects.filter(activo=1)
        if request.method == "POST":
            #se declara la ruta de la plantilla a utilizar
            direc = Environment(loader=FileSystemLoader('sgt/templates/usr_coordInstTut'))
            plantilla = direc.get_template("plantilla_creditos.html")
            #consultas para rellenar el pdf
            tutorados = Tutorado.objects.filter(grupo_id=request.POST['grupo'])
            profesor = Personal_Carrera.objects.get(grupo_id = request.POST['grupo'])
            for a in tutorados:
                info={
                    'tec' : profesor.carrera.tecnologico.nombre,
                    'ciudad' : profesor.carrera.tecnologico.entidadFed,
                    'fecha' : datetime.now(),
                    'ap' : a.user.aPaterno,
                    'am' : a.user.aMaterno,
                    'nombre' : a.user.nombre,
                    'nc' : a.user.idTec,
                    'carrera' : a.carrera.nombre,
                    'tutorap' : profesor.personal.user.aPaterno,
                    'tutoram' : profesor.personal.user.aMaterno,
                    'tutorn' : profesor.personal.user.nombre,
                }
                #ruta donde se guardaran los creditos
                ruta = os.path.join(settings.MEDIA_ROOT+'\\tutorados\\'+profesor.personal.departamento.tecnologico.nombre+'\\'+a.user.idTec+'\\creditos')
                #si no existe la carpeta la crea
                os.makedirs(ruta, exist_ok=True)
                #se crea un objeto con la plantilla
                html = plantilla.render(info)
                #nombre del pdf
                pdf = os.path.join(ruta+'\\Credito tutorias - '+str(a.user.idTec)+'.pdf')
                #crea el pdf
                HTML(string=html, base_url= request.build_absolute_uri()).write_pdf(target=pdf)
                #ruta del archivo
                archivo = os.path.join('\\media\\tutorados\\'+profesor.personal.departamento.tecnologico.nombre+'\\'+a.user.idTec+'\\creditos'+'\\Credito tutorias - '+str(a.user.idTec)+'.pdf')
                ar = Archivo.objects.create(ruta = archivo)
                p = Personal.objects.get(user_id = request.user.id)
                ct = CreditosTutorado.objects.create(tutorado = a, curso = None, ruta = ar ,estado = '2', fechaDeEnvio = datetime.now())
                Creditos.objects.create(fechaDeValidacion=datetime.now(),creditostutorado=ct, personal_id=p.id)
            return render(request, "usr_coordInstTut/creditos.html",{'grupos':grupos, 'mensaje':True})
        else:
            return render(request, "usr_coordInstTut/creditos.html",{'grupos':grupos})
    else:
        return redirect('/')

@login_required
def crear_periodo(request):
    if request.user.tipouser == 'CIT':
        if request.method == 'GET':
            context = {
                'form': crearPeriodo(),
            }
            return render(request, "usr_coordInstTut/crearPeriodo.html", context)
        else:
            Periodo.objects.create(fechaInicio = request.POST['fechaInicio'], fechaTermina = request.POST['fechaFin'], tipoPeriodo = request.POST['tipo'])
            return redirect('/ver_periodos')
    else:
        return redirect('/')

@login_required
def ver_periodos(request):
    if request.user.tipouser == 'CIT':
        context = {
            'periodos': Periodo.objects.all().order_by('id').reverse(),
        }
        return render(request, "usr_coordInstTut/listPeriodos.html", context)
    else:
        return redirect('/')

@login_required
def agregar_carrera(request):
    if request.user.tipouser == 'CIT':
        if request.method == 'GET':
            context = {
                'form': crearCarrera
            }
            return render(request, "usr_coordInstTut/agregarCarrera.html", context)
        else:
            departamento = Departamento.objects.get(nombre=request.POST['departamento'])
            tecnologico = Tecnologico.objects.get(id=1)
            Carrera.objects.create(nombre = request.POST['nombre'], departamento = departamento, tecnologico = tecnologico, nomenclatura = request.POST['nomenclatura'])
            context = {
                'form': crearCarrera
            }
            return render(request, "usr_coordInstTut/agregarCarrera.html", context)
    else:
        return redirect('/')

@login_required
def agregar_departamento(request):
    if request.user.tipouser == 'CIT':
        if request.method == 'GET':
            context = {
                'form': crearDepartamento()
            }
            return render(request, "usr_coordInstTut/agregarDepartamento.html", context)
        else:
            tecnologico = Tecnologico.objects.get(id=1)
            Departamento.objects.create(nombre = request.POST['nombre'], tecnologico = tecnologico)
            context = {
                'form': crearDepartamento()
            }
            return render(request, "usr_coordInstTut/agregarDepartamento.html", context)
    else:
        return redirect('/')

#Pantallas Cordinador de Tutoria del Dpto. Academico
def reportes_docentes(request):
    # Buscar carreras del tecnologico del docente
    departamento = Personal.objects.filter(user_id = request.user.id, departamento_id = request.user.personal.departamento_id).select_related('departamento')
    tecnologico = ""
    for i in departamento:
        tecnologico = str(i.departamento.tecnologico_id)
    carreras = Carrera.objects.filter(tecnologico_id = tecnologico, departamento_id = request.user.personal.departamento_id)

    # Buscar docentes de las carreras del tecnologico seleccionado
    # docentes = Personal.objects.select_related('departamento', 'user', 'departamento__tecnologico', 'personal')
    
    # temp = []  
    
    docentes = Personal_Carrera.objects.select_related('personal', 'carrera','grupo', 'carrera__tecnologico', 'personal__departamento', 'personal__user').filter(personal__departamento__tecnologico_id = tecnologico, activo = True)
    # grupo =  Grupo.objects.select_related('personal', 'constancia')
    # for docente in docentes:
    #     temp.append(grupo.filter(personal_id = docente.id))
    # docentes = docentes.departamento.select_related('personal_carrera')
    print(docentes.query)
    return render(request, "usr_cord_tut_dpto_acad/reportes_docentes.html",{
        'carreras':carreras,
        'docentes':docentes
    })

def ctda_info_docente(request, id):
    docente = Personal_Carrera.objects.select_related('personal','personal__user').get(personal_id = id, activo = True)
    reportes = Personal_Carrera.objects.select_related('grupo','grupo__reporte__archivo').filter(personal_id = id, activo = True)
    return render(request, "usr_cord_tut_dpto_acad/info_docente.html",{
        'docente':docente,
        'reportes':reportes
    })

def ctda_reportes_generar(request):
    return render(request, "usr_cord_tut_dpto_acad/reportes_generar.html")

#Pantallas Tutorado
#Unicamente los tutorados pueden acceder
@login_required
def tutorado_actividades(request):
    # alumno = Tutorado.objects.get(user_id=request.user.id)
    actividades = Actividad.objects.filter(grupo_id = request.user.tutorado.grupo_id)
    entregas = Entregas.objects.filter(tutorado_id = request.user.tutorado.id)
    # print(entregas.query)
    if(actividades.__len__()>0):
        return render(request, "usr_tutorado/actividades.html",{
        "actividades":actividades,
        "entregas":entregas
    })
    else:
        return render(request, "usr_tutorado/actividades.html")

def tutorado_ver_actividad(request, actividad):
    alumno = Tutorado.objects.get(user_id=request.user.id)
    act = Actividad_Archivo.objects.select_related('actividad','archivo').get(actividad_id=actividad)
    stat = Entregas.objects.get(actividad_id = actividad, tutorado_id = alumno.id)
    if request.method == "POST":
            form = enviarTarea(request.POST, request.FILES)
            if form.is_valid():
                tecnologico = Tecnologico.objects.get(id = request.user.tutorado.tecDeProcedencia)
                folder = "Tutorados/"+tecnologico.nombre+"/"+str(request.user.idTec)+"/Actividades"
                uploaded_filename = request.FILES['fileLoad'].name

                # save the uploaded file inside that folder.
                full_filename = os.path.join(settings.MEDIA_ROOT, folder, uploaded_filename)
                fout = open(full_filename, 'wb+')

                file_content = ContentFile( request.FILES['fileLoad'].read() )

                # Iterate through the chunks.
                for chunk in file_content.chunks():
                    fout.write(chunk)
                fout.close()

                archivo = "/media/Tutorados/"+tecnologico.nombre+"/"+str(request.user.idTec)+"/Actividades/"+str(uploaded_filename)
                ultimoArchivo = Archivo.objects.create(ruta = archivo)
                subir = Entregas.objects.get(actividad_id = actividad, tutorado_id = alumno.id)
                subir.estado='E'
                subir.fechaDeEnvio = datetime.today().strftime('%Y-%m-%d')
                subir.save()

                Entregas_Archivo.objects.create(entregas_id = subir.id, archivo_id=ultimoArchivo.id)

                return redirect("/verActividades/")
    else:
        if stat.fechaDeEnvio != None:
            entrega = Entregas_Archivo.objects.select_related('archivo','entregas').get(entregas_id=stat.id)
            return render(request, "usr_tutorado/ver_actividad.html",{
            "actividad":act,
            "estatus":stat,
            'entrega':entrega
            })
        else:
            form = enviarTarea()
            return render(request, "usr_tutorado/ver_actividad.html",{
            "form":form,
            "actividad":act,
            "estatus":stat
            })

def tutorado_carta_liberacion(request):
    credito = CreditosTutorado.objects.select_related('ruta').get(tutorado_id = request.user.tutorado.id, estado = 2, curso_id = None, cursoPendiente_id = None)
    return render(request, "usr_tutorado/carta_liberacion.html",{
        'credito':credito
    })

@login_required
def tutorado_subir_creditos(request):
    
    # creditos = CreditosTutorado.objects.filter(tutorado_id=request.user.tutorado.id).select_related('curso', 'ruta')
    creditos = CreditosTutorado.objects.select_related('curso','ruta').filter(tutorado_id = request.user.tutorado.id)
    form = CreditosComplementarios_tutorado()
    #en caso de que no tenga los 5
    direc = Environment(loader=FileSystemLoader('sgt/templates/usr_tutorado'))
    plantilla = direc.get_template("plantilla_creditos_completos.html")
    #consultas para rellenar el pdf
    tutorado = Tutorado.objects.get(id=request.user.tutorado.id)
    
    info={
        'tec' : tutorado.carrera.tecnologico.nombre,
        'ap' : tutorado.user.aPaterno,
        'am' : tutorado.user.aMaterno,
        'nombre' : tutorado.user.nombre,
        'nc' : tutorado.user.idTec,
        'carrera' : tutorado.carrera.nombre,
    }
    #ruta donde se guardaran los creditos
    ruta = os.path.join(settings.MEDIA_ROOT+'\\tutorados\\'+tutorado.carrera.tecnologico.nombre+'\\'+tutorado.user.idTec+'\\creditos')
    #si no existe la carpeta la crea
    os.makedirs(ruta, exist_ok=True)
    #se crea un objeto con la plantilla
    html = plantilla.render(info)
    #nombre del pdf
    pdf = os.path.join(ruta+'\\Constancia Actividades Complementarias - '+str(tutorado.user.idTec)+'.pdf')
    #crea el pdf
    HTML(string=html, base_url= request.build_absolute_uri()).write_pdf(target=pdf)
    #ruta del archivo
    archivo = os.path.join('\\media\\tutorados\\'+tutorado.carrera.tecnologico.nombre+'\\'+tutorado.user.idTec+'\\creditos\\Constancia Actividades Complementarias - '+str(tutorado.user.idTec)+'.pdf')

    if request.method == "POST":
        # Saber que submit se esta subiendo
        if 'fieldCredito' in request.POST:             
            # Eliminar el objeto     
            CreditosTutorado.objects.filter(id = request.POST['fieldCredito']).delete()
        elif 'fieldCreditoEliminar' in request.POST:
            CreditosTutorado.objects.filter(id = request.POST['fieldCreditoEliminar']).delete() 
        else:
            # Cambiar el form para recibir el archivo
            tecnologico = Tecnologico.objects.get(id = request.user.tutorado.tecDeProcedencia)
            form = CreditosComplementarios_tutorado(request.POST, request.FILES)
            if form.is_valid():
                folder = "Tutorados/"+tecnologico.nombre+"/"+str(request.user.idTec)+"/Creditos"
                uploaded_filename = request.FILES['fileLoad'].name

                # save the uploaded file inside that folder.
                full_filename = os.path.join(settings.MEDIA_ROOT, folder, uploaded_filename)
                fout = open(full_filename, 'wb+')

                file_content = ContentFile( request.FILES['fileLoad'].read() )

                # Iterate through the chunks.
                for chunk in file_content.chunks():
                    fout.write(chunk)
                fout.close()

                
                archivo = "/media/Tutorados/"+tecnologico.nombre+"/"+str(request.user.idTec)+"/Creditos/"+str(uploaded_filename)

                # Guardar la ruta del archivo para sacar su id
                ultimoArchivo = Archivo.objects.create(ruta = archivo)
                tutorado = Tutorado.objects.get(user_id = request.user.id)
                try:
                    folioCurso = Curso.objects.get(folio = request.POST['folio'])             
                except:   
                    folioCursoPendiente = CursoPendiente.objects.create(folio = request.POST['folio'])
                    CreditosTutorado.objects.create(tutorado = tutorado , curso = None, ruta = ultimoArchivo ,estado = '1', fechaDeEnvio = datetime.now(), cursoPendiente = folioCursoPendiente)           
                else:
                    CreditosTutorado.objects.create(tutorado = tutorado , curso = folioCurso, ruta = ultimoArchivo ,estado = '1', fechaDeEnvio = datetime.now(), cursoPendiente = None)             

                # archivoRuta = Archivo.objects.get(id = ultimoArchivo.id, ruta = archivo)
        return render(request, "usr_tutorado/subir_creditos.html", {
            "creditos":creditos,
            "form":form,
            "archivo":archivo,
        })  
    else:
        # for credito in creditos:
        #     print(credito.ruta.ruta)
        return render(request, "usr_tutorado/subir_creditos.html", {
            "creditos":creditos,
            "form":form,
            "archivo":archivo,
        })

#Pantallas administrador
def administrador_inicio(request):
    directorio = MyUser.objects.select_related().all()
    return render(request, "usr_administrador/inicio.html",{
        'directorio':directorio,
    })

def administrador_buzon(request):
    buzon = QuejaSugerencia.objects.filter(estado = 'N')
    if request.method == "POST":
        bz = QuejaSugerencia.objects.get(id = request.POST['id'])
        bz.estado = 'L'
        bz.save()
        return render(request, "usr_administrador/buzon.html",{
        "buzon":buzon
        })
    return render(request, "usr_administrador/buzon.html",{
        "buzon":buzon
    })
    
@login_required
def administrador_docente(request, id):
    doc = MyUser.objects.select_related('personal').filter(id = id).first()
    form = editTutor(instance = doc)
    if request.method == "POST":
        user = MyUser.objects.get(id = id)
        user.nombre = request.POST['Nombre']
        user.aPaterno = request.POST['AP']
        user.aMaterno = request.POST['AM']
        user.telefono = request.POST['Telefono']
        user.idTec = request.POST['RFC']
        if request.POST['Contrasenia'] != "":
            user.password = make_password(request.POST['Contrasenia'])
        user.email = request.POST['Correo']
        user.save()
        personal = Personal.objects.get(user_id=id)
        personal.localizacion = request.POST['Cubiculo']
        personal.departamento = Departamento.objects.get(id=request.POST['Departamento'])
        personal.save()
        
        #return HttpResponseRedirect('/admin_docente/'+str(id))
        return render(request, "usr_administrador/verDocente.html",{
        "form":editTutor(instance = MyUser.objects.select_related('personal').filter(id = id).first()),
        "docente": doc,
        "mensaje": True
        })
    else:
        return render(request, "usr_administrador/verDocente.html",{
        "form":form,
        "docente": doc
        })
    
def administrador_tutorado(request, id):
    tut = Tutorado.objects.select_related('user','carrera','grupo').filter(user_id = id).first()
    form = editTutorado(instance = tut)
    if request.method == "POST":
        alumno = Tutorado.objects.select_related('user','carrera','grupo').filter(user_id = id).first()
        alumno.user.nombre= request.POST['Nombre']
        alumno.user.aPaterno= request.POST['AP']
        alumno.user.aMaterno= request.POST['AM']
        alumno.user.email= request.POST['Correo']
        alumno.user.telefono= request.POST['Telefono']
        alumno.user.idTec= request.POST['NoControl']
        alumno.user.genero= request.POST['genero']
        if request.POST['Contrasenia'] != "":
            alumno.user.password= make_password(request.POST['Contrasenia'])
        alumno.curp = request.POST['Curp']
        alumno.nss = request.POST['NumeroSS']
        alumno.municipio = request.POST['Municipio']
        alumno.domicilio = request.POST['Domicilio']
        alumno.cp = request.POST['CP']
        alumno.contactConfianza = request.POST['CC']
        alumno.semestre = request.POST['Semestre']
        alumno.entidadFed = request.POST['entidadFed']
        alumno.estadoCivil = request.POST['estadoCivil']
        alumno.carrera = Carrera.objects.get(id=request.POST['carrera'])
        alumno.estatus = request.POST['estatus']
        alumno.save()
        return render(request, "usr_administrador/verTutorado.html",{
        "form":editTutorado(instance = Tutorado.objects.select_related('user','carrera','grupo').filter(user_id = id).first()),
        "tutorado": tut,
        "mensaje": 'Modificado correctamente'
        })
    else:
        return render(request, "usr_administrador/verTutorado.html",{
        "form":form,
        "tutorado": tut,
        })

@login_required
@transaction.atomic
def administrador_agregarDocente(request):
    form = AddDocente()
    if request.method == "POST":
        try:
            #Guardamos datos en la tabla MyUser
            id = MyUser.objects.create(
            password=make_password(request.POST['Contrasenia']), 
            email=request.POST['Correo'], 
            is_active=1, 
            is_admin=0,
            idTec=request.POST['RFC'], 
            date_created=datetime.now(),
            aMaterno=request.POST['AM'], 
            aPaterno=request.POST['AP'],
            nombre=request.POST['Nombre'].strip(),
            fotoDePerfil='default_pic.jpg', 
            tipouser=request.POST['Tipo'],
            genero = request.POST['Genero'],
            telefono = request.POST['Telefono'])        
        #Guardamos datos en la tabla Personal
            personal = Personal.objects.get(user_id = id.id)
            personal.campus = 'Campus 1'
            personal.localizacion = request.POST['Cubiculo']
            personal.departamento = Departamento.objects.get(id=request.POST['Dp'])

            #crea la carpeta para el personal
            rutaD = os.path.join(settings.MEDIA_ROOT, 'Docentes\\Instituto Tecnológico de Morelia\\'+ id.idTec +'\\Documentos\\')
            rutaA = os.path.join(settings.MEDIA_ROOT, 'Docentes\\Instituto Tecnológico de Morelia\\'+ id.idTec +'\\Actividades\\')
            rutaR = os.path.join(settings.MEDIA_ROOT, 'Docentes\\Instituto Tecnológico de Morelia\\'+ id.idTec +'\\Reportes\\')
            #si no existe la carpeta la crea
            os.makedirs(rutaD, exist_ok=True)
            os.makedirs(rutaA, exist_ok=True)
            os.makedirs(rutaR, exist_ok=True)
            
            form = AddDocente()
            return render(request, "usr_administrador/agregarDocente.html",{
            "form": form,
            "id_err":'0',
            "Mensaje": True
            })
        except Exception as e:
            print(e)
            return render(request, "usr_administrador/agregarDocente.html",{
            "form": form,
            "id_err":'1',
            "Mensaje": True
            })
    return render(request, "usr_administrador/agregarDocente.html",{
        "form": form,
    })

@login_required
@transaction.atomic
def administrador_agregarTutorado(request):
    form = AddAl()
    if request.method == 'POST':
        try:
            usuario = MyUser.objects.create(
            password= make_password('sgt-'+request.POST['NoControl']),
            email=request.POST['NoControl']+'@morelia.tecnm.mx', 
            is_active=1, 
            is_admin=0,
            date_created=datetime.now(),
            fotoDePerfil='default_pic.jpg', 
            tipouser='T_S',
            idTec=request.POST['NoControl']
            )
            alumno = Tutorado.objects.get(user_id = usuario.id)
            alumno.grupo_id = request.POST['Grupo']
            alumno.tecDeProcedencia = Tecnologico.objects.get(id=1).id
            alumno.save()

            rutaC = os.path.join(settings.MEDIA_ROOT, 'Tutorados\\Instituto Tecnológico de Morelia\\'+ usuario.idTec +'\\Creditos\\')
            rutaA = os.path.join(settings.MEDIA_ROOT, 'Tutorados\\Instituto Tecnológico de Morelia\\'+ usuario.idTec +'\\Actividades\\')

            os.makedirs(rutaC, exist_ok=True)
            os.makedirs(rutaA, exist_ok=True)

            form = AddAl()
            return render(request, "usr_administrador/agregarTutorado.html",{
                "form":form,
                "id_err":'0',
                "Mensaje": True,
                "Credenciales": usuario
            })
        except Exception as e:
            print(e)
            return render(request, "usr_administrador/agregarTutorado.html",{
                "form":form,
                "id_err":'1',
                "Mensaje": True
            })
    else:
        return render(request, "usr_administrador/agregarTutorado.html",{
            "form":form
        })

def administrador_cargarDocumentos(request):
    form = cargarArchivo()

    rutaD = os.path.join(settings.MEDIA_ROOT, 'Documentos\\Instituto Tecnológico de Morelia\\')
    os.makedirs(rutaD, exist_ok=True)

    dirPIT = ""
    dirPAT = ""
    dirAP = ""

    if os.path.isfile(rutaD + 'PIT.pdf'):
        dirPIT = "../media/Documentos/Instituto Tecnológico de Morelia/PIT.pdf"
    if os.path.isfile(rutaD + 'PAT.pdf'):
        dirPAT = "../media/Documentos/Instituto Tecnológico de Morelia/PAT.pdf"
    if os.path.isfile(rutaD + 'AP.pdf'):
        dirAP = "../media/Documentos/Instituto Tecnológico de Morelia/AP.pdf"

    return render(request, "usr_administrador/cargarDocumentos.html",{
        "form":form,
        "dirPIT":dirPIT,
        "dirPAT":dirPAT,
        "dirAP":dirAP,
    })

def admin_eliminarDocumento(request, codigo):
    try:
        dir = os.path.join(settings.MEDIA_ROOT, 'Documentos\\Instituto Tecnológico de Morelia\\')
        if codigo == '1':
            dir += 'PAT.pdf'
        elif codigo == '2':
            dir += 'PIT.pdf'
        elif codigo == '3':
            dir += 'AP.pdf'
        os.remove(dir)
    except Exception as e:
        print(e)
    return redirect('/admin_cargarDocumentos/')

def admin_addDocumento(request, codigo):
    try:
        if codigo == '1':
            uploaded_filename = 'PAT.pdf'
        elif codigo == '2':
            uploaded_filename = 'PIT.pdf' 
        elif codigo == '3':
            uploaded_filename = 'AP.pdf' 

        dir = os.path.join(settings.MEDIA_ROOT, 'Documentos\\Instituto Tecnológico de Morelia\\')
        # save the uploaded file inside that folder.
        full_filename = os.path.join(settings.MEDIA_ROOT, dir, uploaded_filename)
        fout = open(full_filename, 'wb+')
        file_content = ContentFile( request.FILES['fileLoad'].read() )
        # Iterate through the chunks.
        for chunk in file_content.chunks():
            fout.write(chunk)
        fout.close()

    except Exception as e:
        print(e)
    return redirect('/admin_cargarDocumentos/')

# Pantallas Subdirector

def gestionar_Cursos(request):
    cursosAprobados = Curso.objects.select_related('encargado','encargado__user').all()    
    cursosPendientes = CursoPendiente.objects.all()
    creditosTutorado = CreditosTutorado.objects.select_related('curso','ruta','tutorado','tutorado__user').filter(estado = 1, cursoPendiente = None).order_by('fechaDeEnvio')
    formCursoRechazar = RechazarCursoPendiente()
    formCrearCurso = AgregarNuevoCurso()

    if request.method == 'POST':
        #Creditos con folio no registrado
        if 'fieldCursoEliminar' in request.POST:       
            creditos = CreditosTutorado.objects.filter(cursoPendiente = request.POST['fieldCursoEliminar'])
            for credito in creditos:
                credito.estado = 3
                credito.cursoPendiente = None
                credito.save()
            CursoPendiente.objects.get(id = request.POST['fieldCursoEliminar']).delete()
        #Aprobar credito tutorado
        elif 'fieldCreditoAprobar' in request.POST:            
            credito = CreditosTutorado.objects.get(id = request.POST['fieldCreditoAprobar'])
            credito.estado = 2
            credito.save()
        #Rechazar credito tutorado
        elif 'fieldCreditoRechazar' in request.POST:
            credito = CreditosTutorado.objects.get(id = request.POST['fieldCreditoRechazar'])
            credito.estado = 3
            credito.save()            
        #Crear nuevo curso
        elif 'cantTutorados' in request.POST:
            nombre = request.POST['nombre']
            folio = request.POST['folio']
            cantTutorados = request.POST['cantTutorados']
            valor = request.POST['valor']
            encargado = Personal.objects.select_related('user').get(user__idTec = request.POST['encargadoNombre'])

            cursoNuevo = Curso.objects.create(nombre = nombre, folio = folio, cantTutorados = cantTutorados, fecha = datetime.now(), valor = valor, encargado = encargado)

            if CreditosTutorado.objects.select_related('cursoPendiente').filter(cursoPendiente__folio = folio).count() > 0:
                creditosPendientes = CreditosTutorado.objects.select_related('cursoPendiente').filter(cursoPendiente__folio = folio)
                for creditoPendiente in creditosPendientes:
                    creditoPendiente.curso = cursoNuevo
                    creditoPendiente.cursoPendiente = None
                    creditoPendiente.save()
                CursoPendiente.objects.get(folio = folio).delete()

        cursosAprobados = Curso.objects.select_related('encargado','encargado__user').all()    
        cursosPendientes = CursoPendiente.objects.all()
        creditosTutorado = CreditosTutorado.objects.select_related('curso','ruta','tutorado','tutorado__user').filter(estado = 1, cursoPendiente = None).order_by('fechaDeEnvio')
        formCursoRechazar = RechazarCursoPendiente()
        formCrearCurso = AgregarNuevoCurso()
        return render(request, "usr_subdirector/gestionarCursos.html",{
            'cursosAprobados':cursosAprobados,
            'cursosPendientes':cursosPendientes,
            'formCursoRechazar':formCursoRechazar,
            'formCrearCurso':formCrearCurso,
            'creditosTutorado':creditosTutorado,
            
        })
    return render(request, "usr_subdirector/gestionarCursos.html",{
        'cursosAprobados':cursosAprobados,
        'cursosPendientes':cursosPendientes,
        'formCursoRechazar':formCursoRechazar,
        'formCrearCurso':formCrearCurso,
        'creditosTutorado':creditosTutorado,
        
    })
