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
