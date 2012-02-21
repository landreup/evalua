from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('evalua.views',

# Alumnes
url(r'^alumnes$', 'listadoAlumnos', {'rol': "tutor"}),
url(r'^alumnes/nou$', 'nuevoAlumno'),

)