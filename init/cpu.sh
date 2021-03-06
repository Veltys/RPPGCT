#!/bin/bash


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
# Date          : 2019-12-19
# Version       : 2.0.5
# Usage         : /etc/init.d/cpu {start|stop|restart|status}
# Notes         : 


nombre=cpu
directorio='/opt/RPPGCT'
fallo='Este comando debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'

# requisitos[]=''


case "$1" in
	start)
		if [ "$UID" -ne '0' ]; then
			echo $fallo

			exit -1
		else
			if [ -f /var/lock/${nombre}.lock ]; then
				echo "${nombre}.py ya está en ejecución"
			else
				if [ ! -z $requisitos ]; then
					echo "Iniciando requisitos de ${nombre}.py"

					for requisito in "${requisitos[@]}"; do
						/etc/init.d/${requisito} start
					done
				fi

				echo "Iniciando ${nombre}.py"

				${directorio}/${nombre}.py &
			fi
		fi
	;;

	stop)
		if [ "$UID" -ne '0' ]; then
			echo $fallo

			exit -1
		else
			if [ -f /var/lock/${nombre}.lock ]; then
				echo "Deteniendo ${nombre}.py"

				pkill -f ${directorio}/${nombre}.py
			else
				echo "${nombre}.py no está en ejecución"
			fi
		fi
	;;

	restart)
		if [ "$UID" -ne '0' ]; then
			echo $fallo

			exit -1
		else
			/etc/init.d/${nombre} stop && sleep 20 && /etc/init.d/${nombre} start
		fi
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
