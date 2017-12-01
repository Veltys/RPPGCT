#!/bin/bash

# Title         : config.sh
# Description   : Almacena la configuración necesaria para el resto de scripts de bash
# Author        : Veltys
# Date          : 01-12-2017
# Version       : 1.3.0
# Usage         : source config.sh
# Notes         : 


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

dep_ejecutables[0]='internet.py'
dep_ejecutables[1]='indice_gpio.py'
