from django.db import models

# Create your models here.

class Etudiant(models.Model):
    """
    Représente un étudiant qui peut "sous-titrer". Les champs "uidNumber" et
    "uid" identifient l'étudiant dans l'annuaire LDAP de 
    l'établissement.
    """
    uidNumber = models.IntegerField(unique=True)
    uid       = models.CharField(max_length=50)
    nom       = models.CharField(max_length=50)
    prenom    = models.CharField(max_length=50)
    classe    = models.CharField(max_length=10)

    def __str__(self):
        return "{nom} {prenom} {classe} {uid}".format(**self.__dict__)
    

class Enseignant(models.Model):
    """
    Désigne un professeur ou un autre membre de l'équipe éducative.
    le champ "uid" correspond à l'identifiant de ce professeur dans 
    l'annuaire LDAP de l'établissement.
    """
    uid    = models.IntegerField(unique=True)
    nom   = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)

    def __str__(self):
        return "{} (prof)".format(self.nom)
    
class EnseignantClasse(models.Model):
    """
    associe un professeur à une classe
    """

    enseignant = models.ForeignKey(Enseignant)
    classe= models.CharField(max_length=50)
    gid = models.IntegerField() ## groupe ldap de la classe

    def __str__(self):
        return "{} -> {}".format(self.enseignant.nom, self.classe)

class Atelier(models.Model):
    """
    associe une vidéo et peut-être des sous-titres à une classe et un prof
    """
    ec =  models.ForeignKey(EnseignantClasse)
    video = models.FileField(upload_to='video')
    tt    = models.TextField(default="WEBTT\n\n")

    def __str__(self):
        return "{} {} {}".format(self.ec, self.video, self.tt[:20]+"...")

class Travail(models.Model):
    """
    décrit le travail d'un élève dans un atelier
    """
    atelier=models.ForeignKey(Atelier)
    tt = models.TextField()
    etudiant=models.ForeignKey(Etudiant)

    def __str__(self):
        return "{} {} {}".format(self.etudiant,
                                 self.tt[:30]+"...",
                                 self.atelier)

    
