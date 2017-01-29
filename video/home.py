from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import *

from .models import Etudiant, Enseignant, Travail
from .ldapUtils import estProfesseur


def index(request):
    etudiant=Etudiant.objects.filter(uid=request.user)[0]
    travaux=Travail.objects.filter(etudiant=etudiant)
    return render(request, "home.html",context={
        "etudiant": etudiant,
        "travaux": travaux,
    })
