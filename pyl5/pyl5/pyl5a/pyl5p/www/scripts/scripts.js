/*
#
#Papel y Lapiz - Software para la creacion de pequeños cortos.
#Copyright (C) 2015  Universidad de Los Andes - Proyecto DAVID.   
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation,
#Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

*/
function cambiarTamanoImagen()
{
	// Si el tamano es el original coloco '700px', sino, coloco el original
	if ($('#imagen').width() == 700)
		$('#imagen').width('');
	else
		$('#imagen').width('700px');
	
	$('#recuadro').css('visibility', 'hidden');
}

function mostrarRecuadro(left, top, right, bottom)
{
	var image_top = $('#imagen').position().top;
	var image_left = $('#imagen').position().left;
	var image_width = $('#imagen').width();
	var image_height = $('#imagen').height();

	var scroll_top = $('#scroll').scrollTop();
	var scroll_left = $('#scroll').position().left;

	var new_top = image_top - scroll_top + Math.floor(top * image_height);
	var new_left = image_left - scroll_left + Math.floor(left * image_width);
	var new_width = Math.floor((right - left) * image_width);
	var new_height = Math.floor((bottom - top) * image_height);

	$('#recuadro').css('top', new_top + 'px');
	$('#recuadro').css('left', new_left + 'px');
	$('#recuadro').css('width', Math.max(20, new_width) + 'px');
	$('#recuadro').css('height', Math.max(20, new_height) + 'px');

	$('#recuadro').css('visibility', 'visible');
}

function cambiarCursor(nuevoCursor)
{
	document.body.style.cursor = nuevoCursor;
}

function printTimeElapsed(elapsed)
{
	return parseInt(elapsed / 60000) + ' minutes ' + parseInt((elapsed / 1000) % 60) + ' seconds';
}
/*
function executeVideoGenerator(calidad, video, imagefolder)
{

		// Extraemos informacion de tarjeta y validamos
		
		var nombrede = document.getElementById("nombrede").value;
		if ( nombrede == "" ){

			alert("falta De");
			return 0;
		}
		//var mailde = document.getElementById("mailde").value;
		var mailde = "pyl@uniandes.edu.co";
		if ( mailde.indexOf("@") > -1 ) {} else {

			alert("el correo De es incorrecto");
			return 0;
		}
		//var nombrepara = document.getElementById("nombrepara").value;
		var nombrepara = "Usuario";
		if ( nombrepara == "" ){

			alert("falta Para");
			return 0;
		}
		var mailpara = document.getElementById("mailpara").value;
		if ( mailpara.indexOf("@") > -1 ) {} else {

			alert("el correo Para es incorrecto");
			return 0;
		}
		var atext = document.getElementById("atext").value;
		if ( nombrepara == "" ){

			alert("falta mensaje");
			return 0;
		}
		for(i=0;i<atext.length;i++)
		{
			if(atext.indexOf(" ") > -1)
			{
				i = atext.indexOf(" ");
				atext = atext.replace(" ", "nbsp");
			}
		}
		
        jQuery.ajax( {
                url : "cgi-bin/VideoGenerator.pl?render_low_quality=" + calidad +
                "&render_video=" + video +
                "&imagefolder=" + imagefolder +
                "&nombrede=" + nombrede +
                "&mailde=" + mailde +
                "&nombrepara=" + nombrepara +
                "&mailpara=" + mailpara +
                "&atext=" + atext,
                success : function(html)
                {
                        $(video=="False" ? "#executeResponse" : "#videoResponse2").html(html);
                }
        } );

        $(video=="False" ? "#executeResponse" : "#videoResponse2").html(
        		video=="False" ? 
        		"<span class='success'><IMG src='images/loading' width='50'/><br/>Please wait, we are generating a preview...</span>" :
                "<span class='success'><IMG src='images/salut.png' width='50'/><br/>Perfect! Your card is being created.<br/>We are sending you an e-mail when your card is finished</span>"
        );
		if (video=="True")
			alert("Te enviaremos un correo cuando tu tarjeta este lista");
		
}

function executeImageProcessing(imagefolder, imagename)
{
        var startTime = new Date();

        jQuery.ajax( {
                url : "cgi-bin/ImageProcessing.pl?imagename=" + imagename + "&imagefolder=" + imagefolder,
                success : function(html)
                {
                        var elapsedTime = new Date() - startTime.getTime();

                        //$("#executeResponse").html("<span class=success>Image processed successfully !!<br/>(Thanks for waiting)<br/>Time elapsed: "+printTimeElapsed(elapsedTime)+"</span>");
                        //$("#executeResponse2").html(html);

                        //$("#videoResponse").css('display', 'block');
                        //$("#videoResponse").css('visibility', 'visible');
                }
        } );

        $("#executeResponse").html("<span class='success'><IMG src='images/loading' width='50'/><br/>Please wait, we are processing your sketch...</span>");
}
*/





/** Esta funcion esta basada en executeImageProcessing(imagefolder, imagename), y es para iniciar el procesamiento de la imagen **/
function previewImageProcessing(imagefolder, imagename, loadingpreview, errorpreview)
{
	/*Esta seccion borra el archivo de descripcion xml, el preview e inicia procesamiento de imagenes*/
    var startTime = new Date();
    jQuery.ajax( {
        url : "cgi-bin/ImageProcessing.pl?imagename=" + imagename + "&imagefolder=" + imagefolder,
            success : function(html)
            {
                var elapsedTime = new Date() - startTime.getTime();
            }
        } );
    $("#imagePreview").html("<span class='success'><IMG src='images/loading.gif' width='50'/><br/>" + loadingpreview + "</span>");
	
	/*Esta seccion espera a que el archivo de descripcion (xml) termine de crearse para de iniciar la previzualizacion de la escena*/
	var totalDescTime=parseInt("240000");
	var refreshDescTime=parseInt("5000");
	var isDescReady=0;
	for (var i=1; i <= totalDescTime/refreshDescTime; i++){
		setTimeout(
		function(){
			if(isDescReady==0){
				var xmlFile = "./output/images/"+imagefolder+"/script.xml";
				$.ajax({
					url:xmlFile,
					type:'get',
					dataType: 'xml',
					error: function(){
						//file not exists
						//alert('File not created ' +i.toString());
					},
					success: function(){
						//file exists
						jQuery.ajax( {
							url : "cgi-bin/VideoGenerator.pl?render_low_quality=True" +
							"&render_video=False" +
							"&imagefolder=" + imagefolder +
							"&nombrede=none" +
							"&mailde=none@none" +
							"&nombrepara=none" +
							"&mailpara=none@none" +
							"&atext=empty",
							success : function(html)
							{
								$(video=="False" ? "#executeResponse" : "#videoResponse2").html(html);
							}
						} );
						//  url : "cgi-bin/SoundFilm.pl?imagefolder=" + imagefolder + "&soundsActors=" + soundsActors + "&soundsAnimations=" + soundsAnimations,
						jQuery.ajax( {
							url : "cgi-bin/SoundFilm.pl?imagefolder=" + imagefolder,
							success : function(html)
							{
								
							}
						} );
						isDescReady=1;
					}
				});
			}else{
				//alert("xml listo"); archivo generado
			}
		},i*refreshDescTime);
	}
	
	/*Esta seccion espera a que el archivo de previsualizacion termine de crearse para mostrarse en la pagina*/
	var totalTime=parseInt("600000");
	var refreshTime=parseInt("5000");
	var isUpdated=0;
	for (var i=1; i <= totalTime/refreshTime; i++){
		setTimeout(
		function(){
			if(isUpdated==0){
				var file = "./output/images/"+imagefolder+"/output.png";
				$.ajax({
					url:file,
					type:'HEAD',
					error: function(){
						//file not exists
						var endTime=new Date();
						if( (endTime.getTime() - startTime.getTime()) >= totalTime){
							$("#imagePreview").html("<A href='#'><IMG src='images/kreski/gnome-settings'/><br><br>"+errorpreview+"</A>");
						}
					},
					success: function(){
					//file exists
						$("#imagePreview").html("<a href=\"javascript:openPopUp('output/images/"+imagefolder+"/output.png',960,555)\"><IMG SRC='output/images/"+imagefolder+"/output.png' width='100%'/></a>");
						isUpdated=1;
					}
				});
			}
		},i*refreshTime);
	}
}

/** Esta funcion esta basada en videoProcessing, y es solo para actualizar el preview (no verifica cuando termina aun...) **/
function finishImageProcessing(imagefolder)
{
	/*
	var totalTime=parseInt("600000");
	var refreshTime=parseInt("5000");
	var isUpdated=0;
	for (var i=0; i < totalTime/refreshTime; i++){
		setTimeout(
		function(){
			if(isUpdated==0){
				var file = "./output/images/"+imagefolder+"/output.png";
				$.ajax({
					url:file,
					type:'HEAD',
					error: function(){
					//file not exists
					},
					success: function(){
					//file exists
						$("#imagePreview").html("<a href=\"javascript:openPopUp('output/images/"+imagefolder+"/output.png',960,555)\"><IMG SRC='output/images/"+imagefolder+"/output.png' width='100%'/></a>");
						isUpdated=1;
					}
				});
			}
		},i*refreshTime);
	}*/
}

/** Esta funcion esta basada en videoProcessing **/
function initMailProcessing(calidad, video, imagefolder, mailsubject, langName, langEmail, langMessage, langErrorMissing, langErrorFormat, langLoadingEmail, langTryAgain)
{
		// Extraemos informacion de tarjeta y validamos
		var missing_message = "";
		var format_message = "";
		
		var nombrede = document.getElementById("nombrede").value;
		if ( nombrede == "" ){
			missing_message+="\n'" + langName + "'";
			//return 0;
		}

		var mailde = "pyl@uniandes.edu.co";
		var nombrepara = "Usuario";
		
		var mailpara = document.getElementById("mailpara").value;
		if ( mailpara == "" ){
			missing_message+="\n'" + langEmail + "'";
		}else if ( mailpara.indexOf("@") > -1 ) {} else {
			format_message+="\n'" + langEmail + "'";
			//return 0;
		}
		
		var atext = document.getElementById("atext").value;
		if ( atext == "" ){
			missing_message+="\n'" + langMessage + "'";
			//return 0;
		}

		atext = atext.replace(/\n/g,"nwln"); //"new line" sin vocales
		
			
		if (missing_message == "" && format_message == "" ){}else{
			var final_message="";
			if (missing_message != "")
				final_message+=langErrorMissing+missing_message+"\n\n";
			if (format_message != "")
				final_message+=langErrorFormat+format_message;
			alert(final_message);
			return 0;
		}
		

        jQuery.ajax( {
                url : "cgi-bin/VideoGenerator.pl?render_low_quality=" + calidad +
                "&render_video=" + video +
                "&imagefolder=" + imagefolder +
                "&nombrede=" + nombrede +
                "&mailde=" + mailde +
                "&nombrepara=" + nombrepara +
                "&mailpara=" + mailpara +
				"&subject=" + mailsubject +
                "&atext=" + atext,
                success : function(html)
                {
                        $(video=="False" ? "#executeResponse" : "#videoResponse2").html(html);
                }
        } );

		$("#mailForm").html("<span class='success'><IMG src='images/goodbye.jpg' width='80'/><br/><br/>" + langLoadingEmail + ": " + mailpara + "<br/><br/>" + langTryAgain + "</span>");
}

/** Esta funcion esta basada en initMailProcessing **/
function resendMail(imagefolder)
{
	var mailFile = "output/images/"+imagefolder+"/mail.properties";
	
	//alert("............");
	jQuery.ajax( {
		url : "cgi-bin/MailResender.pl?imagefolder="+imagefolder,
		success : function()
		{
			alert("Enviando correo");
		}
	} );
	/*
	jQuery.ajax( {
		url: mailFile,
		type:'HEAD',
		error: function(){
			//file not exists
			//alert("NOOOO");
		},
		success: function(){
			//file exists
			//alert("SI");
			jQuery.ajax( {
				url : "cgi-bin/MailResender.pl?imagefolder=" + imagefolder,
				success : function()
				{
					alert("Enviando correo");
				}
			} );
		}
	});*/
}

function toggleSectionVisibility(div_name)
{
        $("#" + div_name).toggle('slow');

	if ($("#" + div_name + "_arrow").attr('src') == 'images/collapse')
		$("#" + div_name + "_arrow").attr('src', 'images/expand');
	else
		$("#" + div_name + "_arrow").attr('src', 'images/collapse');
}

function executeSoundFilm(imagefolder)
{

	// Extraemos sonidos
        var startTime = new Date();
        var startTime = new Date();
        jQuery.ajax( {
                url : "cgi-bin/SoundFilm.pl?imagefolder=" + imagefolder,
                success : function(html)
                {
var elapsedTime = new Date() - startTime.getTime();
                }
        } );
        
}

function executeSoundFilmRadio(radioActions, radioAnimations, imagefolder)
{

	// Extraemos sonidos de actores
	var listRadio = radioActions.split("#");
	var soundsActors = "";
	for (var j = 0; j < listRadio.length; j++) {
	
		for (var i = 0; i < document.getElementsByName(listRadio[j]).length; i++)
		{
			if (listRadio[j] != "" && document.getElementsByName(listRadio[j])[i].checked)
			{
				// De la forma [sound][Label#][==][<symbol>][=][<sound>]
				soundsActors =  soundsActors + document.getElementsByName(listRadio[j])[i].value + "*";
			}
		}	
	}
	// Extraemos sonidos de animaciones
	listRadio = radioAnimations.split("#");
	var soundsAnimations = "";
	for (var j = 0; j < listRadio.length; j++) {
	
		for (var i = 0; i < document.getElementsByName(listRadio[j]).length; i++)
		{
			if (listRadio[j] != "" && document.getElementsByName(listRadio[j])[i].checked)
			{
				// De la forma [sound][Label#][==][<symbol>][=][<sound>]
				soundsAnimations =  soundsAnimations + document.getElementsByName(listRadio[j])[i].value + "*";
			}
		}	
	}	
	alert("soundsActors = " + soundsActors + ", soundsAnimations = " + soundsAnimations);
        var startTime = new Date();

        jQuery.ajax( {
                url : "cgi-bin/SoundFilm.pl?imagefolder=" + imagefolder + "&soundsActors=" + soundsActors + "&soundsAnimations=" + soundsAnimations,
                success : function(html)
                {
var elapsedTime = new Date() - startTime.getTime();
                }
        } );
}



function openPopUp(page, width, height) 
{
	var left = ($(window).width()-width)/2;
	var top = ($(window).height()-height)/2 + 50;
	window.open(page,'',"left="+left+",top="+top+",titlebars=0, toolbar=0,scrollbars=1,location=0,status=0,menubar=0,resizable=0,menubar=0,width="+width+",height="+height); 
	$(window).blur();
} 

function checkfile(file)
{
	var exist="";
	var img = new Image();
	img.src = file;
	if (img.height != 0){
		exist="True";
	}else{
		exist="False";
	}
	return exist;
}
