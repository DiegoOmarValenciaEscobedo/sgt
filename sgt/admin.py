from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from datetime import datetime

from sgt.models import Actividad, Actividad_Archivo, Archivo, Carrera, Citas, Creditos, CreditosTutorado, Curso, Departamento, Entregas, Entregas_Archivo, Grupo, MyUser, Personal, QuejaSugerencia, Reportes, Tecnologico, Tutorado


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'idTec',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.date_created = datetime.now()
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'idTec', 'is_active', 'is_admin')

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'idTec', 'is_admin', 'tipouser',)
    list_filter = ('is_admin', 'tipouser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('idTec', 'nombre', 'aPaterno', 'aMaterno', 'telefono', 'fotoDePerfil', 'genero', 'tipouser')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'idTec', 'tipouser','password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class PersonalChangeForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ('campus', 'localizacion', 'departamento')

class PersonalAdmin(admin.ModelAdmin):
    form = PersonalChangeForm

    list_display = ('nombre_completo', 'user', 'departamento',)
    list_filter = ('departamento',)

    def nombre_completo(self, obj):
        myuser = MyUser.objects.get(id = obj.user_id)
        if myuser.nombre:
            return myuser.aPaterno + " " + myuser.aMaterno + " " + myuser.nombre
        else:
            return myuser.email

class TutoradoChangeForm(forms.ModelForm):
    class Meta:
        model = Tutorado
        fields = ('fechaDeNacimiento', 'curp', 'estadoCivil', 'nss', 'observaciones', 'carrera', 'semestre', 'estatus', 'entidadFed', 'municipio', 'domicilio', 'cp')

class TutoradoAdmin(admin.ModelAdmin):
    form = TutoradoChangeForm

    list_display = ('tec_id', 'user', 'carrera_id', 'semestre',)
    

    def tec_id(self, obj):
        myuser = MyUser.objects.get(id = obj.user_id)
        return myuser.idTec

class TecnologicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'entidadFed',)
    list_filter = ('entidadFed',)

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tecnologico',)
    list_filter = ('tecnologico',)

class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'tecnologico',)
    list_filter = ('tecnologico', 'departamento',)

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre', ),
        }),
    )

admin.site.register(MyUser, UserAdmin)
admin.site.register(Tecnologico, TecnologicoAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Carrera, CarreraAdmin)
admin.site.register(Personal, PersonalAdmin)
admin.site.register(Archivo)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Tutorado, TutoradoAdmin)
admin.site.register(Reportes)
admin.site.register(Actividad)
admin.site.register(Actividad_Archivo)
admin.site.register(Entregas)
admin.site.register(Entregas_Archivo)
admin.site.register(Citas)
admin.site.register(Curso)
admin.site.register(CreditosTutorado)
admin.site.register(Creditos)
admin.site.register(QuejaSugerencia)