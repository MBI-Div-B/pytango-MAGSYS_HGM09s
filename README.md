# pytango-MagsysHGM09s

pytango device server for Magsys HGM09s handheld Hall probe

## device settings
The device needs to be in serial communication mode:
* hold "RANGE" button for 3+ seconds
* set "USB MODE" to "SERIAL" by pressing DATA button, confirm with SETUP button 

## kernel module configuration
The kernel by default tries to load the `cdc-acm` module, which doesn't work with the device. Blacklist the module:

```bash
echo "blacklist cdc-acm" > /etc/modprobe.d/blacklist-cdc-acm.conf
```

Force using the usbserial module. Which of the two methods below works depends on the OS:

### method 1
interactive command to test:
```bash
sudo modprobe usbserial vendor=0x04d8 product=0xfe78
```

corresponding udev rule:
```bash
SUBSYSTEM=="usb", ATTR{idVendor}=="04d8", ATTR{idProduct}=="fe78", RUN+="/usr/sbin/modprobe usbserial vendor=0x04d8 product=0xfe78"
```

### method 2
```bash
sudo echo 04d8 fe78 > /sys/bus/usb-serial/drivers/generic/new_id
```
udev rule:
```bash
SUBSYSTEM=="usb", ATTR{idVendor}=="04d8", ATTR{idProduct}=="fe78", RUN+="/bin/sh -c 'echo 04d8 fe78 > /sys/bus/usb-serial/drivers/generic/new_id'"
```
