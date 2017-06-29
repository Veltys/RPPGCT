#!/bin/bash

# Title         : desinstalador.sh
# Description   : Desinstala los scripts y los elimina la configuración para iniciarse automáticamente
# Author        : Veltys
# Date          : 29-06-2017
# Version       : 1.0.0
# Usage         : sudo bash desinstalador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento

rm /usr/local/bin/pid.py
rm /usr/local/bin/temperaturas.py
rm /etc/init.d/temperaturas
update-rc.d -f temperaturas remove

rm /usr/local/bin/cpu.py
rm /etc/init.d/cpu
update-rc.d -f cpu remove

rm /usr/local/bin/internet.py
rm /usr/local/bin/reiniciar_router.py
rm /etc/init.d/reiniciar_router
update-rc.d -f reiniciar_router remove




