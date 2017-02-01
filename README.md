<b> Les tests on été concluant sous ubuntu 14.04 LTS </b> 
<p> 
Bienvenu dans le programme d'installation de l'application web Autos.
</p>
<p>
l'application se base sur une topologie réseaux fourni servant de base de test. vous pouvez créer votre propre topologie.<br/><br/>
Pour l'installation de l'application et de son environnement complet:
<ol>
<li> Deziper ou cloner le projet dans votre répertoire personnel</li>
<li> lancer le programme install.sh dans le dossier Autos en root (sudo bash install.sh) et suivez les instructions.</li>
	<ul>le programme installera:
		<li>git si vous ne l'avez pas déjà installé</li>
		<li>mininet et toutes ses dépendances</li>
		<li>flowvisor et toutes ses dépendances</li>
		<li>Autos et ses dépendances (Autos s'éxécute dans un environnement virtuel. ses dépendances n'affectent donc en 			aucun cas le système)</li>
	</ul>
<li> une fois l'installation terminée un nouveau terminal va s'ouvrir : c'est le server web qui a été lancé </li>
<li>ouvrez un navigateur et allez à l'adresse 127.0.0.1:5000 </li>
<li>vous pouvez dès à présent créer des slices et des flowspaces (les flowspaces utilisant des slices, ces derniers doivent au préalables être créés)</li>
<li> créer le fichier de routage des packets pour chaque slice creé et placez les dans $HOME/pox/ext</li>
<li>lancez la topologie et le controleur</li>
<li>faites les tests </li>
</ol>
</p>

