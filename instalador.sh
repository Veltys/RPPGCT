#!/bin/bash

# Title         : instalador.sh
# Description   : Instala los scripts y los configura para iniciarse automáticamente
# Author        : Veltys
# Date          : 10-08-2017
# Version       : 1.2.3
# Usage         : sudo bash instalador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	directorio='/opt/RPPGCT'

	scripts[0]='cpu'
	scripts[1]='domotica_cliente'
	scripts[2]='domotica_servidor'
	scripts[3]='reiniciar_router'
	scripts[4]='temperatura'

	arrancables[0]='cpu'
	arrancables[1]='domotica_servidor'
	arrancables[2]='reiniciar_router'
	arrancables[3]='temperatura'

	dependencias[0]='config_sample.py'
	dependencias[1]='comun.py'
	dependencias[2]='pid.py'
	dependencias[3]='internet.py'
	dependencias[4]='indice_gpio.py'

	mkdir $directorio

	echo "Recuerde editar ${directorio}/${dependencias[0]} y guardarlo como config.py con los valores adecuados"

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
	done

	for arrancable in "${arrancables[@]}"; do
		install ./init/${arrancable}.sh /etc/init.d/${arrancable}
		update-rc.d ${arrancable} defaults
	done
fi
