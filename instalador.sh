#!/bin/bash

install ./Python/pid.py /usr/local/bin/
install ./Python/temperaturas.py /usr/local/bin/
install ./init/temperaturas.sh /etc/init.d/temperaturas
update-rc.d temperaturas defaults

install ./Python/cpu.py /usr/local/bin/
install ./init/cpu.sh /etc/init.d/cpu
update-rc.d cpu defaults

install ./Python/internet.py /usr/local/bin/
install ./Python/reiniciar_router.py /usr/local/bin/
install ./init/reiniciar_router.sh /etc/init.d/reiniciar_router
update-rc.d reiniciar_router defaults

