#!/bin/bash

cd ~
apt-get install git
git clone git://github.com/mininet/mininet > /dev/null
if [ -d mininet ]; then
	cd mininet
	version=`git tag | tail -n -1`
	echo "voici les différentes versions de mininet disponibles :"
	git tag 
	dispo=`git tag`
	echo -n "intaller la dernière version ? (n/y): "
	read rep
	if [ "$rep" = "y" ]; then
		echo $version
		git checkout -b $version
	else
		trouve="mauvais"
		while [ "$trouve" = "mauvais" ] 
		do
			echo -n "Entrez la version à installer (q:quitter,d:dernière version): "
			read autre
			for i in `echo $dispo | tr " " " "`; do
				if [ "$autre" = $i ]; then
					trouve="bon"
				fi
	 		done
			if [ "$trouve" = "bon" ] ; then	
				git checkout -b $autre
			elif [ "$autre" = "d" ];then
 				git checkout -b $version
				trouve="bon"
			elif [ "$autre" = "q" ];then
				echo "vous quittez l'installation sans avoir choisi la version de mininet a installer"
				#echo "vous pouvez plus tard saisir la commande \" git checkout -b <version_a_installer>\"
				exit 1
			else
				echo "branche inexistente"
			fi
		done
	fi
	cd ..
	mininet/util/install.sh -a 
	mn --test pingall
fi