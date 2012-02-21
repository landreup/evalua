from django.db import models

class Alumno(models.Model):
    dni = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=50)
    usuarioUJI = models.CharField(max_length=30)
    
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    usuarioUJI = models.CharField(max_length=30)
    ROL_CHOICES = (
                    ('P', 'Professor'),
                    ('T', 'Tutor'),
                    ('C', 'Coordinador')
                    )
    rol = models.CharField(max_length=1, choices=ROL_CHOICES)
    
    def __str__(self):
        return self.nombre

class Curso(models.Model):
    curso = models.CharField(max_length=15)
    
    def __str__(self):
        return self.curso

class Proyecto(models.Model):
    alumno = models.ForeignKey(Alumno, null=True)
    tutor = models.ForeignKey(Usuario)
    supervisor = models.CharField(max_length=50)
    curso = models.ForeignKey(Curso, null=True)
    
    empresa= models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    
    titulo = models.CharField(max_length=100, null=True, blank=True)
    
    inicio = models.DateField(null=True, blank=True)
    dedicacionSemanal = models.FloatField(null=True, blank=True)
    
    otrosDatos = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        unique_together = [("alumno", "curso")]
    
    
        
    