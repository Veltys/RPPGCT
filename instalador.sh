#!/bin/bash

# Title		: instalador.sh
# Description	: Instala los scripts y los configura para iniciarse automáticamente
# Author	: Veltys
# Date		: 29-06-2017
# Version	: 1.0.1
# Usage		: sudo bash instalador.sh
# Notes		: Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
  echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
  install ./Python/pid.py /usr/local/bin/
  install ./Python/temperaturas.py /usr/local/bin/
  install ./init/temperaturas.sh /etc/init.d/temperaturas
  update-rc.d temperaturas defaults

  install ./Python/cpu.py /usr/local/bin/
  install ./init/cpu.sh /etc/init.d/cpu
  update-rc.d cpu defaults

  install ./Python/internet.py /usr/local/bin/
  install ./Python/reiniciar_router.py /usr/local/bin/
  install ./init/reiniciar_router.sh /etc/init.d/reiniciar_router
  update-rc.d reiniciar_router defaults
fi

