# Manager for V2 Lighthouses by Valve/HTC
This python script helps you switch your Valve Lighthouses V2 on and into stand-by. Unfortunately, my Pimax 5K XR needs the lighthouses up and running before I turn it on, so the awesome work done by [@mann1x]( https://github.com/mann1x ) in his project [Pimax BS Manager](https://github.com/mann1x/pimax_bs_manager) is of little use to me. This may be different with your particular Pimax HMD.

## installation (Windows binary release)
1. Create a folder where you want to store the manager's files, e.g. `C:\Program Files\LH-Manager`. 
1. Download and copy the files (executable and both icons) from [this repository's releases page](https://github.com/nouser2013/lighthouse-v2-manager/releases) into the target folder from step 1. Depending on the destination, administrative privileges may be required for copying.
1. Make sure your Bluetooth Low-Energy dongle is connected.
1. Open a command prompt and navigate to the folder from step 1, e.g. `C:\Program Files\LH-Manager`. From there, follow the instructions in the chapter "Usage".

## installation & prerequisites (python script version)
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

**Note:** if you installed the binary version, simply call the program by executing it. Instead of `python3 .\lighthouse-v2-manager.py` type `lighthouse-v2-manager.exe` in the command prompt window for the commands below.

### display instructions
If you call the executable/script with no command line arguments or with an invalid command, the useage instructions are returned. Choose one of the commands `discover`, `on` or `off` to interact with your Lighthouses V2.

**usage:** `python3 .\lighthouse-v2-manager.py`

### discovery
If you call the program with the `discover` command, it tries to open your BLE device and scans for BLE servers in range. Once found, it looks for the service and characteristic which allow for the power-up and power-down of a lighthouse V2. Look for the MAC addresses and the results on the console output.

Optionally, since version 1.1, you can specify the command line option `-cs` or `--create-shortcuts` with the discovery command. The program then tries to create suitable shortcuts for your installation and your Lighthouses' MAC addresses. This works with both the script version and the binary stand-alone version.

**usage:** `python3 .\lighthouse-v2-manager.py discover [-cs,--create-shortcuts]`

### switch lighthouses into standby
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

## Credits
* [Enzo Geant](https://github.com/egeant94) for the new on/off icons. Thanks for your contribution.
