#!/bin/sh
acpi -b | awk -F'[,:%]' '{print $2, $3}' | {
  read -r status capacity

  if [ "$status" = Discharging -a "$capacity" -lt 5 ]; then
    logger "Critical battery threshhold"
	# make sure you have permission to use this without password
	# edit /etc/suoders
	# e.g. add for the sudo group NOPASSWD for the command:
	# %sudo   ALL=(ALL) NOPASSWD: /usr/bin/systemctl hibernate
    sudo /usr/bin/systemctl hibernate
  fi
}

