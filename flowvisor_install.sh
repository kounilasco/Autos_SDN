#!/bin/bash
cd ~
wget http://updates.onlab.us/GPG-KEY-ONLAB
apt-key add GPG-KEY-ONLAB
add-apt-repository "deb http://updates.onlab.us/debian stable/"
apt-get update && sudo apt-get install flowvisor
sudo -u flowvisor fvconfig generate /etc/flowvisor/config.json
/etc/init.d/flowvisor start
fvctl -f /dev/null set-config --enable-topo-ctrl
/etc/init.d/flowvisor restart
echo " profitez bien de  flowvisor. Version du logiciel : `fvctl -v` " 
echo "vous pouvez saisir la commande \"fvctl -n get-config\" pour voir la configuration "
