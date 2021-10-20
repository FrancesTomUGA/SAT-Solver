Projet solveur minisat : jeu Light-Up

### A FAIRE AVANT DE COMMENCER ###
	- installer le package python tkinter : python-tk (normalement préinstallé avec la version 3 de python
	(Linux) : sudo apt-get install python-tk
		
Le programme principal main peut prendre un certain nombre d'arguments :

	- 5 : 	* nom_script (main)
			* proba (nombre de cases non libres sur le plateau)
			* nombre de lignes du plateau
			* nombre de colonnes du plateau 
			* step-by-step (1 si on veut afficher tous les plateaux testés, 0 sinon)
			
	- 4 : 	* nom_script
			* proba (nombre de cases non libres sur le plateau)
			* dimension (plateau carré)
			* step-by-step (1 si on veut afficher tous les plateaux testés, 0 sinon)
			
	- 3 : 	* nom_script
			* entier (numéro du test préétabli, de 1 à 6)
			* debugg (1 si on veut afficher la construction de la fnc pas à pas, 0 sinon)
			
Les 6 tests sont les suivants :
	1 : plateau 7x7, facile
	2 : plateau 7x7, difficile
	3 : plateau 10x10, facile
	4 : plateau 10x10, difficile
	5 : plateau 14x14, facile
	6 : plateau 14x14, difficile
