# divers utilitaires, dont les requêtes à l'annuaire du lycée
from webtt.settings import connection
from .models import Etudiant, Enseignant, EnseignantClasse

def uid2enseignant(uid):
    """
    consulte l'annuaire et crée un objet Enseignant
    @param uid l'identifiant
    @result un objet Enseignant
    """
    base_dn = 'ou=Groups,dc=lycee,dc=jb'
    filtre  = '(cn=profs)'
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes=["gidNumber" ]
        )
    gid=connection.response[0]['attributes']["gidNumber" ][0]
    # à ce stade gid est le groupe des profs
    ### récupération des profs
    base_dn = 'ou=Users,dc=lycee,dc=jb'
    filtre  = '(&(uidNumber={})  (&(objectClass=kwartzAccount)(gidNumber={})))'.format(uid,gid)
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes=["uidNumber", "sn", "givenName" ]
        )
    ## liste des uids de profs déjà dans l'atelier
    uids=[p.uid for p in Enseignant.objects.all()]
    for entry in connection.response:
        if int(entry['attributes']['uidNumber'][0]) not in uids:
            ## on n'ajoute le prof que s'il n'est pas encore dans l'atelier
            try:
                prof=Enseignant(
                    uid=entry['attributes']['uidNumber'][0],
                    nom=entry['attributes']['sn'][0],
                    prenom=entry['attributes']['givenName'][0],
                )
            except:
                prof=None
                pass # par exemple s'il n'y a pas d'attribut givenName
            return prof
    
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

def getAllProfs():
    """
    fait la liste de tous les profs de l'annuaire et absents de la
    barrette
    """
    base_dn = 'ou=Groups,dc=lycee,dc=jb'
    filtre  = '(cn=profs)'
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes=["gidNumber" ]
        )
    gid=connection.response[0]['attributes']["gidNumber" ][0]
    profs=[]
    base_dn = 'ou=Groups,dc=lycee,dc=jb'
    filtre  = '(gidNumber={})'.format(gid)
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes=["cn" ]
        )
    for entry in connection.response:
        cn=nomClasse(entry['attributes']['cn'][0])
    ### récupération des profs
    base_dn = 'ou=Users,dc=lycee,dc=jb'
    filtre  = '(&(objectClass=kwartzAccount)(gidNumber={}))'.format(gid)
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes=["uidNumber", "sn", "givenName" ]
        )
    ## liste des uids de profs déjà dans la barrette
    uids=[p.uid for p in Enseignant.objects.all()]
    for entry in connection.response:
        if int(entry['attributes']['uidNumber'][0]) not in uids:
            ## on n'ajoute le prof que s'il n'est pas encore dans la barrette
            try:
                profs.append(
                    {
                        "uid":entry['attributes']['uidNumber'][0],
                        "nom":entry['attributes']['sn'][0],
                        "prenom":entry['attributes']['givenName'][0],
                    }
                )
            except:
                pass # par exemple s'il n'y a pas d'attribut givenName
    profs.sort(key=lambda e: "{nom} {prenom}".format(**e))
    return profs

def getProfs(uids):
    """
    récupère une liste de profs étant donné la liste de leurs uids
    """
    base_dn = 'ou=Groups,dc=lycee,dc=jb'
    filtre  = '(cn=profs)'
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes=["gidNumber" ]
        )
    gid=connection.response[0]['attributes']["gidNumber" ][0]
    profs=[]
    base_dn = 'ou=Users,dc=lycee,dc=jb'
    filtre  = '(&(objectClass=kwartzAccount)(gidNumber={gid})(|{uids}))'.format(
        gid=gid,
        uids=" ".join(["(uidNumber={})".format(uid) for uid in uids]),
    )
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes=["uidNumber", "sn", "givenName" ]
    )
    for entry in connection.response:
        profs.append(
            {
                "uid":entry['attributes']['uidNumber'][0],
                "nom":entry['attributes']['sn'][0],
                "prenom":entry['attributes']['givenName'][0],
            }
        )
    profs.sort(key=lambda e: "{nom} {prenom}".format(**e))
    return profs

def getEleves(gid):
    """
    renvoie une liste d'élèves dans une classe, selon l'annuaire
    @param gid : un identifiant de groupe classe
    @return une liste d'élèves
    """
    eleves=[]
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
    return eleves

def getClasses():
    """
    renvoie les classes connues de l'annuaire
    """
    classes=[]
    base_dn = 'ou=Groups,dc=lycee,dc=jb'
    filtre = '(&(cn=c*)(!(cn=*smbadm))(objectclass=kwartzGroup))'
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes = ['cn', 'gidnumber'],
    )
    for entry in connection.response:
        classes.append({
            'gid':entry['attributes']['gidNumber'][0],
            'classe':nomClasse(entry['attributes']['cn'][0]),
        })
    return classes

def ownedClasses(uid, classes):
    """
    Renvoie la liste des classe d'un prof
    @param uid l'identifiant du prof
    @param classes une liste de dicos gid=> entier classe=> chaine
    @return un sous-ensemble de classes
    """
    result=[]
    owned=list(EnseignantClasse.objects.filter(enseignant__uid=uid))
    gids=[ec.gid for ec in owned]
    for c in classes:
        if c["gid"] in gids:
            result.append(c)
    return result

def estProfesseur(user):
    """
    Vérifie si un utilisateur (au sens ldap) est un professeur
    de la table Enseignant
    @param user un objet django de type User
    @return un statut: "non", "prof" ou "profAP", selon que c'est un
    non-enseignant, un enseignant extérieur à l'AP, ou un prof de la table
    Enseignant.
    """
    result="non"
    nom=user.last_name
    prenom=user.first_name
    login=user.username
    #### récupération du numéro du groupe des profs
    base_dn = 'ou=Groups,dc=lycee,dc=jb'
    filtre  = '(cn=profs)'
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes=["gidNumber" ]
        )
    gid=connection.response[0]['attributes']["gidNumber" ][0]
    #### d'abord, user est-il prof ?
    base_dn = 'ou=Users,dc=lycee,dc=jb'
    filtre  = '(&(objectClass=kwartzAccount)(gidNumber={0})(uid={1}))'.format(gid, login)
    connection.search(
        search_base = base_dn,
        search_filter = filtre,
        attributes=["uidNumber", "sn", "givenName" ]
        )
    if len(connection.response) > 0: # on a affaire à un prof.
        if len(Enseignant.objects.filter(nom=nom, prenom=prenom))==0:
            result="prof"
        else:
            result="profAP"
    return result

