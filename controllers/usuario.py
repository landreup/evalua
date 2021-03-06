from evalua.models import Usuario

def tutorActivo(request):
    return ""

def usuarioPorId(usuarioId):
    return Usuario.objects.filter(usuarioUJI=usuarioId)

def creaUsuario(usuario):
    usuario.save()

def editaUsuario(usuarioId, usuario):
    usuarioDB = usuarioPorId(usuarioId)
    usuarioDB.nombre = usuario.nombre
    usuarioDB.usuarioUJI = usuario.usuarioUJI
    usuarioDB.rol = usuario.rol
    usuarioDB.save()

def nombreTutor(usuarioId):
    return usuarioPorId(usuarioId)[0].nombre

def usuarioPorRol(rol):
    return Usuario.objects.filter(rol=rol)

def listaCoordinador():
    return usuarioPorRol("C")

def listaTutor():
    return usuarioPorRol("T")

def listaProfesor():
    return usuarioPorRol("P")

def cambiaTutoresAProfesores():
    listadoTutores = listaTutor()
    for tutor in listadoTutores:
        tutor.rol="P"
        tutor.save()