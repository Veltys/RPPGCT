#!/bin/sh


### BEGIN INIT INFO
# Provides:          cpu.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO


# Title         : cpu
# Description   : Script de init.d para el arranque automático del sistema "cpu.py".
# Author        : Veltys
# Date          : 01-07-2017
# Version       : 1.0.2
# Usage         : /etc/init.d/cpu {start|stop|restart|status}
# Notes         : 


nombre=cpu


case "$1" in

  start)
    if [ -f /var/lock/${nombre}.lock ]; then
      echo "${nombre}.py ya está en ejecucuón"
    else
      echo "Iniciando ${nombre}.py"
      /usr/local/bin/${nombre}.py &
    fi
    ;;

  stop)
    if [ -f /var/lock/${nombre}.lock ]; then
      echo "Deteniendo ${nombre}.py"
      pkill -f /usr/local/bin/${nombre}.py
    else
      echo "${nombre}.py no está en ejecucuón"
    fi
    ;;

  restart)
    /etc/init.d/${nombre} stop && /etc/init.d/${nombre} start
    ;;

  status)
    if [ -f /var/lock/${nombre}.lock ]; then
      echo "${nombre}.py está en ejecución"
    else
      echo "${nombre}.py no está en ejecución"
    fi
    ;;

  *)
    echo "Uso: /etc/init.d/${nombre} {start|stop|restart|status}"
    exit 1
    ;;

esac

exit 0
