#!/bin/bash
addonname="apf-gui"
addonpath="/usr/local/cpanel/whostmgr/docroot/cgi/admingeekz/apf-gui"

if [ ! -e "/usr/local/cpanel/cpsrvd" ]; then
  echo "This only works for cPanel servers"
  exit 2
fi

if [ ! -e "/usr/local/cpanel/bin/register_appconfig" ]; then
  echo "We only support newer versions of cPanel with appconfig"
  exit 2
fi

if [ ! -e "/usr/local/cpanel/3rdparty/bin/perl" ]; then
  echo "Unable to find /usr/local/cpanel/3rdparty/bin/perl"
  exit 2
fi

#Cleanup/Upgrade old installs
if [ -e "${addonpath}/${addonname}.cgi" ]; then
echo "Upgrading old installation"
/usr/local/cpanel/bin/unregister_appconfig ${addonname} &> /dev/null
rm -rf ${addonpath}
fi

mkdir -p ${addonpath}
chmod 700 ${addonpath}
files="${addonname}.cgi ${addonname}.conf admingeekz.pm"
for file in ${files}; do
  cp -fa ${file} ${addonpath}/${file} 
  chmod 600 ${addonpath}/${file}
done
#This is the only one that will need execute permissions
chmod 700 ${addonpath}/${addonname}.cgi

if [ ! -e "${addonpath}/${addonname}.cgi" ]; then
  echo "Critical error installing addon,  please report"
  exit 2
fi

/usr/local/cpanel/bin/register_appconfig ${addonpath}/${addonname}.conf

echo "AdminGeekZ ${addonname} has been installed"
exit 0

