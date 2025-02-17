
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

