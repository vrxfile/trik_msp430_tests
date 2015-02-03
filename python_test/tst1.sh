#!/bin/sh

# Test1 for motors

#Power on 12 volts power
echo 1 > /sys/class/gpio/gpio62/value

#Configure com port for raw data format
stty -F /dev/ttyACM0 -echo -onlcr

#cat /dev/ttyACM0 &

#Set alternative output device
#out_device="/dev/tty"
#out_device="000.txt"
out_device="/dev/ttyACM0"


#Set device to read responses
resp_device="000.data"

#Test packet
printf "Privet!\n" > $out_device; 
printf "Privet!\n";

#Set motor period
set_period_for_motor ()
{
	local crc
	local func=3
	local regaddr=2
	#Start condition
	printf ":" >> $out_device; 
	printf ":";
	#Motor number
	if [ $devaddr -lt 16 ]; then 
		printf "0%X" $devaddr >> $out_device; 
		printf "0%X" $devaddr;
	else 
		printf "%X" $devaddr >> $out_device; 
		printf "%X" $devaddr;
	fi
	#Function number
	if [ $func -lt 16 ]; then 
		printf "0%X" $func >> $out_device; 
		printf "0%X" $func;
	else 
		printf "%X" $func >> $out_device; 
		printf "%X" $func;
	fi
	#Register number
	if [ $regaddr -lt 16 ]; then 
		printf "0%X" $regaddr >> $out_device; 
		printf "0%X" $regaddr;
	else 
		printf "%X" $regaddr >> $out_device; 
		printf "%X" $regaddr;
	fi
	#Register value
	if [ $period -lt 16 ]; then 
		printf "000%X" $period >> $out_device; 
		printf "000%X" $period;
	elif [ $period -lt 256 ]; then 
		printf "00%X" $period >> $out_device; 
		printf "00%X" $period;
	elif [ $period -lt 4096 ]; then 
		printf "0%X" $period >> $out_device; 
		printf "0%X" $period;
	else 
		printf "%X" $period >> $out_device; 
		printf "%X" $period;
	fi
	#Checksum
	crc=$((((0-($devaddr+$func+$regaddr+(($period>>8)&255)+($period&255)))&255)))
	if [ $crc -lt 16 ]; then 
		printf "0%X\n" $crc >> $out_device; 
		printf "0%X\n" $crc;
	else 
		printf "%X\n" $crc >> $out_device; 
		printf "%X\n" $crc;
	fi
	return
}

#Set motor power by duty
set_duty_for_motor ()
{
	local crc
	local func=3
	local regaddr=1
	#Start condition
	printf ":" >> $out_device; 
	printf ":";
	#Motor number
	if [ $devaddr -lt 16 ]; then 
		printf "0%X" $devaddr >> $out_device; 
		printf "0%X" $devaddr;
	else 
		printf "%X" $devaddr >> $out_device; 
		printf "%X" $devaddr;
	fi
	#Function number
	if [ $func -lt 16 ]; then 
		printf "0%X" $func >> $out_device; 
		printf "0%X" $func;
	else 
		printf "%X" $func >> $out_device; 
		printf "%X" $func;
	fi
	#Register number
	if [ $regaddr -lt 16 ]; then 
		printf "0%X" $regaddr >> $out_device; 
		printf "0%X" $regaddr;
	else 
		printf "%X" $regaddr >> $out_device; 
		printf "%X" $regaddr;
	fi
	#Register value
	if [ $duty -lt 16 ]; then 
		printf "000%X" $duty >> $out_device; 
		printf "000%X" $duty;
	elif [ $duty -lt 256 ]; then 
		printf "00%X" $duty >> $out_device; 
		printf "00%X" $duty;
	elif [ $duty -lt 4096 ]; then 
		printf "0%X" $duty >> $out_device; 
		printf "0%X" $duty;
	else 
		printf "%X" $duty >> $out_device; 
		printf "%X" $duty;
	fi
	#Checksum
	crc=$((((0-($devaddr+$func+$regaddr+(($duty>>8)&255)+($duty&255)))&255)))
	if [ $crc -lt 16 ]; then 
		printf "0%X\n" $crc >> $out_device; 
		printf "0%X\n" $crc;
	else 
		printf "%X\n" $crc >> $out_device; 
		printf "%X\n" $crc;
	fi
	return
}

#Stop motor
stop_motor ()
{
	local crc
	local func=3
	local regaddr=0
	local ctrl_reg=32768
	#Start condition
	printf ":" >> $out_device; 
	printf ":";
	#Motor number
	if [ $devaddr -lt 16 ]; then 
		printf "0%X" $devaddr >> $out_device; 
		printf "0%X" $devaddr;
	else 
		printf "%X" $devaddr >> $out_device; 
		printf "%X" $devaddr;
	fi
	#Function number
	if [ $func -lt 16 ]; then 
		printf "0%X" $func >> $out_device; 
		printf "0%X" $func;
	else 
		printf "%X" $func >> $out_device; 
		printf "%X" $func;
	fi
	#Register number
	if [ $regaddr -lt 16 ]; then 
		printf "0%X" $regaddr >> $out_device; 
		printf "0%X" $regaddr;
	else 
		printf "%X" $regaddr >> $out_device; 
		printf "%X" $regaddr;
	fi
	#Register value
	if [ $ctrl_reg -lt 16 ]; then 
		printf "000%X" $ctrl_reg >> $out_device; 
		printf "000%X" $ctrl_reg;
	elif [ $ctrl_reg -lt 256 ]; then 
		printf "00%X" $ctrl_reg >> $out_device; 
		printf "00%X" $ctrl_reg;
	elif [ $ctrl_reg -lt 4096 ]; then 
		printf "0%X" $ctrl_reg >> $out_device; 
		printf "0%X" $ctrl_reg;
	else 
		printf "%X" $ctrl_reg >> $out_device; 
		printf "%X" $ctrl_reg;
	fi
	#Checksum
	crc=$((((0-($devaddr+$func+$regaddr+(($ctrl_reg>>8)&255)+($ctrl_reg&255)))&255)))
	if [ $crc -lt 16 ]; then 
		printf "0%X\n" $crc >> $out_device; 
		printf "0%X\n" $crc;
	else 
		printf "%X\n" $crc >> $out_device; 
		printf "%X\n" $crc;
	fi
	return
}

#Stop motor with braking
brake_motor ()
{
	local crc
	local func=3
	local regaddr=0
	local ctrl_reg=32776
	#Start condition
	printf ":" >> $out_device; 
	printf ":";
	#Motor number
	if [ $devaddr -lt 16 ]; then 
		printf "0%X" $devaddr >> $out_device; 
		printf "0%X" $devaddr;
	else 
		printf "%X" $devaddr >> $out_device; 
		printf "%X" $devaddr;
	fi
	#Function number
	if [ $func -lt 16 ]; then 
		printf "0%X" $func >> $out_device; 
		printf "0%X" $func;
	else 
		printf "%X" $func >> $out_device; 
		printf "%X" $func;
	fi
	#Register number
	if [ $regaddr -lt 16 ]; then 
		printf "0%X" $regaddr >> $out_device; 
		printf "0%X" $regaddr;
	else 
		printf "%X" $regaddr >> $out_device; 
		printf "%X" $regaddr;
	fi
	#Register value
	if [ $ctrl_reg -lt 16 ]; then 
		printf "000%X" $ctrl_reg >> $out_device; 
		printf "000%X" $ctrl_reg;
	elif [ $ctrl_reg -lt 256 ]; then 
		printf "00%X" $ctrl_reg >> $out_device; 
		printf "00%X" $ctrl_reg;
	elif [ $ctrl_reg -lt 4096 ]; then 
		printf "0%X" $ctrl_reg >> $out_device; 
		printf "0%X" $ctrl_reg;
	else 
		printf "%X" $ctrl_reg >> $out_device; 
		printf "%X" $ctrl_reg;
	fi
	#Checksum
	crc=$((((0-($devaddr+$func+$regaddr+(($ctrl_reg>>8)&255)+($ctrl_reg&255)))&255)))
	if [ $crc -lt 16 ]; then 
		printf "0%X\n" $crc >> $out_device; 
		printf "0%X\n" $crc;
	else 
		printf "%X\n" $crc >> $out_device; 
		printf "%X\n" $crc;
	fi
	return
}

#Start motor forward
start_motor ()
{
	local crc
	local func=3
	local regaddr=0
	local ctrl_reg=32775
	#Start condition
	printf ":" >> $out_device; 
	printf ":";
	#Motor number
	if [ $devaddr -lt 16 ]; then 
		printf "0%X" $devaddr >> $out_device; 
		printf "0%X" $devaddr;
	else 
		printf "%X" $devaddr >> $out_device; 
		printf "%X" $devaddr;
	fi
	#Function number
	if [ $func -lt 16 ]; then 
		printf "0%X" $func >> $out_device; 
		printf "0%X" $func;
	else 
		printf "%X" $func >> $out_device; 
		printf "%X" $func;
	fi
	#Register number
	if [ $regaddr -lt 16 ]; then 
		printf "0%X" $regaddr >> $out_device; 
		printf "0%X" $regaddr;
	else 
		printf "%X" $regaddr >> $out_device; 
		printf "%X" $regaddr;
	fi
	#Register value
	if [ $ctrl_reg -lt 16 ]; then 
		printf "000%X" $ctrl_reg >> $out_device; 
		printf "000%X" $ctrl_reg;
	elif [ $ctrl_reg -lt 256 ]; then 
		printf "00%X" $ctrl_reg >> $out_device; 
		printf "00%X" $ctrl_reg;
	elif [ $ctrl_reg -lt 4096 ]; then 
		printf "0%X" $ctrl_reg >> $out_device; 
		printf "0%X" $ctrl_reg;
	else 
		printf "%X" $ctrl_reg >> $out_device; 
		printf "%X" $ctrl_reg;
	fi
	#Checksum
	crc=$((((0-($devaddr+$func+$regaddr+(($ctrl_reg>>8)&255)+($ctrl_reg&255)))&255)))
	if [ $crc -lt 16 ]; then 
		printf "0%X\n" $crc >> $out_device; 
		printf "0%X\n" $crc;
	else 
		printf "%X\n" $crc >> $out_device; 
		printf "%X\n" $crc;
	fi
	return
}

#Start motor backward
reverse_motor ()
{
	local crc
	local func=3
	local regaddr=0
	local ctrl_reg=32791
	#Start condition
	printf ":" >> $out_device; 
	printf ":";
	#Motor number
	if [ $devaddr -lt 16 ]; then 
		printf "0%X" $devaddr >> $out_device; 
		printf "0%X" $devaddr;
	else 
		printf "%X" $devaddr >> $out_device; 
		printf "%X" $devaddr;
	fi
	#Function number
	if [ $func -lt 16 ]; then 
		printf "0%X" $func >> $out_device; 
		printf "0%X" $func;
	else 
		printf "%X" $func >> $out_device; 
		printf "%X" $func;
	fi
	#Register number
	if [ $regaddr -lt 16 ]; then 
		printf "0%X" $regaddr >> $out_device; 
		printf "0%X" $regaddr;
	else 
		printf "%X" $regaddr >> $out_device; 
		printf "%X" $regaddr;
	fi
	#Register value
	if [ $ctrl_reg -lt 16 ]; then 
		printf "000%X" $ctrl_reg >> $out_device; 
		printf "000%X" $ctrl_reg;
	elif [ $ctrl_reg -lt 256 ]; then 
		printf "00%X" $ctrl_reg >> $out_device; 
		printf "00%X" $ctrl_reg;
	elif [ $ctrl_reg -lt 4096 ]; then 
		printf "0%X" $ctrl_reg >> $out_device; 
		printf "0%X" $ctrl_reg;
	else 
		printf "%X" $ctrl_reg >> $out_device; 
		printf "%X" $ctrl_reg;
	fi
	#Checksum
	crc=$((((0-($devaddr+$func+$regaddr+(($ctrl_reg>>8)&255)+($ctrl_reg&255)))&255)))
	if [ $crc -lt 16 ]; then 
		printf "0%X\n" $crc >> $out_device; 
		printf "0%X\n" $crc;
	else 
		printf "%X\n" $crc >> $out_device; 
		printf "%X\n" $crc;
	fi
	return
}

: <<'END'
#Start process to read responses
start_response_reading ()
{
	killall cat
	killall cat
	killall cat
	killall cat
	killall cat
	usleep 2000000;
	rm $resp_device
	touch $resp_device
	cat $out_device >> $resp_device &
	usleep 2000000;
	return
}
END

: <<'END'
#Determine last responses
determine_last_response ()
{
	local i=0
	while read line           
	do
		tmpstr[$i]="$line"
		i=$((i+1))
	done < "$resp_device"
	laststring=$((tmpstr[0]))
	echo $i 
	return
}
END

#Init PWM period
period=10000
devaddr=0; set_period_for_motor
devaddr=1; set_period_for_motor
devaddr=2; set_period_for_motor
devaddr=3; set_period_for_motor

#Init PWM duty
duty=1
devaddr=0; set_duty_for_motor
devaddr=1; set_duty_for_motor
devaddr=2; set_duty_for_motor
devaddr=3; set_duty_for_motor

devaddr=0;

SELNUM=1
while [[ $SELNUM != 0 ]]; do
	clear
	echo "
	Please Select:
	1. Select motor number: $((devaddr+1))
	2. Change PWM period: $period
	3. Change PWM duty: $duty
	4. Start motor forward
	5. Start motor backward
	6. Brake motor
	7. Stop motor
	0. Exit
	"
	read -p "Enter selection [0-7] > " SELNUM
	#Testing valid input
	if [[ -z $SELNUM ]]; then 
		SELNUM=1000;
	fi
	case $SELNUM in
		1)	read -p "Enter motor number [1-4]: " mnum
		if [[ $mnum -lt 1 || $mnum -gt 4 ]]; then
			echo "Incorrect motor number!"
			usleep 2000000
		else 
			devaddr=$((mnum-1))
		fi
		;;
		2)	read -p "Enter PWM period [1..65535]: " mper
		if [[ $mper -lt 1 || $mper -gt 65535 ]]; then
			echo "PWM period must be in [1..65535] range!"
			usleep 2000000
		elif [[ $mper -lt $duty ]]; then
			echo "PWM period must be greater than PWM duty!"
			usleep 2000000
		else 
			period=$mper
			set_period_for_motor
		fi
		;;
		3)	read -p "Enter PWM duty [1..65535]: " mdut
		if [[ $mdut -lt 1 || $mdut -gt 65535 ]]; then
			echo "PWM duty must be in [1..65535] range!"
			usleep 2000000
		elif [[ $mdut -gt $period ]]; then
			echo "PWM duty must be less than PWM period!"
			usleep 2000000
		else 
			duty=$mdut
			set_duty_for_motor
		fi
		;;
		4) start_motor
		;;
		5) reverse_motor
		;;
		6) brake_motor
		;;
		7) stop_motor
		;;
		1000) echo "Invalid input!"
		usleep 2000000
		;;
	esac
done	
echo "Program terminated"

