from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import *

from .models import Etudiant, Enseignant
from .ldapUtils import estProfesseur

def index(request):
    return render(request, "preparation.html")
