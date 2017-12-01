#!/bin/bash

# Title         : actualizador.sh
# Description   : Actualiza los scripts sin alterar la configuración de inicio automático
# Author        : Veltys
# Date          : 30-11-2017
# Version       : 1.2.5
# Usage         : sudo bash actualizador.sh
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
		install ./Python/${dependencia} ${directorio}/
	done
fi
