MAZE ESCAPE
=====================================

Descizione del Progetto:
-----------------------
Questo progetto consente ad un robot di muoversi all'interno di un labirinto sconosciuto e di scegliere la strada da intraprendere attraverso la detection di specifici apriltags usati come segnaletica.
In particolare il robot deve essere capace di distinguere la tipologia del tag e, sulla base di questo, di ruotare a destra o a sinistra dell'angolo richiesto.
Per eseguire la rotazione viene usata l'odomoteria e in particolare il valore di yaw che, aggiornandosi continuamente attraverso il metodo di callback, fornisce una stima accurata della posizione corrente del robot e permette, quindi, di regolare la velocità angolare in modo da fermare il robot quando si è raggiunta la posa richiesta.


Requisiti:
-----------------------
Per lo sviluppo del progetto sono stati utilizzati ROS Melodic e Ubuntu 18.04.4 LTS.
E' possibile trovare le istruzioni necessarie all'installazione di ROS al seguente link:
http://wiki.ros.org/melodic/Installation/Ubuntu

Una volta installato ROS, è necessario eseguire le seguenti istruzioni per la configurazione del catkin workspace:

	$ source /opt/ros/melodic/setup.bash
	$ mkdir -p ~/catkin_ws/src
	$ cd ~/catkin_ws/src
	$ catkin_init_workspace
	$ cd ~/catkin_ws/
	$ catkin_make


Nel file ~/.bashrc aggiungere la seguente linea di codice:

	source ~/catkin_ws/devel/setup.bash

ed infine eseguire catkin_make nella root del catkin workspace.

Come robot è stato scelto il turtlebot3 modello waffle, poichè già dotato della camera necessaria per la detection degli apriltags.
L'installazione dei pacchetti necessari può essere fatta eseguendo le istruzioni seguenti:

	$ cd ~/catkin_ws/src/
	$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
	$ git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
	$ cd ~/catkin_ws && catkin_make

NOTA: Se si vuole abilitare la visualizzazione del laser, è necessario andare a modificare in turtlebot3/turtlebot3_description/urdf il file turtlebot3_waffle.gazebo.xacro inserendo true come valore di default in <xacro:arg name="laser_visual"  default="false"/> e sostituendo il seguente frammento di codice in corrispondenza del sensore base_scan:

	<scan>
	    <horizontal>
	      <samples>360</samples>
	      <resolution>1</resolution>
	      <min_angle>-1.570796</min_angle>
	      <max_angle>1.570796</max_angle>
	    </horizontal>
	</scan>
	<range>
	    <min>0.20</min>
	    <max>30.0</max>
	    <resolution>0.01</resolution>
	</range>


Per il corretto funzionamento del progetto, procedere all'installazione di ros-melodic-apriltag-ros e ros-melodic-navigation con le seguenti istruzioni:

	sudo apt-get install ros-melodic-apriltag-ros
	sudo apt-get install ros-melodic-navigation

necessari per la detection degli apriltags e per la navigazione del turtlebot.

A questo punto è necessario clonare altri due repository con le seguenti istruzioni:

	$ cd ~/catkin_ws/src/
	$ git clone https://github.com/AprilRobotics/apriltag_ros.git
	$ git clone https://github.com/ros/common_msgs.git	


Installazione progetto:
-----------------------
Per installare il progetto Maze escape è sufficiente clonare il repository nella cartella src di catkin_ws.

E' inoltre necessario:
- inserire il contenuto della cartella models in .gazebo, in modo da rendere fruibili il modello del mondo e degli apriltags.
- sostituire i file settings.yaml e tags.yaml presenti in apriltag_ros/apriltag_ros/config/ con quelli presenti nella cartella config del progetto.

Per lanciarlo sarà sufficiente eseguire il comando:

	export TURTLEBOT3_MODEL=waffle
	roslaunch maze_project maze_project.launch


Soluzione:
-----------------------
PSEUDO-CODICE

	salva l'angolo acquisito dal robot

	while not rospy.is_shutdown():
	   if(non è stato acquisito il lock ed è stato chiamato il callback di odom)
	        fai muovere in avanti il robot
	        if(è stato individuato un apriltag dalla detection):
	            ferma il robot
		        if(l'apriltag ha id 1):
		        	il robot deve girare a destra
		        elif('apriltag ha id 0):
		        	il robot deve girare a sinistra
		        else:
		        	ferma il robot

	def rotate_angle(self, angle):
		trasforma l'angolo in radianti
		fai la differenza tra l'angolo che si vuole raggiungere e il valore corrente di yaw
		while(non si è raggiunto l'angolo desiderato):
			continua a ruotare il robot
		interrompi la rotazione


Autori
-----------------------
Gioia Lotito
Marco Rizzi
