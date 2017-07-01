#!/bin/bash

# Title         : actualizador.sh
# Description   : Actualiza los scripts sin alterar la configuración de inicio automático
# Author        : Veltys
# Date          : 01-07-2017
# Version       : 1.0.0
# Usage         : sudo bash actualizador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
  echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
  /etc/init.d/temperaturas stop
  rm /usr/local/bin/pid.py
  rm /usr/local/bin/temperaturas.py
  rm /etc/init.d/temperaturas
  install ./Python/pid.py /usr/local/bin/
  install ./Python/temperaturas.py /usr/local/bin/
  install ./init/temperaturas.sh /etc/init.d/temperaturas


  /etc/init.d/cpu stop
  rm /usr/local/bin/cpu.py
  rm /etc/init.d/cpu
  install ./Python/cpu.py /usr/local/bin/
  install ./init/cpu.sh /etc/init.d/cpu


  /etc/init.d/reiniciar_router stop
  rm /usr/local/bin/internet.py
  rm /usr/local/bin/reiniciar_router.py
  rm /etc/init.d/reiniciar_router
  install ./Python/internet.py /usr/local/bin/
  install ./Python/reiniciar_router.py /usr/local/bin/
  install ./init/reiniciar_router.sh /etc/init.d/reiniciar_router

fi
