#!/bin/bash

# Title         : instalador.sh
# Description   : Instala los scripts y los configura para iniciarse automáticamente
# Author        : Veltys
# Date          : 10-07-2017
# Version       : 1.2.0
# Usage         : sudo bash instalador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	directorio='/opt/RPPGCT'
	scripts[0]='cpu'
	scripts[1]='domotica'
	scripts[2]='reiniciar_router'
	scripts[3]='temperatura'
	dependencias[0]='config.py.sample'
	dependencias[1]='comun.py'
	dependencias[2]='pid.py'
	dependencias[3]='internet.py'
	dependencias[4]='indice_gpio.py'

	mkdir $directorio

	echo "Recuerde editar ${directorio}/config.py.sample y guardarlo como config.py con los valores adecuados"

	echo 'Es necesario instalar el paquete psutil'
	read -p "¿Desea instalarlo de forma automática? (S/n): " eleccion
	case "$eleccion" in
		n|N )
			echo "Omitiendo instalación..."
			;;
		* )
			echo "Instalando..."
			pip3 install psutil
			;;
	esac

	for dependencia in "${dependencias[@]}"; do
		install ./Python/${dependencia} ${directorio}/
	done

	for script in "${scripts[@]}"; do
		install ./Python/${script}.py ${directorio}/
		install ./init/${script}.sh /etc/init.d/${script}
		update-rc.d ${script} defaults
	done
fi
