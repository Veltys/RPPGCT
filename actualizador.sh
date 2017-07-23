#!/bin/bash

# Title         : actualizador.sh
# Description   : Actualiza los scripts sin alterar la configuración de inicio automático
# Author        : Veltys
# Date          : 10-07-2017
# Version       : 1.2.1
# Usage         : sudo bash actualizador.sh
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

	echo 'Recuerde revisar ./Python/config.py.sample por si la configuración ha cambiado'
	echo 'Es necesario que esté instalado el paquete psutil. No olvide instalarlo con "pip3 install psutil" si aún no está instalado'

	for script in "${scripts[@]}"; do
		/etc/init.d/${script} stop
		rm /var/lock/${script}.lock
		rm /etc/init.d/${script}
		rm ${directorio}/${script}.py

		install ./Python/${script}.py ${directorio}/
        install ./init/${script}.sh /etc/init.d/${script}
	done

	for dependencia in "${dependencias[@]}"; do
		rm ${directorio}/${dependencia}
		install ./Python/${dependencia} ${directorio}/
	done
fi
