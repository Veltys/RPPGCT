#!/bin/bash

# Title         : instalador.sh
# Description   : Instala los scripts y los configura para iniciarse automáticamente
# Author        : Veltys
# Date          : 2021-04-30
# Version       : 1.4.0
# Usage         : sudo bash instalador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	source config.sh

	mkdir $directorio

	echo "Recuerde editar ${directorio}/${dependencias[0]} y guardarlo como config.py con los valores adecuados"

	for paquete in "${paquetes[@]}"; do
		echo "Es necesario instalar el paquete $paquete"

		read -p "¿Desea instalarlo de forma automática? (S/n): " eleccion

		case "$eleccion" in
			n|N )
				echo "Omitiendo instalación..."
			;;
			* )
				echo "Instalando..."
				pip3 install "$paquete"
			;;
		esac
	done

	for dependencia in "${dependencias[@]}"; do
		install -m 0644 ./Python/${dependencia} ${directorio}/
	done

	for dep_ejecutable in "${dep_ejecutables[@]}"; do
		install ./Python/${dep_ejecutable} ${directorio}/
	done

	for script in "${scripts[@]}"; do
		install ./Python/${script}.py ${directorio}/
	done

	for arrancable in "${arrancables[@]}"; do
		install ./init/${arrancable}.sh /etc/init.d/${arrancable}
		update-rc.d ${arrancable} defaults
	done
fi
