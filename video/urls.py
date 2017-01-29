from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^addEleves$', views.addEleves, name='addEleves'),
    url(r'^addProfs$', views.addProfs, name='addProfs'),
    url(r'^plusProfs$', views.plusProfs, name='plusProfs'),
    url(r'^delProf$', views.delProf, name='delProf'),
    url(r'^listClasse$', views.listClasse, name='listClasse'),
    url(r'^delClasse$', views.delClasse, name='delClasse'),
    url(r'^profClasse$', views.profClasse, name='profClasse'),
    url(r'^sousTitre/(?P<travail_id>[0-9]+)$', views.sousTitre, name='sousTitre'),
    url(r'^setTextarea$', views.setTextarea, name='setTextarea'),
    url(r'^saveTextarea$', views.saveTextarea, name='saveTextarea'),
]
