#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : indice_gpio.py
# Description   : Sistema indizador de puertos GPIO
# Author        : Veltys
# Date          : 2019-12-19
# Version       : 1.0.7
# Usage         : python3 indice_gpio.py
# Notes         : Sistema que lee las distintas configuraciones y muestra cuáles puertos están ocupados y cuáles no


import errno                                                                                                # Códigos de error
import inspect                                                                                              # Metaprogramación
import sys                                                                                                  # Funcionalidades varias del sistema

try:
    import config                                                                                           # @UnusedImport Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


def main(argv):
    clases = inspect.getmembers(sys.modules['config'], inspect.isclass)                                     # Se recoge cada clase

    gpios_bcm_normales = [4, 13, 16, 17, 22, 23, 24, 25, 27]                                                # Puertos GPIO "normales"

    gpios_bcm_extendidos = [5, 6, 12, 19, 20, 21, 26]                                                       # Puertos GPIO "extendidos"

    gpios_bcm_especiales = [0, 1, 2, 3, 7, 8, 9, 10, 11, 14, 15, 18]                                        # Puertos GPIO "especiales"

    gpios = gpios_bcm_normales + gpios_bcm_extendidos + gpios_bcm_especiales                                # Los tres anteriores

    gpios_bcm_normales_libres = gpios_bcm_normales[:]                                                       # Puertos GPIO "normales" libres

    gpios_bcm_extendidos_libres = gpios_bcm_extendidos[:]                                                   # Puertos GPIO "extendidos" libres

    gpios_bcm_especiales_libres = gpios_bcm_especiales[:]                                                   # Puertos GPIO "especiales" libres


    for _, clase in clases:                                                                                 # Se recorre la lista de clases
        if hasattr(clase, 'GPIOS'):                                                                         #     Si la clase contiene el miembro GPIOS
            for gpios in clase.GPIOS:                                                                       #         Éste se recorre
                for gpio in gpios:
                    if gpio[0] in gpios_bcm_normales_libres:                                                #             Si el puerto está en esta lista
                        gpios_bcm_normales_libres.remove(gpio[0])                                           #                 Se elimina de la lista de libres
    
                    elif gpio[0] in gpios_bcm_extendidos_libres:                                            #             Si el puerto está en esta lista
                        gpios_bcm_extendidos_libres.remove(gpio[0])                                         #                 Se elimina de la lista de libres
    
                    elif gpio[0] in gpios_bcm_especiales_libres:                                            #             Si el puerto está en esta lista
                        gpios_bcm_especiales_libres.remove(gpio[0])                                         #                 Se elimina de la lista de libres

    gpios_libres = gpios_bcm_normales_libres + gpios_bcm_extendidos_libres + gpios_bcm_especiales_libres    # Cálculo de los puertos libres

    print('Quedan: ', len(gpios_libres), '/', len(gpios), ' puertos libres', sep = '')                      # Presentación de los resultados por pantalla
    print()
    print('De los cuales:')
    print(len(gpios_bcm_normales_libres),   '/', len(gpios_bcm_normales),   "\tnormales",   sep = '')
    print(len(gpios_bcm_extendidos_libres), '/', len(gpios_bcm_extendidos), "\textendidos", sep = '')
    print(len(gpios_bcm_especiales_libres), '/', len(gpios_bcm_especiales), "\tespeciales", sep = '')
    print()
    print()

    print('Los puertos GPIO libres son:', sorted(gpios_libres), sep = ' ')
    print()
    print('De los cuales:')
    print('Normales:',   ((sorted(gpios_bcm_normales_libres))   if (len(gpios_bcm_normales_libres)   > 0) else "(ninguno)"), sep = "\t")
    print('Extendidos:', ((sorted(gpios_bcm_extendidos_libres)) if (len(gpios_bcm_extendidos_libres) > 0) else "(ninguno)"), sep = "\t")
    print('Especiales:', ((sorted(gpios_bcm_especiales_libres)) if (len(gpios_bcm_especiales_libres) > 0) else "(ninguno)"), sep = "\t")


if __name__ == '__main__':
    main(sys.argv)
