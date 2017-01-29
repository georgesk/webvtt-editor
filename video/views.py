from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import json

from webtt.settings import connection
from .models import Etudiant, Enseignant
#from .csvResult import csvResponse
#from .odfResult import odsResponse, odtResponse
from collections import OrderedDict

def nomClasse(s):
    """
    Correction des noms des classes ;
    dans notre annuaire, toutes les classes sont préfixées par "c"
    @param s une chaîne commençant par "c"
    @return la chaîne sans le préfixe "c"
    """
    if s[0]=="c":
        return s[1:]
    else:
        return s

# Create your views here.

def index(request):
    return HttpResponse("Hello, voici l'index des votes.")

def addEleves(request):
    """
    Une page pour ajouter des élèves à l'atelier de sous-titrage
    """
    eleves=[]
    wantedClasses = request.POST.getlist("classes")
    ######################################
    # affichage des élèves ajoutés
    ######################################
    if wantedClasses:
        for gid in wantedClasses:
            ### récupération du nom de la classe
            base_dn = 'ou=Groups,dc=lycee,dc=jb'
            filtre  = '(gidNumber={})'.format(gid)
            connection.search(
                search_base = base_dn,
                search_filter = filtre,
                attributes=["cn" ]
                )
            for entry in connection.response:
                cn=nomClasse(entry['attributes']['cn'][0])
            ### récupération des élèves inscrits dans la classe
            base_dn = 'ou=Users,dc=lycee,dc=jb'
            filtre  = '(&(objectClass=kwartzAccount)(gidNumber={}))'.format(gid)
            connection.search(
                search_base = base_dn,
                search_filter = filtre,
                attributes=["uidNumber", "sn", "givenName", "uid" ]
                )
            for entry in connection.response:
                eleves.append(
                    {
                        "uidNumber":entry['attributes']['uidNumber'][0],
                        "uid":entry['attributes']['uid'][0],
                        "nom":entry['attributes']['sn'][0],
                        "prenom":entry['attributes']['givenName'][0],
                        "classe": cn,
                    }
                )
        eleves.sort(key=lambda e: "{classe} {nom} {prenom}".format(**e))
        for e in eleves:
            etudiant=Etudiant.objects.filter(uid=e["uid"])
            if not etudiant:
                ## création d'un nouvel enregistrement
                etudiant=Etudiant(uidNumber=e["uidNumber"],uid=e["uid"],
                                  nom=e["nom"], prenom=e["prenom"],
                                  classe=e["classe"])
                etudiant.save()
    base_dn = 'ou=Groups,dc=lycee,dc=jb'
    filtre = '(&(cn=c*)(!(cn=*smbadm))(objectclass=kwartzGroup))'
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes = ['cn', 'gidnumber'],
    )
    classes=[]
    for entry in connection.response:
        classes.append({
            'gid':entry['attributes']['gidNumber'][0],
            'classe':nomClasse(entry['attributes']['cn'][0]),
        })
    ### Liste des classes déjà connues dans la base de données
    etudiants=list(Etudiant.objects.all())
    classesDansDb=list(set([nomClasse(e.classe) for e in Etudiant.objects.all()]))
    classesDansDb.sort()
    return render(
        request, "addEleves.html",
        context={
            "classes": classes,
            "eleves":  eleves,
            "classesDansDb" : classesDansDb,
        }
    )

def listClasse(request):
    c=request.GET.get("classe")
    etudiants=Etudiant.objects.filter(classe=c)
    eleves=[e.nom+" "+e.prenom for e in etudiants]
    return JsonResponse({
        "eleves": "<br/>".join(eleves),
    })
