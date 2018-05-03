#!/bin/bash

# Title         : config.sh
# Description   : Almacena la configuración necesaria para el resto de scripts de bash
# Author        : Veltys
# Date          : 11-03-2018
# Version       : 1.4.0
# Usage         : source config.sh
# Notes         : 


directorio='/opt/RPPGCT'

scripts[0]='cpu'
scripts[1]='dht11'
scripts[2]='domotica_cliente'
scripts[3]='domotica_servidor'
scripts[4]='reiniciar_router'
scripts[5]='temperatura'

# arrancables[]='cpu'
# arrancables[]='domotica_servidor'
# arrancables[]='reiniciar_router'
# arrancables[]='temperatura'

dependencias[0]='config.py'
dependencias[1]='comun.py'
dependencias[2]='pid.py'

dep_ejecutables[0]='internet.py'
dep_ejecutables[1]='indice_gpio.py'
