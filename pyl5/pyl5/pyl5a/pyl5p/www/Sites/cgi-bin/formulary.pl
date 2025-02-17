#
#Papel y Lapiz - Software para la creacion de peque�os cortos.
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
use URI::Escape;

my $query = new CGI;
my $error = $query->param("error");
my $IMAGE_TEST = '../images/prueba';


print "Content-type: text/html; charset=iso-8859-1\n\n";


print << "EOF";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">

<!-- Thanks to: http://www.sitepoint.com/uploading-files-cgi-perl/ -->

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<base href="/~dwilches/sbi/" />
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE" />
        <META HTTP-EQUIV="Pragma" CONTENT="no-cache" />
        <META HTTP-EQUIV="Expires" CONTENT="0" />
	<link rel="STYLESHEET" href="css/style.css" type="text/css">
	<title>SBI for animation generation</title>
</head>
<body>
	<h1>Carga de im&aacute;genes para procesamiento</h1>
	<table width="80%" align="center">
	<form action="cgi-bin/upload.pl" method="post" enctype="multipart/form-data">
		<tr><td>Seleccione la imagen a cargar:</td></tr>
		<tr><td><input type="file" name="photo" /></td></tr>
		<tr><td><input type="submit" name="Submit" value="Subir imagen" /></td></tr>
	</form>
	</table>
EOF

if ($error)
{
	print "<P class='error'>Ocurri&oacute; un error. Posibles causas:<BR/>" .
		"(1) Usted no seleccion&oacute; ning&uacute;n archivo<BR/>" .
		"(2) El archivo seleccionado es demasiado grande (m&aacute;s de 5 Mb)</P>";
}

# Mostrar im�genes de prueba:
print "<P>Tambi&eacute;n puede probar con alguna de las siguientes im&aacute;genes de prueba:</P>";
print "<TABLE align='center'>\n";
opendir(IMAGE_DIR, $IMAGE_TEST);
my $file_number = 0;
my $FILES_PER_ROW = 3;
while (readdir(IMAGE_DIR))
{
	next unless /\.png$/;
	if (($file_number % $FILES_PER_ROW) == 0)
	{
		print "<TR>\n";
	}
	print "	<TD><IMG SRC='images/prueba/$_' WIDTH='200'><BR/>" .
		"$_<BR/>" .
		"<A HREF='images/prueba/$_'>Ver</A></BR>\n" .
		"<A HREF='cgi-bin/SBI.pl?imagetype=TEST&imagename=$_'>Ejecutar</A></BR></TD>\n";
	
	$file_number++;
	if (($file_number % $FILES_PER_ROW) == 0)
	{
		print "</TR>\n";
	}
}
closedir(IMAGE_DIR);
print "</TABLE>";


print << "EOF";
	<p class="footer">Creado por:<br/>Daniel Wilches, Agust&iacute;n Conde.</p>
</body>
</html>
EOF
