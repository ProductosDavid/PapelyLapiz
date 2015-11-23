
#!/usr/bin/perl

require 'template.pl';
require 'functions.pl';

BeginPage("&nbsp;");

BeginSection("Symbol set in use", "symbolset_div", "fullwidth_div");

PrintSymbolSet();

EndSection();

BeginSection("Home", "home_div", "fullwidth_div");

print "
<div id='initialmenu'>
<TABLE align='center' width='100%' class='center_tds'>
	<TR>
		<TD>
			<A HREF='cgi-bin/formulary.pl'> <IMG src='images/kreski/file-manager' /> </A>
		</TD>
		<TD>
			<A HREF='cgi-bin/choose-saved-image.pl'> <IMG src='images/kreski/gnome-fs-server' /> </A>
		</TD>
	</TR>
	<TR>
		<TD>
			<A HREF='cgi-bin/formulary.pl'>Upload an image</A>
		</TD>
		<TD>
			<A HREF='cgi-bin/choose-saved-image.pl'>Select a previously uploaded image</A>
		</TD>
	</TR>
</TABLE>
</div>
";

EndSection();

EndPage();

