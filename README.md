# Manager for V2 Lighthouses by Valve/HTC
This python script helps you switch your Steam HMD lighthouses V2 on and into stand-by. Unfortunately, my Pimax XR needs the lighthouses up and running before I turn it on, so the awesome work done by [@mann1x]( https://github.com/mann1x ) in his project [Pimax BS Manager](https://github.com/mann1x/pimax_bs_manager) is of litte use to me. This may be different with your particular Pimax HMD.

## installation & prerequisites
Make sure that you have the following:
* Windows 10, at least 17xx build 
* BLE / Bluetooth 4.0 dongle installed and connected (*not* a BGAPI one!)
* Python 3, I used Python 3.8.2
* Pythonnet installation from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pythonnet)
  1. download `pythonnet‑2.4.1.dev0‑cp38‑cp38‑win_amd64.whl` 
  2. `pip3 install pythonnet‑2.4.1.dev0‑cp38‑cp38‑win_amd64.whl`
* bleak installed `pip3 install bleak`

## usage with command line arguments
The script provides three usage options: discovery, turning on and switch to standby of a lighthouse V2.

### discovery
If you don't call it with any arguments, it tries to open your BLE device and scans for BLE servers in range. Once found, it looks for the service and characteristic which allow for the power-up and power-down of a lighthouse V2. Look for the MAC addresses and the results on stdout.

**usage:** `python3 .\lighthouse-v2-manager.py`

### turning lighthouses into standby
If you want to switch a lighthouse off ("stand-by"), specify either "off" as first argument and then each MAC address consecutively as further arguments like so:

**usage:** `python3 .\lighthouse-v2-manager.py off aa:aa:aa:aa:aa:aa bb:bb:bb:bb:bb:bb ...`

The lighthouses LED will now start a blue breathing animation, that is, it will fade-in and fade-out to indicate its standby operation state.

### turning lighthouses back on
If you want to switch a lighthouse back on, specify either "on" as first argument and then each MAC address consecutively as further arguments like so:

**usage:** `python3 .\lighthouse-v2-manager.py on aa:aa:aa:aa:aa:aa bb:bb:bb:bb:bb:bb ...`

The lighthouses LED will power up. As soon as it's stabilized, the LED turns solid green.

### Hard-coding your Lighthouses' MAC addresses
Inside the script, you can edit the list `lh_macs` to contain the MAC addresses of your lighthouses as strings. Doing so allows a shorter command line interaction:
* `python3 .\lighthouse-v2-manager.py on`
* `python3 .\lighthouse-v2-manager.py off`

Still, you can add other MAC addresses dynamically even after you put some in the file itself:
* `python3 .\lighthouse-v2-manager.py off cc:cc:cc:cc:cc:cc`
