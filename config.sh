#!/bin/bash

# Title         : config.sh
# Description   : Almacena la configuración necesaria para el resto de scripts de bash
# Author        : Veltys
# Date          : 2021-04-30
# Version       : 1.5.0
# Usage         : source config.sh
# Notes         : 


directorio='/opt/RPPGCT'

paquetes[0]='psutil'
paquetes[1]='dht11'

scripts[0]='aviso_electricidad'
scripts[1]='correo_electronico'
scripts[2]='cpu'
scripts[3]='domotica_cliente'
scripts[4]='domotica_servidor'
scripts[5]='reiniciar_router'
scripts[6]='sonda_dht11'
scripts[7]='temperatura'

arrancables[0]='cpu'
arrancables[1]='domotica_servidor'
arrancables[2]='reiniciar_router'
arrancables[3]='temperatura'

dependencias[0]='config.py'
dependencias[1]='comun.py'
dependencias[2]='pid.py'

dep_ejecutables[0]='internet.py'
dep_ejecutables[1]='indice_gpio.py'
