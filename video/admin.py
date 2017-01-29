from django.contrib import admin

# Register your models here.

from .models import Etudiant, Enseignant, EnseignantClasse, \
    Atelier, Travail

admin.site.register(Etudiant)
admin.site.register(Enseignant)
admin.site.register(EnseignantClasse)
admin.site.register(Atelier)
admin.site.register(Travail)
