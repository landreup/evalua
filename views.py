from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from forms import ProfesorForm, AlumnoProyectoForm
from evalua.controllers.titulos import tituloListadoProyectos
from evalua.controllers.proyecto import listaProyectos
from evalua.controllers.usuario import listaCoordinador, listaTutor, listaProfesor
from evalua.controllers.curso import cursoNuevo, listaCursoTodos, creaCurso
  
def listadoAlumnos(request, vista, profesorid=""):
    titulo = tituloListadoProyectos(vista, profesorid)
    listadoProyectos = listaProyectos(request, vista, profesorid)
    
    return render_to_response('alumnoListado.html', {'listaProyectos': listadoProyectos, 'rol': vista, 'titulo': titulo})

def listadoProfesores(request):
    listadoCoordinadores = listaCoordinador()
    listadoTutores = listaTutor()
    listadoProfesores = listaProfesor()
    return render_to_response('profesorListado.html', {'listaCoordinadores': listadoCoordinadores, 'listaTutores': listadoTutores, 'listaProfesores': listadoProfesores})

def listadoCursos(request):
    listadoCursos = listaCursoTodos()
    return render_to_response('cursoListado.html', {'listaCursos': listadoCursos})

def nuevoCurso(request, confirma=False):
    curso = cursoNuevo()
    existe = False
    if (confirma):
        existe = creaCurso(curso)
        if (not existe) : return HttpResponseRedirect('/coordinacio/cursos')
    
    return render_to_response('cursoNuevo.html', {'curso': curso, 'existe': existe})

def gestionProfesor(request, accion="nuevo", profesorid=""):
    #profesorid = profesorid if (profesorid[-1]!='/') else profesorid[:-1]
    if (request.method == "POST" ) :
        form = ProfesorForm(request, accion, profesorid, "lee")
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/professorat')
    else:
        form = ProfesorForm(request, accion, profesorid)
    
    # CAMBIAR PLANTILLA PARA QUE RECIBA SOLO UN FORMULARIO
    return render_to_response('profesorGestion.html', {'form': form.usuarioForm, 'accion': accion, 'professorid': profesorid})

def gestionAlumno(request, accion="nuevo", alumnoid=""):
    if (request.method == "POST") :
        form = AlumnoProyectoForm(request, accion, alumnoid, "lee")
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/coordinacio/cursos')
    else: 
        form = AlumnoProyectoForm(request, accion, alumnoid)
    
    # CAMBIAR PLANTILLA PARA QUE RECIBA SOLO UN FORMULARIO
    return render_to_response('alumnoGestion.html', {
                                                   'accion': accion,
                                                   'alumnoid': alumnoid,
                                                   'form_alumno': form.alumnoForm, 
                                                   'form_proyecto': form.proyectoForm,
                                                   })
