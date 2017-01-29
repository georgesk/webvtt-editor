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
			location.reload(); // on rafraîchit la page
		    }
		}
	    ]
	});
    });
}

