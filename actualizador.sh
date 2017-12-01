#!/bin/bash

# Title         : actualizador.sh
# Description   : Actualiza los scripts sin alterar la configuración de inicio automático
# Author        : Veltys
# Date          : 01-12-2017
# Version       : 1.3.0
# Usage         : sudo bash actualizador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	source config.sh

	echo "Recuerde revisar ${directorio}/${dependencias[0]} por si la configuración ha cambiado"
	echo 'Es necesario que esté instalado el paquete psutil. No olvide instalarlo con "pip3 install psutil" si aún no lo está'

	for script in "${scripts[@]}"; do
		rm ${directorio}/${script}.py

		install ./Python/${script}.py ${directorio}/
	done

	for arrancable in "${arrancables[@]}"; do
		/etc/init.d/${arrancable} stop
		rm /var/lock/${arrancable}.lock &> /dev/null
		rm /etc/init.d/${arrancable}

		install ./init/${arrancable}.sh /etc/init.d/${arrancable}
		update-rc.d ${arrancable} defaults
	done

	for dependencia in "${dependencias[@]}"; do
		rm ${directorio}/${dependencia}
		install -m 0644 ./Python/${dependencia} ${directorio}/
	done

	for dep_ejecutable in "${dep_ejecutables[@]}"; do
		rm ${directorio}/${dep_ejecutable}
		install -m 0644 ./Python/${dep_ejecutable} ${directorio}/
	done
fi
