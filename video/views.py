from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import json

from .models import Etudiant, Enseignant, EnseignantClasse
#from .csvResult import csvResponse
#from .odfResult import odsResponse, odtResponse
from collections import OrderedDict

from .ldapUtils import nomClasse, getAllProfs, getProfs, getEleves, \
    getClasses, uid2enseignant, ownedClasses

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
            eleves+=getEleves(gid)
        eleves.sort(key=lambda e: "{classe} {nom} {prenom}".format(**e))
        for e in eleves:
            etudiant=Etudiant.objects.filter(uid=e["uid"])
            if not etudiant:
                ## création d'un nouvel enregistrement
                etudiant=Etudiant(uidNumber=e["uidNumber"],uid=e["uid"],
                                  nom=e["nom"], prenom=e["prenom"],
                                  classe=e["classe"])
                etudiant.save()
    classes=getClasses()
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

def delClasse(request):
    c=request.GET.get("classe")
    etudiants=Etudiant.objects.filter(classe=c)
    etudiants.delete()
    return JsonResponse({
        "status": "ok",
    })

def addProfs(request):
    """
    Une page pour ajouter des profs à un atelier de sous-titrage
    """
    profs=getAllProfs()
    profsAP=Enseignant.objects.all()
    pClasse=[]
    for p in profsAP:
        classes=[ec.classe for ec in EnseignantClasse.objects.filter(enseignant__uid=p.uid)]
        pClasse.append({"nom": "{} {}".format(p.nom, p.prenom),
                        "classes": classes,
                        "uid": p.uid,
        })
    return render(
        request, "addProfs.html",
        context={
            "profs":  profs,
            "profsAP": profsAP,
            "pClasse": pClasse,
        }
    )

def plusProfs(request):
    ids=eval(request.POST.get("ids"))
    for id in ids:
        prof=uid2enseignant(id)
        if prof:
            prof.save()
    return JsonResponse({
        "status": "ok",
    })
    
def delProf(request):
    uid=int(request.POST.get("uid"))
    p=Enseignant.objects.filter(uid=uid)
    if p:
        p[0].delete()
    return JsonResponse({
        "status": "ok",
    });

def profClasse(request):
    uid=int(request.POST.get("uid"))
    req=request.POST.get("req")
    if req=="possibles":
        classes=getClasses()
        owned=ownedClasses(uid,classes)
        return JsonResponse({
            "status": "ok",
            "classes": classes,
            "owned": owned,
        });
    elif req == "choisis":
        classes=json.loads(request.POST.get("classes"))
        owned=[ec.gid for ec in EnseignantClasse.objects.filter(enseignant__uid=uid)]
        required=[c["gid"] for c in classes]
        e=Enseignant.objects.filter(uid=uid)[0]
        ## ajout des classes non encore possédées
        for c in classes:
            if c["gid"] not in owned:
                ec= EnseignantClasse(enseignant=e, classe=c["classe"], gid=c["gid"])
                ec.save()
                ## effacement des classe non requises
        for ec in EnseignantClasse.objects.filter(enseignant__uid=uid):
            if ec.gid not in required:
                ec.delete()
        return JsonResponse({
            "status": "ok",
        });
