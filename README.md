# Autos_SDN
The project consist  to create a web interface to automate slicing of a mininet topology
bienvenu dans le programme d'installation de l'application web Autos.
si vous lisez ce fichier c'est que vous avez déjà dezipé l'archive :)
l'application se base sur une topologie réseaux fourni servant de base de test. vous pouvez creer votre propre topologie.
Pour l'installation de l'application et de son environnement complet:
1- mettez le dossier Autos dézipé dans votre répertoire personnel 
2- lancer le programme install.sh dans le dossier Autos en root (sudo bash install.sh) et suivez les instructions.
	le programme installera:
		- git si vous ne l'avez pas déjà installé
		- mininet et toutes ses dépendances
		- flowvisor et toutes ses dépendances
		- Autos et ses dépendances (Autos s'éxécute dans un environnement virtuel. ses dépendances n'affectent donc en aucun cas le système)
3- une fois l'installation terminée un nouveau terminal va s'ouvrir : c'est le server web qui a été lancé 
4- ouvrez un navigateur et allez à l'adresse 127.0.0.1:5000 
5- vous pouvez dès à présent créer des slices et des flowspaces (les flowspaces utilisant des slices, ces derniers doivent au préalables être créés)
6- créer le fichier de routage des packets pour chaque slice creés et placez les dans $HOME/pox/ext
7- lancez la topologie et le controleur
8- faites les tests 
