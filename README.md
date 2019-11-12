# Male-P.I.W.O
Projekt realizowany na kursie Zastosowania Systemów Wbudowanych (PWr)
## Working with submodules
Cloning repository:
```
git clone git@github.com:kuras120/Male-P.I.W.O-Core.git --recurse-submodules 
```
Updating submodules to latest version:
```
git submodule foreach git pull origin master
git add .
git commit -m "Update submodules"
git push
```
## Useful commands
### Find pi on local network
Scan network with nmap looking for open ssh ports
```
sudo nmap -sS -p 22 192.168.0.1/24
```
### Mount pi home folder on local file system
```
sudo mkdir /mnt/pi
sudo sshfs -o allow_other pi@192.168.0.32:/home/pi /mnt/pi
```
To unmount:
```
sudo umount /mnt/pi
```
To persist after reboot, add this entry to `/etc/fstab`
```
sshfs#pi@192.168.0.32:/home/pi /mnt/pi
```
## Bluetooth speaker configuration
Speaker MAC address: `8D:16:E5:43:83:47`

Install dependencies and add pi user to bluetooth group:
```
sudo apt-get install pulseaudio pulseaudio-module-bluetooth
sudo usermod -G bluetooth -a pi
sudo reboot
```
Add switching to newly connected devices - edit `/etc/pulse/default.pa` and add:
``` 
# automatically switch to newly-connected devices
load-module module-switch-on-connect
```
Enable bluetooth
```console
pi@raspberrypi:~/piwo-core $ bluetoothctl 
Agent registered
[bluetooth]# power on
[bluetooth]# agent on
```
Turn on the device, pair and connect with device
```console
[bluetooth]# scan on
[bluetooth]# pair 8D:16:E5:43:83:47
[bluetooth]# trust 8D:16:E5:43:83:47
[bluetooth]# connect 8D:16:E5:43:83:47
```
Kill Bluealsa and start PulseAudio
```
sudo killall bluealsa
pulseaudio --start
```
List available sinks and set default sink to speaker
```
pacmd-list
pacmd set-card-profile bluez_card.8D_16_E5_43_83_47 a2dp_sink
pacmd set-default-sink bluez_sink.8D_16_E5_43_83_47.a2dp_sink

```
Download and play example file;
```
wget http://youness.net/wp-content/uploads/2016/08/h2g2.ogg -P /tmp/
paplay /tmp/h2g2.ogg --volume 15000 -v

```
Supported audio formats are .wav and .ogg. For complete list see [libsendfile](http://www.mega-nerd.com/libsndfile/).
### Troubleshooting
Check syslog
```
tail -100f /var/log/syslog | less
```
org.Bluez.Error.NotReady
```
rfkill unblock all
bluetoothctl power on
```
### Sources
 - [Guide #1](https://youness.net/raspberry-pi/how-to-connect-bluetooth-headset-or-speaker-to-raspberry-pi-3)
 - [Guide #2](https://gist.github.com/actuino/9548329d1bba6663a63886067af5e4cb)
 - [Guide #3 (GUI)](https://github.com/binnes/tobyjnr/wiki/Getting-Sound-to-work-on-the-Raspberry-Pix)
 - [Automatic connection](https://raspberrypi.stackexchange.com/questions/53408/automatically-connect-trusted-bluetooth-speaker)
 
 
