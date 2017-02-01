#!/bin/bash
#echo "Pour permettre un redemarage depuis l'interface graphique de l'application il nous faut le mot de passe root"
#rep=""
#while [ "$rep" != "yes" -a "$rep" != "No" ]
#do
#	read  -p "voulez-vous entrez votre mot de passe ? (yes/No)" rep
##done
#if [ "$rep" = "No" ]; then
#	echo "vous avez choisi de ne pas utiliser la fonctionalité redemarrage ..."
#elif [ "$rep" = "yes" ]; then
#	read -s -p "Entrez le mot de passe root : " pass1;echo
#	read -s -p "Confirmer le mot de passe : " pass2;echo		
#	while [ "$pass1" != "$pass2" ]; do
#		echo "les deux mots de passe entrés diffèrent"	
#		read -s -p "Entrez le mot de passe root : " pass1;echo
#		read -s -p "Confirmer le mot de passe : " pass2;echo				
#	done
#	echo $pass2 > $HOME/Autos/Autos/.mdp.txt
#	chmod a=r $HOME/Autos/Autos/.mdp.txt		
#fi

chmod u+x mininet_install.sh
chmod u+x flowvisor_install.sh
chmod u+x autos_env_install.sh
#chmod u+x create_slice_and_flowspaces.sh
#installation de mininet
./mininet_install.sh
#installation de flowvisor
./flowvisor_install.sh ## l'installation automatique pose certains problèmes parfois. il est donc préférable de lancer
# manuellement le script : sudo bash flowvisor_install.sh
#deploiement de la topologie de base
cp neteam.py $HOME/mininet/custom
#deploiment des regles de routage pour le slice de test "dsi"
cp dsi_controller.py $HOME/pox/ext
#deploiement de l'environnement python pour l'application web
tar -xzvf Autos.tar.gz -C $HOME/Autos
./autos_env_install.sh
#service flowvisor restart
#cd ~
#gnome-terminal -e "mn --custom $HOME/mininet/custom/neteam.py --topo=neteam --controller=remote --link=tc --mac --arp" &
#gnome-terminal -e "$HOME/pox/pox.py openflow.of_01 --port=10001 dsi_controller" &
