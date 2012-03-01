from evalua.controllers.usuario import nombreTutor

def tituloListadoProyectos(vista, profesorid):
    if (len(vista) == 1 ):
        titulo = "Alumnes Assignats" if vista == ["tutor"] else "Gestio d'Alumnes"
    else :
        titulo = "Alumnes de " + nombreTutor(profesorid)    
    return titulo
    