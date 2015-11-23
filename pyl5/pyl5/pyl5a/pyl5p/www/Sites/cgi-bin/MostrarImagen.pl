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

print "Content-type: text/html\n\n";

$| = 1;

my $query = new CGI;
my $imagename = $query->param("imagename");

my $THESIS_DIR = '/home/dwilches/pyl/ImageProcessing';
my $GENERATED_DIR = '/home/dwilches/pyl/ImageProcessing/Execution/Log';
my $IMAGE_TEST = '/home/dwilches/public_html/sbi/images/prueba';
my $UPLOAD_DIR = '/tmp';

print << "EOF";

<HTML>
	<HEADER>
		<META http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<base href="/~dwilches/sbi/" />
		<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE" />
		<META HTTP-EQUIV="Pragma" CONTENT="no-cache" />
		<META HTTP-EQUIV="Expires" CONTENT="0" />
		<LINK rel="STYLESHEET" href="css/style.css" type="text/css">
		<script type="text/javascript">
			var tamanoAnterior;
			
			function cambiarTamanoImagen()
			{
				var escala;
				
				if (document.imagen.height == 450)
				{
					escala = document.oculta.height / document.imagen.height;
					document.imagen.height = tamanoAnterior;
				}
				else
				{
					tamanoAnterior = document.imagen.height;
					document.imagen.height = 450;
					escala = document.imagen.height / document.oculta.height;
				}
				
				document.recuadro.style.top  = Math.floor(parseFloat(document.recuadro.style.top)  * escala);
				document.recuadro.style.left = Math.floor(parseFloat(document.recuadro.style.left) * escala);
			}
		</script>
	</HEADER>
	<BODY>

		<IMG SRC='images/recuadro.gif' WIDTH='0' HEIGHT='0' id='recuadro'
			name='recuadro' style='position:absolute;
			top: 0px; left: 0px; z-index: 3; opacity:0.4;' />

		<A onClick="cambiarTamanoImagen()">
			<IMG SRC='output/images/Processing_$imagename' id='imagen' name='imagen'
				style='position:absolute; top: 0px; left: 0px; z-index: 1;'
				/>
		</A>
		
		<IMG SRC='output/images/Processing_$imagename' id='oculta' name='oculta'
			style='position:absolute; top: 0px; left: 0px; z-index: 1; visibility:hidden;' />
EOF

