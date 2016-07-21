# BlueFinder
A rangefinding application used to identify and locate IEEE 802.15.1 devices. This application is capable of detecting and locating Bluetooth devices using the classic Bluetooth protocol and Bluetooth Low Energy. BlueFinder is built to run on a Bluetooth adapter running BCM20702A0 drivers. his command line application uses the log-distance path loss model (LDPL) to calculate a distance estimate based on Received Signal Strength (RSS) from a target transceiver.

## Usage
Two modes exists within BlueFinder: Bluetooth Classic and BLE. To call the BLE rangefinding function, use ```-b``` and Bluetooth Classic uses the tag ```-c```. BlueFinder has an optional long range mode ```-l``` which utilizes the UD-100 Bletooth Adapter which is currently only supported with BLE. The long range mode requires the gain of the antenna (dB).

```./BlueFinder -b -l Ant BD_ADDR ```

## Requirements
- Tested and developed on [Kali Linux](https://www.kali.org/) v2016.1.
- [Bluetooth Smart USB Adapter (BCM20702A0)] (https://www.amazon.com/Plugable-Bluetooth-Adapter-Raspberry-Compatible/dp/B009ZIILLI/ref=sr_1_2?s=pc&ie=UTF8&qid=1469111177&sr=1-2-spons&keywords=bluetooth+adapter&psc=1)
- [Sena UD100 BLuetooth USB Adapter] (https://www.amazon.com/Sena-UD100-Bluetooth-Class1-Adapter/dp/B01BHD7WR2)

## Build and Install
- Requires Bluez 5.29 (or greater)

## Version
- v1.3a released 21 July 2016