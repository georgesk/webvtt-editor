// Scripts pour la page d'édition des sous-titres

$(document).ready(function() { 
    var textarea=$("#tt");
    var uniqueId=parseInt($("#uniqueId").val());
    $.get(
	"/video/setTextarea",
	{uid: uniqueId},
	function(data){
	    textarea.text(data.txt);
	}
    );
});

function saveTextarea(uid){
    $.post("/video/saveTextarea",
	{
	    uid: uid,
	    txt: $("#tt").val(),
	    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
	},
	function(data){
	    $("#dialog").html("Les sous-titres sont enregistrés");
	    $("#dialog").dialog({
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
			},
		    }
		]
	    });
	    window.location.href = window.location.protocol +'//'+ window.location.host + window.location.pathname;
	}
       );
}
