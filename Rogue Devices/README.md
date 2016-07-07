# Rogue Devices
Creates a spoofed version of the Bluetooth Low Energy devices using Bleno. These are files that can be used with [Bleno](https://github.com/sandeepmistry/bleno).

## Before Execution

### Bleno
The device name and current nonce needs to be found either using the [BLE Stack] (https://github.com/merculite/BLE-Security/tree/master/Bluetooth-Locks) developed to hack door locks or a 3rd party program that can run on mobile devices (e.g. [LightBlue Explorer] (https://punchthrough.com/).   

### Quicklock

## Installation & Execution
- Install [Bleno](https://github.com/sandeepmistry/bleno).
- Replace bleno/lib/hci-socket/Gatt.js file with custom file provided.
- Execute Bitlock.js or Quicklock.js

```sudo node Bitlock.js```