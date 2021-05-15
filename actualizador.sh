#!/bin/bash

# Title         : actualizador.sh
# Description   : Actualiza los scripts y los configura para iniciarse automáticamente
# Author        : Veltys
# Date          : 2021-04-30
# Version       : 2.0.0
# Usage         : sudo bash actualizador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	source config.sh

	rm -r $directorio

	source instalador.sh
fi
