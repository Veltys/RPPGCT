#!/bin/bash

# Title         : desinstalador.sh
# Description   : Desinstala los scripts y elimina la configuración para iniciarse automáticamente
# Author        : Veltys
# Date          : 01-07-2017
# Version       : 1.1.0
# Usage         : sudo bash desinstalador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
  echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
  directorio='/opt/RPPGCT'

  /etc/init.d/temperaturas stop
  update-rc.d -f temperaturas remove

  /etc/init.d/cpu stop
  rm /etc/init.d/cpu
  update-rc.d -f cpu remove

  /etc/init.d/reiniciar_router stop
  rm /etc/init.d/reiniciar_router
  update-rc.d -f reiniciar_router remove

  rm -r $directorio/
fi
