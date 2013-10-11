#!/usr/local/cpanel/3rdparty/bin/perl
# APF GUI
# v0.1
# URL: www.admingeekz.com
# Contact: sales@admingeekz.com
#
# 
# Copyright (c) 2013, AdminGeekZ Ltd 
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2, as 
# published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

use lib '/usr/local/cpanel/', '/usr/local/cpanel/whostmgr/docroot/cgi/admingeekz/apf-gui';
use strict;
use Whostmgr::ACLS  ();
use Cpanel::Logger  ();
use Cpanel::Encoder ();
use Cpanel::Form    ();
use SafeFile;
require "admingeekz.pm";

my @allowedfiles = ("/etc/apf/conf.apf", "/etc/apf/allow_hosts.rules", "/etc/apf/deny_hosts.rules");
my @search;
my %FORM = Cpanel::Form::parseform();
my $logger = Cpanel::Logger->new();

Whostmgr::ACLS::init_acls();
if (!Whostmgr::ACLS::hasroot()) {
	print "Content-type: text/html\r\n\r\n";
	print "Access Denied.";
        $logger->info("Unauthorized access to APF-GUI by $ENV{REMOTE_ADDR}");
	exit;
}

print "Content-type: text/html\r\n\r\n";

print <<EOF;
<html>
<head>
<style>
body {
	background:#E9F6F7;
	font-size:90%;
	color:#204C69;
	margin:20px auto;
	text-align:center;
	font-family:"Myriad Pro", Myriad, Helvetica, Arial, sans-serif;
	line-height:1.4em;
}
header {
	display:block;
	position:relative;
	text-align:center;
	padding:10px 20px 20px;
	margin:10px;
	border:1px solid #e7e2d7;
	border-radius:8px;
	-webkit-border-radius:.8em;
	-moz-border-radius:.8em;
	font-family:Helvetica, Arial, sans-serif;
	font-size:2.0em;
	letter-spacing:-0.06em;
	font-weight:normal;
	text-shadow: 0 1px 0 #403232;
}
textarea {
	border: 2px solid #e7e2d7;
        border-radius:8px;
        -webkit-border-radius:.8em;
        -moz-border-radius:.8em;
	width: 60%;
}
a:link {color:#204C69;}
a:visited {color:#204C69;}
a:hover {color:#0066FF; }
a:active {color:#204C69;}
</style>
<title>APF Firewall WHM Interface by AdminGeekZ.com</title>
</head>
<body>
<header>
<div>
APF Firewall Interface for WHM
</div>
</header>
<div>
EOF

exit_error("Unable to find working APF install") if !check_file("/etc/apf/apf","y");

foreach(@allowedfiles) {
	exit_error("Unable to find $_ or the file is not owned by root") if !check_file($_);
}

#Sanity check
if ($FORM{'filename'}) {
	if ( @search = grep { $_ eq $FORM{'filename'} } @allowedfiles ) {
	#find a better way to do this
	}
	else {
	$logger->info("$ENV{REMOTE_ADDR} attempted to modify an unauthorized file. $FORM{'filename'}");
	exit_error("Attempting to modify an unauthorized file");
	}
}

if ($FORM{'action'} eq "saveconfig") {
	print "Saving changes......";
	exit_error("Unable to save config file") if !savefile($FORM{'filename'},$FORM{'config'});
	restart_daemon("apf");
     	print displayfile($FORM{'filename'});
	print "Changes saved.....";
        displayfooter();

}
elsif ($FORM{'action'} eq "displayconfig") {
	print displayfile($FORM{'filename'});
	print "<p><strong>The firewall will be automatically reloaded once you click \"Save Changes\".  Ensure your changes are correct otherwise you may end up with an inaccessible system.</strong></p>";
	displayfooter();
}
else {
	print "<a href='apf-gui.cgi?action=displayconfig&filename=/etc/apf/allow_hosts.rules'>View allowed hosts</a><br />
<a href='apf-gui.cgi?action=displayconfig&filename=/etc/apf/deny_hosts.rules'>View blocked hosts</a><br />
<a href='apf-gui.cgi?action=displayconfig&filename=/etc/apf/conf.apf'>View APF config</a>";
}

sub displayfooter {
	print "<a href=\"apf-gui.cgi\">Return to menu</a>";
}

print <<EOF;
</div>
</body>
</html>
EOF
