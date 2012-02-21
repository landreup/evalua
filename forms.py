from models import Usuario, Alumno, Proyecto
from django.forms import ModelForm

class UsuarioForm(ModelForm):
    class Meta():
        model = Usuario
        
class AlumnoForm(ModelForm):
    class Meta():
        model = Alumno  

class ProyectoForm(ModelForm):
    class Meta():
        model = Proyecto
        exclude = ('curso', 'alumno')