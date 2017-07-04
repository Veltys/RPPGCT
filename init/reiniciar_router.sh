#!/bin/bash


### BEGIN INIT INFO
# Provides:          reiniciar_router.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO


# Title         : reiniciar_router
# Description   : Script de init.d para el arranque automático del sistema "reiniciar_router.py".
# Author        : Veltys
# Date          : 04-07-2017
# Version       : 1.1.0
# Usage         : /etc/init.d/reiniciar_router {start|stop|restart|status}
# Notes         :


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'

	exit -1
else
	nombre=reiniciar_router
	directorio='/opt/RPPGCT'

	case "$1" in

		start)
			if [ -f /var/lock/${nombre}.lock ]; then
				echo "${nombre}.py ya está en ejecucuón"
			else
				echo "Iniciando ${nombre}.py"
				${directorio}/${nombre}.py &
			fi
			;;

		stop)
			if [ -f /var/lock/${nombre}.lock ]; then
				echo "Deteniendo ${nombre}.py"
				pkill -f ${directorio}/${nombre}.py
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
fi
