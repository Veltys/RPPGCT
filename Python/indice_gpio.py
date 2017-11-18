#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : indice_gpio.py
# Description   : Sistema indizador de puertos GPIO
# Author        : Veltys
# Date          : 10-08-2017
# Version       : 1.0.3
# Usage         : python3 indice_gpio.py
# Notes         : Sistema que lee las distintas configuraciones y muestra cuáles puertos están ocupados y cuáles no


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
    import config                                                                 # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

import inspect                                                                  # Metaprogramación
import os                                                                       # Funcionalidades varias del sistema operativo


def main(argv = sys.argv):
    clases = inspect.getmembers(sys.modules['config'], inspect.isclass)

    gpios_bcm_normales = [4, 13, 16, 17, 22, 23, 24, 25, 27]
    gpios_bcm_normales_libres = gpios_bcm_normales[:]
    gpios_bcm_extendidos = [5, 6, 12, 19, 20, 21, 26]
    gpios_bcm_extendidos_libres = gpios_bcm_extendidos[:] 
    gpios_bcm_especiales = [2, 3, 7, 8, 9, 10, 11, 14, 15, 18]
    gpios_bcm_especiales_libres = gpios_bcm_especiales[:]
    gpios = gpios_bcm_normales + gpios_bcm_extendidos + gpios_bcm_especiales

    for nombre, clase in clases:
        if hasattr(clase, 'GPIOS'):
            for gpio in clase.GPIOS:
                if gpio[0] in gpios_bcm_normales_libres:
                    gpios_bcm_normales_libres.remove(gpio[0])

                elif gpio[0] in gpios_bcm_extendidos_libres:
                    gpios_bcm_extendidos_libres.remove(gpio[0])

                elif gpio[0] in gpios_bcm_especiales_libres:
                    gpios_bcm_especiales_libres.remove(gpio[0])

    gpios_libres = gpios_bcm_normales_libres + gpios_bcm_extendidos_libres + gpios_bcm_especiales_libres

    print('Quedan: ', len(gpios_libres), '/', len(gpios), ' libres', sep = '')
    print('De los cuales:', os.linesep,
          len(gpios_bcm_normales_libres),   '/', len(gpios_bcm_normales),   ' normales', os.linesep,
          len(gpios_bcm_extendidos_libres), '/', len(gpios_bcm_extendidos), ' extendidos', os.linesep,
          len(gpios_bcm_especiales_libres), '/', len(gpios_bcm_especiales), ' especiales', os.linesep,
          sep = '',
         )
    print('Los puertos GPIO libres son:', sorted(gpios_libres), sep = ' ')
    print('De los cuales:', os.linesep,
          'Normales: ', sorted(gpios_bcm_normales_libres), os.linesep,
          'Extendidos: ', sorted(gpios_bcm_extendidos_libres), os.linesep,
          'Especiales: ', sorted(gpios_bcm_especiales_libres), os.linesep,
          sep = '',
         )


if __name__ == '__main__':
    main(sys.argv)
