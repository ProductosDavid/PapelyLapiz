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
#!/usr/bin/perl

#use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use Data::Dumper;
use File::Copy;
use Digest::MD5;

require 'paths.pl';
require 'template.pl';
require 'functions.pl';

$| = 1;

my $query = new CGI;
my $imagename = $query->param("imagename");
my $uploaddir = $query->param("uploaddir");

my $THESIS_DIR = "$ROOT_PATH/ImageProcessing";
my $GENERATED_DIR = "$THESIS_DIR/Execution/Log";
my $IMAGE_TEST = "$WEB_ROOT_PATH/images/prueba";
my $UPLOAD_DIR = $uploaddir eq "" ? $TEMP_PATH : "$WEB_ROOT_PATH/output/images/$uploaddir";


# Genero una identificacion unica para esta imagen
$md5 = Digest::MD5->new;
open TMP_FILE, "$UPLOAD_DIR/$imagename";
$md5->addfile(TMP_FILE);
$md5_checksum = $md5->hexdigest;
close TMP_FILE;

my $SESSION_DIR = $md5_checksum;

# copiar al directorio accesible por Apache la imagen que el usuario subio
mkdir "$GENERATED_DIR/$SESSION_DIR";

if ($imagename =~ 'Processing_')
{
	copy "$UPLOAD_DIR/$imagename", "$GENERATED_DIR/$SESSION_DIR/$imagename";
	$imagename =~ s/Processing_//;
}
else
{
	copy "$UPLOAD_DIR/$imagename", "$GENERATED_DIR/$SESSION_DIR/Processing_$imagename";
}

BeginPage("You can click on the section titles to hide/show the contents", $SESSION_DIR);

BeginSection("Symbol set in use", "symbolset_div", "fullwidth_div");

PrintSymbolSet();

EndSection();

BeginSection("Choosen image ($imagename)", "choosen_image_div");

print "
	<div id='scroll'>
		<center>
			<A onClick='cambiarTamanoImagen()'>
				<IMG SRC='images/recuadro.png' id='recuadro'
					style='z-index:10; position:absolute; visibility:hidden;' />

				<IMG SRC='output/images/$SESSION_DIR/Processing_$imagename' id='imagen'
					style='position:relative; top: 0px; left: 0px; z-index: 1;' />
			</A>
		</center>
	</div>
		
	<script type='text/javascript'>
		cambiarTamanoImagen();
	
		\$('#scroll').scroll(function()
		{
			\$('#recuadro').css('visibility','hidden');
		});
	</script>
";

EndSection();

BeginSection("Card", "sect_2_div");

print "
<div id='card'>
		De   :<br/> <input type=\"text\" name=\"de\"><br>
		Correo de   :<br/> <input type=\"text\" mailde=\"de\"><br>
		Para :<br/> <input type=\"text\" name=\"para\"><br>
		Correo para   :<br/> <input type=\"text\" mailpara=\"de\"><br>
		Texto:<br/> <textarea name=\"atext\" rows=\"10\" cols=\"50\"></textarea> 
</div>
";

EndSection();

BeginSection("Preview", "sect_1_div");

print "
<div id='executeResponse'>
<A onclick='alert(\"listo para reconocer\");executeImageProcessing(\"$SESSION_DIR\", \"Processing_$imagename\");
			alert(\"listo para preview\");
			executeVideoGenerator(\"True\",\"False\", \"$SESSION_DIR\")'>
	<IMG src='images/kreski/gnome-settings' /><br/>Click in this icon to preview</A>
</div>";

EndSection();

BeginSection("Compose", "sect_1_div");

print "
<div id='hola'>
<A onclick='executeImageProcessing(\"$SESSION_DIR\", \"Processing_$imagename\");
			executeSoundFilm(\"$SESSION_DIR\");
			executeVideoGenerator(\"False\",\"True\", \"$SESSION_DIR\")'>
	<IMG src='images/kreski/gnome-settings' /><br/>Click in this icon to compose</A>
</div>";

EndSection();

print "</div>";

EndPage();

