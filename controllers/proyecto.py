from evalua.models import Proyecto

from evalua.controllers.curso import cursoSeleccionado
from evalua.controllers.usuario import tutorActivo, usuarioPorId

def proyectoPorId(alumno, curso):
    return Proyecto.objects.get(alumno=alumno, curso=curso)

def proyectosPorCurso(request):
    curso = cursoSeleccionado(request)
    proyectos = Proyecto.objects.filter(curso=curso) 
    return proyectos

def proyectosPorCursoTutor(request):
    curso = cursoSeleccionado(request)
    proyectos = Proyecto.objects.filter(curso=curso, tutor=tutorActivo(request))
    return proyectos

def proyectosPorCursoTutorid(request, tutorId):
    tutor = usuarioPorId(tutorId)
    curso = cursoSeleccionado(request)
    proyectos = Proyecto.objects.filter(curso=curso, tutor=tutor)
    return proyectos

def listaProyectos(request, rol, profesorid):
    if (len(rol)==1):
        if (rol==["tutor"]):
            listado = proyectosPorCursoTutor(request)
        else:
            listado = proyectosPorCurso(request)
    else:
        listado = proyectosPorCursoTutorid(request, profesorid)
    
    return listado

def creaProyecto(request, proyecto, alumno):
    proyecto.alumno = alumno
    proyecto.curso = cursoSeleccionado()
    proyecto.save()
    
def editaProyecto(request, alumno, proyecto):
    curso = cursoSeleccionado(request)
    
    proyectoDB = proyectoPorId(alumno, curso)
    
    proyectoDB.tutor = proyecto.tutor
    proyectoDB.supervisor = proyecto.supervisor
    proyectoDB.empresa = proyecto.empresa
    proyectoDB.telefono = proyecto.telefono
    proyectoDB.titulo = proyecto.titulo
    proyectoDB.inicio = proyecto.inicio
    proyectoDB.dedicacionSemanal = proyecto.dedicacionSemanal
    proyectoDB.otrosDatos = proyecto.otrosDatos
    
    proyectoDB.save()
    