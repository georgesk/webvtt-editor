from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^addEleves$', views.addEleves, name='addEleves'),
    url(r'^listClasse$', views.listClasse, name='listClasse'),
]
