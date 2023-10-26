from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Principal
    path('', views.index, name="index"),
    path('fill_profile/', views.first_login, name='fill_profile'),
    path('perfil/', views.perfil, name="perfil"),

    # Autenticacion
    path('login/', views.iniciarSesion, name='login'),
    path('logout/', views.cerrarSesion, name='logout'),
    path('changePassword/', views.changePass, name='changePass'),
    path('changeProfilePicture/', views.changeProfilePic, name='changeProfilePic'),

    # Psicologo
    path('psi_citas/', views.cita, name="psi_citas"),

    # Subdirector
    path('gestionarCursos/', views.gestionar_Cursos, name="gestionarCursos"),

    # Navbar
    path('buzon/',views.buzon, name="buzon"),
    path('documentacion/',views.documentacion, name="documentacion"),

    # Creditos
    path('developBy/',views.developBy, name="developBy"),

    # Tutor urls
    path('grupos/', views.grupos,name="grupos"),
    path('verGrupo/<int:id>/', views.verGrupo, name="verGrupo"),
    path('perfilTutorado_tutor/<int:id>/', views.perfilTutorado_tutor, name="perfilTutorado_tutor"),
    path('actividades/<int:id>/', views.actividades, name="actividades"),
    path('verActividad/<int:id>/<int:actividad>/', views.verActividad, name="verActividad"),
    path('actividadNueva/<int:id>/', views.nuevaActivdad, name="actividadNueva"),
    path('verEntrega_tutor/<int:id>/<int:actividad>/', views.verEntrega_tutor, name="verEntrega_tutor"),
    path('cargarGrupo_tutor/<int:id>/', views.cargarGrupo_tutor, name="cargarGrupo_tutor"),
    path('constancia_tutor/', views.constancia_tutor, name="constancia_tutor"),
    path('semestral_tutor/', views.reporteSemestral_tutor, name="semestral_tutor"),

    #Jefe de Departamento Academico
    path('docentes/', views.docentes, name="docentes"),
    path('verTutor/<int:id>/', views.verTutor, name="verTutor"),
    path('reporte/', views.reporte, name="reporte"),
    path('crearNuevoGrupo/', views.crear_nuevo_grupo, name="crearNuevoGrupo"),

    # Coordinador institucional de tutorias
    path('reportes/', views.reportes, name='reportes'),
    path('eval_diag/', views.eval_diag, name='eval_diag'),
    path('nueva_eval/', views.nueva_eval, name='nueva_eval'),
    path('borrar_eval/<int:id>/', views.borrar_eval, name='borrar_eval'),
    path('const_tutores/', views.const_tutores, name='const_tutores'),
    path('creditos/', views.creditos, name='creditos'),
    path('crear_periodo/', views.crear_periodo, name='crear_periodo'),
    path('ver_periodos/', views.ver_periodos, name='ver_periodos'),
    path('agregar_carrera/', views.agregar_carrera, name='agregar_carrera'),
    path('agregar_departamento/', views.agregar_departamento, name='agregar_departamento'),

    #Cordinador de Tutoria del Dpto. Academico
    path('reportesDocentes/', views.reportes_docentes, name='reportesDocentes'),
    path('ctda_info_docente/<int:id>/', views.ctda_info_docente, name='ctda_info_docente'),

    #Tutorado
    path('verActividades/', views.tutorado_actividades, name='verActividades'),
    path('actividad/<int:actividad>/', views.tutorado_ver_actividad, name='actividad'),
    path('tutorado_carta_liberacion/', views.tutorado_carta_liberacion, name='tutorado_carta_liberacion'),
    path('tutorado_subir_creditos/', views.tutorado_subir_creditos, name='tutorado_subir_creditos'),

    #Administrador
    path('admin_inicio/', views.administrador_inicio, name='admin_inicio'),
    path('admin_buzon/', views.administrador_buzon, name='admin_buzon'),
    path('admin_docente/<int:id>/', views.administrador_docente, name='admin_docente'),
    path('admin_tutorado/<int:id>/', views.administrador_tutorado, name='admin_tutorado'),
    path('admin_agregarDocente/', views.administrador_agregarDocente, name='admin_agregarDocente'),
    path('admin_agregarTutorado/', views.administrador_agregarTutorado, name='admin_agregarTutorado'),
    path('admin_cargarDocumentos/', views.administrador_cargarDocumentos, name='admin_cargarDocumentos'),
    path('admin_eliminarDocumento/<codigo>', views.admin_eliminarDocumento, name='admin_eliminarDocumento'),
    path('admin_addDocumento/<codigo>', views.admin_addDocumento, name='admin_addDocumento')
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)