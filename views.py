from django.shortcuts import render_to_response
from models import Proyecto, Usuario, Curso, Alumno
from django.http import HttpResponseRedirect, HttpResponseNotFound
from forms import UsuarioForm, AlumnoForm, ProyectoForm
import datetime

def listadoAlumnos(request, rol, profesorid=""):
    listaProyectos= Proyecto.objects.all()
    
    if (rol=="tutor"):
        titulo = "Alumnes Assignats"
        listaProyectos= Proyecto.objects.all()
    elif (rol=="coordinador"):
        titulo = "Gestio d'Alumnes"
    elif (rol=="coordinador-tutor"):
        rol = ["coordinador", "tutor"]
        tutor = Usuario.objects.filter(usuarioUJI=profesorid)
        if (not tutor):
            return HttpResponseNotFound()
        titulo = "Alumnes de " + tutor[0].nombre
        listaProyectos = Proyecto.objects.filter(tutor=tutor[0].id)
    
    return render_to_response('alumnoListado.html', {'listaProyectos': listaProyectos, 'rol': rol, 'titulo': titulo})

def listadoProfesores(request):
    listaCoordinadores = Usuario.objects.filter(rol="C")
    listaTutores = Usuario.objects.filter(rol="T")
    listaProfesores = Usuario.objects.filter(rol="P")
    return render_to_response('profesorListado.html', {'listaCoordinadores': listaCoordinadores, 'listaTutores': listaTutores, 'listaProfesores': listaProfesores})

def listadoCursos(request):
    listaCursos = Curso.objects.all().order_by("-id")
    return render_to_response('cursoListado.html', {'listaCursos': listaCursos})

def nuevoCurso(request, confirma="no"):
    cursoActual = int(datetime.date.today().year)
    cursoNuevo = str(cursoActual)+"/"+str(cursoActual+1)
    if (confirma == "si"):
        cursos = Curso.objects.filter(curso=cursoNuevo)
        if ( not cursos):
            curso = Curso(curso=cursoNuevo)
            curso.save()
            listaTutores = Usuario.objects.filter(rol="T")
            for tutor in listaTutores:
                tutor.rol="P"
                tutor.save()
                
        return HttpResponseRedirect('/coordinacio/cursos')
    else:
        existe = False
        cursos = Curso.objects.filter(curso=cursoNuevo)
        if (cursos) :
            existe = True
    return render_to_response('cursoNuevo.html', {'curso': cursoNuevo, 'existe': existe})

def gestionProfesor(request, accion="nuevo", profesorid=""):
    profesorid = profesorid if (profesorid[-1]!='/') else profesorid[:-1]
    if (request.method == "POST" ) :
        usuario = Usuario()
        form = UsuarioForm(request.POST, instance=usuario)
        if (form.is_valid()):
            if (accion =="nuevo") :
                form.save()
            else:
                usuarioDB = Usuario.objects.get(usuarioUJI=profesorid)
                usuarioDB.nombre = usuario.nombre
                usuarioDB.usuarioUJI = usuario.usuarioUJI
                usuarioDB.rol = usuario.rol
                usuarioDB.save()
            return HttpResponseRedirect('/coordinacio/professorat')
    else:
        if ( accion == "nuevo" ):
            form = UsuarioForm()
        else :
            profesor = Usuario.objects.filter(usuarioUJI=profesorid)
            if ( not profesor ) :
                return HttpResponseNotFound()
            form = UsuarioForm(initial = {
                                'nombre': profesor[0].nombre,
                                'usuarioUJI': profesor[0].usuarioUJI,
                                'rol': profesor[0].rol
                    })
    return render_to_response('profesorGestion.html', {'form': form, 'accion': accion, 'professorid': profesorid})

def gestionAlumno(request, accion="nuevo", alumnoid=""):
    if (request.method == "POST") :
        alumno = Alumno()
        proyecto = Proyecto()
        form_alumno = AlumnoForm(request.POST, prefix='alumno', instance=alumno)
        form_proyecto = ProyectoForm(request.POST, prefix='proyecto', instance=proyecto)
        if (form_alumno.is_valid() and form_proyecto.is_valid()):
            curso = Curso.objects.order_by("-id")[0]
            if (accion == nuevo):
                alumno.save()
                proyecto.alumno = alumno
                proyecto.curso = curso
                proyecto.save()
            else :
                alumnoDB = Alumno.objects.get(usuarioUJI=alumnoid)
                alumnoDB.nombre = alumno.nombre
                alumnoDB.usuarioUJI = alumno.usuarioUJI
                alumnoDB.dni = alumno.dni
                proyectoDB = Proyecto.objects.get(alumno=alumnoDB, curso=curso)
                proyectoDB.tutor = proyecto.tutor
                proyectoDB.supervisor = proyecto.supervisor
                proyectoDB.empresa = proyecto.empresa
                proyectoDB.telefono = proyecto.telefono
                proyectoDB.titulo = proyecto.titulo
                proyectoDB.inicio = proyecto.inicio
                proyectoDB.dedicacionSemanal = proyecto.dedicacionSemanal
                proyectoDB.otrosDatos = proyecto.otrosDatos
            return HttpResponseRedirect('/coordinacio/cursos')
    else: 
        if (accion != "nuevo" ):
            alumno = Alumno.objects.filter(usuarioUJI=alumnoid)
            if (not alumno):
                return HttpResponseNotFound()
            form_alumno = AlumnoForm(prefix='alumno', initial={'dni' : alumno[0].dni, 'nombre': alumno[0].nombre, 'usuarioUJI': alumno[0].usuarioUJI})
            
            proyecto = Proyecto.objects.filter(alumno=alumno, curso=Curso.objects.order_by('-id')[0])
            if (not proyecto) :
                return HttpResponseNotFound()
            form_proyecto = ProyectoForm(prefix='proyecto', initial={
                                        'tutor': proyecto[0].tutor, 
                                        'supervisor': proyecto[0].supervisor, 
                                        'empresa': proyecto[0].empresa, 
                                        'telefono': proyecto[0].telefono,
                                        'titulo': proyecto[0].titulo,
                                        'inicio': proyecto[0].inicio,
                                        'dedicacionSemanal': proyecto[0].dedicacionSemanal,
                                        'otrosDatos': proyecto[0].otrosDatos
                            })
            form_proyecto.fields["tutor"].queryset = Usuario.objects.filter(rol="T")
            form_proyecto.initial["tutor"] = proyecto[0].tutor
        else:
            form_alumno = AlumnoForm(prefix='alumno')
            form_proyecto = ProyectoForm(prefix='proyecto')
            form_proyecto.fields["tutor"].queryset = Usuario.objects.filter(rol="T")
        
    return render_to_response('alumnoGestion.html', {
                                                   'accion': accion,
                                                   'alumnoid': alumnoid,
                                                   'form_alumno': form_alumno, 
                                                   'form_proyecto': form_proyecto,
                                                   })
