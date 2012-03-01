from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('evalua.views',

# Professorat
url(r'^professorat$', 'listadoProfesores'),
url(r'^professorat/nou$', 'gestionProfesor'),
url(r'^professorat/(?P<profesorid>\w+)/editar?/?', 'gestionProfesor', {'accion': "editar"}),

# Alumnes
url(r'^alumnes/?$', 'listadoAlumnos', {'vista': ["coordinador"]}),
url(r'^alumnes/nou$', 'gestionAlumno'),
url(r'^alumnes/(?P<alumnoid>\w+)//?editar?/?','gestionAlumno', {'accion': "editar"}),
url(r'^(?P<profesorid>\w+)/alumnes$', 'listadoAlumnos', {'vista': ["coordinador", "tutor"]}),

# Cursos
url(r'^cursos/?$', 'listadoCursos'),
url(r'^cursos/nou/?$', 'nuevoCurso'),
url(r'^cursos/nou/confirmat/?$', 'nuevoCurso', {'confirma': True}),
)