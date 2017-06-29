#!/bin/sh

### BEGIN INIT INFO
# Provides:          temperaturas.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

nombre=temperaturas

case "$1" in
  start)
    echo "Iniciando ${nombre}.py"
    /usr/local/bin/${nombre}.py &
    ;;
  stop)
    echo "Deteniendo ${nombre}.py"
    pkill -f /usr/local/bin/${nombre}.py
    ;;
  restart)
    /etc/init.d/${nombre}.sh stop && /etc/init.d/${nombre}.sh start
    ;;
  status)
    if [ -f /var/lock/${nombre}.lock ]; then
      echo "Estado de ${nombre}.py: en ejecución"
    else
      echo "Estado de ${nombre}.py: detenido"
    fi
    ;;
  *)
    echo "Uso: /etc/init.d/${nombre}.sh {start|stop|restart|status}"
    exit 1
    ;;
esac

exit 0
