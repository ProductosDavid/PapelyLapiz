
#!/usr/bin/perl

use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use Data::Dumper;
use File::Copy;

require 'template.pl';
require 'functions.pl';

$| = 1;

my $query = new CGI;
my $imagename = $query->param("imagename");
my $imagefolder = $query->param("imagefolder");

ExecuteImageProcessing($imagename, $imagefolder);

GetImageProcessingLog($imagefolder);

BeginSection("1.1. Recognized objects", "sect_11_div", "fullwidth_div");

print "<div id='objetosreconocidos'>";

PrintActors($imagefolder);

print "</div>";

EndSection();

BeginSection("1.1. Recognized text", "sect_11_div", "fullwidth_div");

print "<div id='textoreconocido'>";

PrintText($imagefolder);

print "</div>";

EndSection();

BeginSection("1.2. Unrecognized objects", "sect_12_div", "fullwidth_div");

print "<div id='objetosnoreconocidos'>";

PrintNoise($imagefolder);

print "</div>";

EndSection();


