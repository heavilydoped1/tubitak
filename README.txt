Getting Started on Linux
These are the instructions for installing our RTL-SDR Blog drivers. Type them into the Linux terminal one by one.

First, if you already have some other drivers installed, please purge them from your system using the following commands:

sudo apt purge ^librtlsdr
sudo rm -rvf /usr/lib/librtlsdr* /usr/include/rtl-sdr* /usr/local/lib/librtlsdr* /usr/local/include/rtl-sdr* /usr/local/include/rtl_* /usr/local/bin/rtl_*
Next you can install the RTL-SDR Blog drivers using the following.

sudo apt-get install libusb-1.0-0-dev git cmake pkg-config build-essential
git clone https://github.com/rtlsdrblog/rtl-sdr-blog
cd rtl-sdr-blog/
mkdir build
cd build
cmake ../ -DINSTALL_UDEV_RULES=ON
make
sudo make install
sudo cp ../rtl-sdr.rules /etc/udev/rules.d/
sudo ldconfig
After installing the libraries you will likely need to unload the DVB-T drivers, which Linux uses by default. To unload them temporarily type "sudo rmmod dvb_usb_rtl28xxu" into terminal. This solution is only temporary as when you replug the dongle or restart the PC, the DVB-T drivers will be reloaded. For a permanent solution, create a text file "rtlsdr.conf" in /etc/modprobe.d and add the line "blacklist dvb_usb_rtl28xxu". You can use the one line command shown below to automatically write and create this file.

echo 'blacklist dvb_usb_rtl28xxu' | sudo tee --append /etc/modprobe.d/blacklist-dvb_usb_rtl28xxu.conf
Now you can restart your device. After it boots up again run "rtl_test" at the terminal with the RTL-SDR plugged in. It should start running.

NOTE: Some devices like the Orange Pi zero have a bug in their current mainline OSes. Instead of blacklisting "dvb_usb_rtl28xxu", you will need to blacklist "dvb_usb_rtl2832u". If you installed rtl-sdr by "apt-get", you will need to update the black list file at /etc/modprobe.d/rtl-sdr-blacklist.conf manually too.
