// scripts nécessaires à la page addEleves
// jQuery est défini dans ce contexte, ansi que jQuery-UI

function voirClasse(c){
    $.get("listClasse", {classe: c}, function(data){
	$("#dialog").html(data.eleves);
	$( "#dialog" ).dialog({
	    autoOpen: true,
	    modal: true,
	    buttons: [
		{
		    text: "OK",
		    icons: {
			primary: "ui-icon-heart"
		    },
		    click: function() {
			$( this ).dialog( "close" );
		    }
		}
	    ]
	});
    });
}

function effacerClasse(c){
    $.get("delClasse", {classe: c}, function(data){
	$("#dialog").html("Effacement de "+c);
	$( "#dialog" ).dialog({
	    autoOpen: true,
	    modal: true,
	    buttons: [
		{
		    text: "OK",
		    icons: {
			primary: "ui-icon-heart"
		    },
		    click: function() {
			$( this ).dialog( "close" );
			window.location.href = window.location.protocol +'//'+ window.location.host + window.location.pathname;
		    }
		}
	    ]
	});
    });
}

function ajouteProfs() {
    var checks=$("input:checked");
    var nomProfs=[], idProfs=[];
    for (var i=0; i < checks.length; i++){
	nomProfs.push($(checks[i]).parent().text().trim());
	idProfs.push(parseInt(checks[i].id));
    }
    $.post("plusProfs", {
	ids: JSON.stringify(idProfs),
	csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    }, function(data){
	$("#dialog").html("Inscription de : " + nomProfs.join(", "));
	$( "#dialog" ).dialog({
	    autoOpen: true,
	    modal: true,
	    dialogClass: "no-close",
	    buttons: [
		{
		    text: "OK",
		    icons: {
			primary: "ui-icon-heart"
		    },
		    click: function() {
			$( this ).dialog( "close" );
			window.location.href = window.location.protocol +'//'+ window.location.host + window.location.pathname;
		    }
		}
	    ]
	});
    });
}

function delProf(uid){
    $.post("delProf", {
	uid: uid,
	csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    }, function(data){
	$("#dialog").html("Suppression terminée");
	$( "#dialog" ).dialog({
	    autoOpen: true,
	    modal: true,
	    dialogClass: "no-close",
	    buttons: [
		{
		    text: "OK",
		    icons: {
			primary: "ui-icon-heart"
		    },
		    click: function() {
			$( this ).dialog( "close" );
			window.location.href = window.location.protocol +'//'+ window.location.host + window.location.pathname;
		    }
		}
	    ]
	});
    });    
}


/**
 * présente la liste des classes que le prof n'a pas, et lui permet de piquer
 * dedans.
 **/
function profClasse(uid){
    $.post("profClasse",
	   {
	       uid: uid,
	       req: "possibles",
	       csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
	   },
	   function(data){
	       var dial=$("#dialog");
	       dial.html(""); // efface le dialogue
	       var sel=$("<select>",{
		   id: "sel",
		   width: "250px",
		   height: "400px",
		   overflow: "auto",
		   multiple: "on",
	       });
	       dial.append(sel);
	       for(var i = 0; i < data.classes.length; i++){
		   // vérifier l'absence de la classe data.classes[i]
		   // dans data.owned
		   var op=$("<option>",{
		       value: data.classes[i].gid,
		   }).text(data.classes[i].classe);
		   for (var j=0; j < data.owned.length; j++){
		       if (data.owned[j].gid == data.classes[i].gid){
			   op.attr("selected","on");
		       }
		   }
		   sel.append(op);
	       }
	       dial.dialog({
		   autoOpen: true,
		   modal: true,
		   dialogClass: "no-close",
		   buttons: [
		       {
			   text: "OK",
			   icons: {
			       primary: "ui-icon-heart"
			   },
			   click: function() {
			       $( this ).dialog( "close" );
			       // do someting useful with the selection!
			       var os=$("#sel option:selected");
			       var classes=[];
			       for (var i=0; i<os.length; i++){
				   classes.push({
				       gid: parseInt(os[i].value),
				       classe: $(os[i]).text()
				   });
			       }
			       $.post(
				   "profClasse",
				   {
				       classes: JSON.stringify(classes),
				       uid: uid,
				       csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
				       req: "choisis",
				   },
				   function(data){
				       window.location.href = window.location.protocol +'//'+ window.location.host + window.location.pathname;
				   }
			       );
			   }
		       }
		   ]
	       });

	   }
	  );
}
