APF GUI
=============

##Overview

APF GUI is a free, open source WHM plugin cPanel that allows you to manage your APF firewall from within WHM.  It presently has support for,

- Managing the APF configuration.
- Managing the allowed IP file.
- Managing the denied IP file.

### Requirements
 - cPanel/WHM
 - Perl 5.8 or better
 - APF (Advanced Policy Firewall) from R-fx networks (http://www.rfxn.com/downloads/apf-current.tar.gz)
 - Red Hat/CentOS

### Security

We have developed this plugin with security in mind,  only authorized (root) users may use the interface,  only permitted files are allowed to be viewed/modified,  owners of files are checked and error checking in is place.   The cPanel logging library has been used and any malicious attempts are reported at /usr/local/cpanel/logs/error_log

### Installation

To install the latest version of apf-gui from SSH run

<pre><code>
wget -O apf-gui.tar.gz https://www.admingeekz.com/files/apf-gui.tar.gz
tar -zxf apf-gui.tar.gz
cd apf-gui
/bin/bash install.sh
</code></pre>

You should then be able to see "APF GUI" in WHM on the left menu under "Plugins".

### Support,  bug fixes and contributions

You may report issues and contribute to the project at on github at https://github.com/admingeekz/apf-gui 

#### Todo
 - Add debian/ubuntu support
 - Make GUI more friendly
