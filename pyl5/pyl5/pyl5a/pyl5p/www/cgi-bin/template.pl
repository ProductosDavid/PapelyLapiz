
#!/usr/bin/perl

require 'functions.pl';


sub BeginPage
{
	($lang, $introduccion, $SESSION_DIR, $imagename) = @_;
	
	if($lang eq 'es'){
		require 'lang-ES.pl';
	}else{
		require 'lang-EN.pl';
	}
	
	my $onload="onload='toggleSectionVisibility(\"sect_2_div\");' ";
	if ($imagename){
		$onload="onload='previewImageProcessing(\"$SESSION_DIR\", \"Processing_$imagename\", \"@langLoadingPreview\", \"@langErrorOnPreview\"); toggleSectionVisibility(\"sect_1_div\"); ' ";
	}

	print << "EOF";

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" dir="ltr">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

		<base href="..">

		<meta name="robots" content="inicio, follow">
		<meta name="keywords" content="">
		<meta name="description" content="SBI for Animation for Non-Experts v1.0">
		<meta name="generator" content="Daniel ... con la ayuda de Joomla">
		<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE" />
		<META HTTP-EQUIV="Pragma" CONTENT="no-cache" />
		<META HTTP-EQUIV="Expires" CONTENT="0" />

		<title>SBI for Animation for Non-Experts v1.0</title>
		<link rel="stylesheet" href="css/template.css" type="text/css" media="screen,projection">
		<link rel="stylesheet" href="css/style.css" type="text/css" media="screen,projection">

		<script type="text/javascript" src="scripts/scripts.js"></script>
		<script type="text/javascript" src="scripts/jquery.js"></script>
		<script type="text/javascript" src="scripts/wz_jsgraphics.js"></script>
		<script type="text/javascript" src="scripts/demo.js"></script>
		<!-- script>!window.jQuery && document.write(unescape('%3Cscript src="scripts/jquery.js"%3E%3C/script%3E'))</script -->
		
		
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
		<script type="text/javascript">
		$(document).ready(function() {
			setTimeout(function() {
				// Grow/Shrink
				$('#menu3 > li > a.expanded + ul').show('normal');
				$('#menu3 > li > a').click(function() {
					$(this).toggleClass('expanded').toggleClass('collapsed').parent().find('> ul').toggle('normal');
				});
				$('#example3 .expand_all').click(function() {
					$('#menu3 > li > a.collapsed').addClass('expanded').removeClass('collapsed').parent().find('> ul').show('normal');
				});
				$('#example3 .collapse_all').click(function() {
					$('#menu3 > li > a.expanded').addClass('collapsed').removeClass('expanded').parent().find('> ul').hide('normal');
				});
			}, 250);
		});
		
		
		</script>
		
	</head>
	
	
	<body $onload style="font-size: 100%;">
		<div id="contenedor">
		
			<div id="all">
			
			
				<div id="bgleft">
				</div>
				<div id="bgright">
				</div>
				<div id="main_menu_left_image">
					<img src="images/fondobarrasmenuleft.png" border="0" style="border: 0; margin: 0px;">
				</div>
				<div id="main_menu_right_image">
					<img src="images/fondobarrasmenuright.png" border="0" style="border: 0; margin: 0px;">
				</div>
			
				<div id="header">
				
					<table width=100%>
						<tr>
							<td>
								<div class="logo1">
									<a href="http://www.uniandes.edu.co">
										<img src="images/headerUniandes.jpg" border="0" style="border: 0; margin: 0px" alt="Logo Universidad de los Andes">
									</a>
								</div>
							</td>
							<td>
								<div class="logo2">
									<a href="http://sistemas.uniandes.edu.co">
										<img src="images/headerISIS.jpg" border="0" style="border: 0; margin: 0px" alt="Logo Ingenieria de Sistemas y Comptuacion">
									</a>
								</div>
							</td>
						</tr>
						<tr>
							<td colspan="2">
								<div id="logo">
									<div class="page_title">
										<h2 class="logo"> @langProjectName </h2>
								</div>
								</div>
							</td>
						</tr>
						
						<tr>
							<td colspan="2">
								<div id="" style="text-align:right;">
									<A HREF="cgi-bin/inicio.pl?lang=es" title="@langSelectTitleES"><IMG src='images/@langSelectImgES' width='30px'/></A>&nbsp;
									<A HREF="cgi-bin/inicio.pl?lang=en" title="@langSelectTitleEN"><IMG src='images/@langSelectImgEN' width='30px'/></A>&nbsp;
									&nbsp;&nbsp;&nbsp;&nbsp;<br><br>
								</div>
							</td>
						</tr>
						
					</table>
				</div>
				
				
				<div id="principal">
					<div id="menupage">
					
						<div id="menu_item" style="width:50px;">
							<ul class="dj-main">
								<li class="submenu1">
									<a href="cgi-bin/inicio.pl?lang=$lang" class="dj-up_a">
									<span class="main_menu_item">@langHome</span>
									</a>
								</li>
							</ul>
						</div>
						
						<div id="menu_item" style="width:80px;">
							<ul class="dj-main">
								<li class="submenu1">
									<a href="http://juegos.virtual.uniandes.edu.co/" class="dj-up_a">
									<span class="main_menu_item">@langDavid</span>
									</a>
								</li>
							</ul>
						</div>
						
						<div id="menu_item" style="width:70px;">
							<ul class="dj-main">
								<li class="submenu1">
									<a href="cgi-bin/pdf_server.php?file=manual_es.pdf" class="dj-up_a">
									<span class="main_menu_item">@langUserManual</span>
									</a>
								</li>
							</ul>
						</div>
						
						<div id="menu_item" style="width:45px;">
							<ul class="dj-main">
								<li class="">
								<ul id="menu3" class="example_menu" style="text-align:right;">
									<li><a class="collapsed" style="text-align:left;width:45px;font-size:120%;">@langFAQ</a>
									<ul>
									</li>
										<li><a href="javascript:openPopUp('cgi-bin/create.pl?lang=$lang',600,300)" target="create" style="text-align:left;">@langFAQ1</a></li>
										<li><a href="javascript:openPopUp('cgi-bin/symbol.pl?lang=$lang',600,350)" target="symbol" style="text-align:left;">@langFAQ2</a></li>
										<li><a href="javascript:openPopUp('cgi-bin/mixup.pl?lang=$lang',600,350)" target="mixup" style="text-align:left;">@langFAQ3</a></li>
									</ul>
									</li>
								</ul>
								</li>
							</ul>
						</div>
						
						<div id="menu_item" style="width:1px;">
							<ul class="dj-main">
								<li class="submenu1">
									<span class="main_menu_empty" style="border-left:1px solid #BDB064;font-size: 1px; line-height: 30px;text-align: left;">&nbsp</span>
								</li>
							</ul>
						</div>
						
						<div id="menu_item" style="width:600px;">
							<ul class="dj-main">
								<li class="submenu1">
									<span class="main_menu_item"> </span>
								</li>
							</ul>
						</div>
						
						
						<div id="menu_item" style="width:100px;">
							<ul class="dj-main">
								<li class="">
								<ul id="menu3" class="example_menu" style="text-align:right;">
									<li><a class="collapsed" style="text-align:right;width:100px;font-size:120%;">@langHelp</a>
									<ul>
									</li>
										<li><a href="javascript:openPopUp('cgi-bin/option1help.pl?lang=$lang',600,300)" target="about" style="width:100px;">@langStep1Tip</a></li>
										<li><a href="javascript:openPopUp('cgi-bin/option2help.pl?lang=$lang',650,400)" target="about" style="width:100px;">@langStep2Tip</a></li>
										
										<li><a href="javascript:openPopUp('cgi-bin/about.pl?lang=$lang',600,550)" target="about" style="width:100px;">@langHelp1</a></li>
										<li><a href="javascript:openPopUp('cgi-bin/acknowledgment.pl?lang=$lang',600,300)" target="acknowledgment" style="width:100px;">@langHelp2</a></li>
									</ul>
									</li>
								</ul>
								</li>
							</ul>
						</div>
						
					</div>
				</div>

				<div id="descripcion_general">
					$introduccion
				</div>

				<div id="contentarea2">
					<!--div id="left">
						<div id="menuinformacionpara">
							<div>
								<h3>Men&uacute; principal</h3>
								<ul>
									<li>
										<a href="cgi-bin/inicio.pl">
											<span>Home</span>
										</a>
									</li>
									<li>
										<a href="cgi-bin/resultados.pl">
											<span>Resultados</span>
										</a>
									</li>
									<li>
										<a href="cgi-bin/descargar-resultados.pl">
											<span>Descargar Resultados</span>
										</a>
									</li>
								</ul>
							</div>
						</div>
						
						<div id="espmultimedia">
							<div class="moduletable">
								<h3>&nbsp;</h3>
							</div>
						</div>
						
					</div-->
					
EOF
}

sub EndPage
{
	($lang) = @_;
	
	if($lang eq 'es'){
		require 'lang-ES.pl';
	}else{
		require 'lang-EN.pl';
	}
print << "EOF";
					<div class="wrap">
					</div>
				</div>
				
				<div id="footer" style="width:100%;">
					<div class="txtfooter">
						@langContact
					</div>
					<div class="txtfooter">
						@langContactEmail
					</div>
					<div class="wrap">
					</div>
				</div>
				
				<div id="menu_item" style="width:835px">
					<ul class="dj-main">
						<li class="submenu1">
							<span class="main_menu_item"> </span>
						</li>
					</ul>
				</div>
				<div id="menu_item" style="height:70px;">
					<ul class="dj-main">
						<li class="">
							<ul id="menu3" class="example_menu" style="text-align:right;">
								<li><a class="collapsed" style="text-align:right;width:100px;font-size:120%;"> </a>
									<ul>
									</li>
										<li><a href="output/images/$SESSION_DIR/ImageProcessing.log" target="log_viewer" style="width:100px;">ImageProcessing</a></li>
										<li><a href="output/images/$SESSION_DIR/VideoGenerator.log" target="log_viewer" style="width:100px;">VideoGenerator</a></li>
										<li><a href="cgi-bin/pdf_server.php?file=programmer_es.pdf" target="log_viewer" style="width:100px;">Programmer</a></li>
										<li><a href="output/images/$SESSION_DIR/SoundFilm.log" target="log_viewer" style="width:100px;">SoundFilm</a></li>
									</ul>
								</li>
							</ul>
						</li>
					</ul>
				</div>
				</div>

			</div>
		</div>
	</body>
</html>
EOF
}

sub BeginSection
{
	($titulo, $div_name, $div_class) = @_;
print << "EOF";
                                        <div id="noticiasuniandinas">
                                                <a onclick="toggleSectionVisibility('$div_name')"><h3><img src="images/expand.gif" id="${div_name}_arrow"> $titulo</h3></a>
                                                <div class="moduletable">
                                                        <div id="mod_noticiasuniandinas">
                                                                <table id="tbnotiuniandinas" cellpadding="0" cellspacing="0" border="0" align="center">
                                                                        <tbody>
                                                                                <tr class="fila">
                                                                                        <td class="colarticulo">
												<div id="$div_name" class="$div_class">
EOF
}

sub EndSection
{
	($titulo) = @_;
print << "EOF";
                                                                                        	</div>
											</td>
                                                                                </tr>
                                                                        </tbody>
                                                                </table>
                                                        </div>
                                                </div>
                                        </div>
EOF
}


print "Content-type: text/html; charset=iso-8859-1\n\n";

