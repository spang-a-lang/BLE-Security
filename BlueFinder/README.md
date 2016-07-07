# BlueFinder
A rangefinding application used to identify and locate IEEE 802.15.1 devices. This application is capable of detecting and locating Bluetooth devices using the classic Bluetooth protocol and Bluetooth Low Energy. BlueFinder is built to run on a Bluetooth adapter running BCM20702A0 drivers. his command line application uses the log-distance path loss model (LDPL) to calculate a distance estimate based on Received Signal Strength (RSS) from a target transceiver.

## Usage
Two modes exists within BlueFinder: Bluetooth Classic and BLE. To call the BLE rangefinding function, use ```-B``` and Bluetooth Classic uses the tag ```-C```.

```./BlueFinder -B BD_ADDR```

## Requirements
- Tested and developed on [Kali Linux](https://www.kali.org/) v2016.1.
- Bluetooth Smart USB Adapter (BCM20702A0)

## Build and Install
- Requires Bluez 5.29 (or greater)

## Version
- v1.2 released 30 May 2016

## Future Releases
- v1.3a - transfering code to run completely in python compared to a comination of bash and python
