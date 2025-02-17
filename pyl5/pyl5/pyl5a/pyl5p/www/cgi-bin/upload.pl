
#!/usr/bin/perl
#Thanks to: http://www.sitepoint.com/uploading-files-cgi-perl/

#use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use URI::Escape;
#print "Content-type: text/html\n\n";

$CGI::POST_MAX = 1024 * 5000;
my $safe_filename_characters = "a-zA-Z0-9_.-";
my $upload_dir = '/tmp';

my $query = new CGI;
my $filename = $query->param("photo");
my $lang = $query->param("lang");

if ( !$filename )
{
	print "Content-Type: text/html\n";
	print "Status: 302 Moved\n";
	print "Location: inicio.pl?lang=$lang&error=NoFile\n";
	print "\n";
	exit;
}

my ( $name, $path, $extension ) = fileparse ( $filename, '\..*' ); $filename = $name . $extension;
$filename =~ tr/ /_/; $filename =~ s/[^$safe_filename_characters]//g;

if ( $filename =~ /^([$safe_filename_characters]+)$/ )
{
	$filename = $1;
}
else
{
	die "Filename contains invalid characters";
}

my $upload_filehandle = $query->upload("photo");

open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "Error creando archivo: $upload_dir/$filename";
binmode UPLOADFILE;
while ( <$upload_filehandle> )
{
	print UPLOADFILE;
}
close UPLOADFILE;

# Ejecución del script de AConde:
print "Content-Type: text/html\n";
print "Status: 302 Moved\n";
print "Location: inicio.pl?lang=$lang&imagename=" . uri_escape("$filename") . "\n";
print "\n";

