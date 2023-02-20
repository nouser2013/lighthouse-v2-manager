#!/usr/bin/env python3

import asyncio
import sys
import re
import os

__PWR_SERVICE        = "00001523-1212-efde-1523-785feabcd124"
__PWR_CHARACTERISTIC = "00001525-1212-efde-1523-785feabcd124"
__PWR_ON             = bytearray([0x01])
__PWR_STANDBY        = bytearray([0x00])
__power_state        = ""

command = ""
lh_macs = [] # hard code mac addresses here if you want, otherwise specify in command line

print(" ")
print("=== LightHouse V2 Manager ===")
print(" ")

cmdName = os.path.basename(sys.argv[0])
cmdPath = os.path.abspath(sys.argv[0]).replace(cmdName, "")
cmdStr  = (cmdPath+cmdName).replace(os.getcwd(), ".")
if cmdStr.find(".py")>0:
	cmdStr = '"'+ sys.executable +'" "' + cmdStr + '"'

if len(sys.argv)>1 and sys.argv[1] in ["on", "off", "discover", "toggle"]:
	command = sys.argv[1]

if len(sys.argv)==1 or command=="":
	print(" Invalid or no command given. Usage:")
	print(" ")
	print(" * discover lighthouses V2:")
	print("   "+ cmdStr +" discover [--create-shortcuts, -cs]")
	print(" ")
	print(" * power one or more lighthoses V2 ON:")
	print("   "+ cmdStr +" on [MAC1] [MAC2] [...MACn]")
	print(" ")
	print(" * power one or more lighthoses V2 OFF:")
	print("   "+ cmdStr +" off [MAC1] [MAC2] [...MACn]")
	print(" ")
	print(" * toggle one or more lighthoses V2 ON or OFF:")
	print("   "+ cmdStr +" toggle [MAC1] [MAC2] [...MACn]")
	print(" ")
	sys.exit()

from bleak import discover, BleakClient

async def run(loop, lh_macs):
	if command == "discover":
		lh_macs = []
		createShortcuts = True if ("-cs" in sys.argv or "--create-shortcuts" in sys.argv) else False
		print(">> MODE: discover suitable V2 lighthouses")
		if createShortcuts: print("         and create desktop shortcuts")
		print(" ")
		print (">> Discovering BLE devices...")
		devices = await discover()
		for d in devices:
			deviceOk = False
			if type(d.name) != str or d.name.find("LHB-") != 0:
				continue
			print (">> Found potential Valve Lighthouse at '"+ d.address +"' with name '"+ d.name +"'...")
			services = None
			async with BleakClient(d.address) as client:
				try:
					services = await client.get_services()
				except:
					print(">> ERROR: could not get services.")
					continue
			for s in services:
				if (s.uuid==__PWR_SERVICE):
					print("   OK: Service "+ __PWR_SERVICE +" found.")
					for c in s.characteristics:
						if c.uuid==__PWR_CHARACTERISTIC:
							print("   OK: Characteristic "+ __PWR_CHARACTERISTIC +" found.")
							print(">> This seems to be a valid V2 Base Station.")
							print(">> Trying to connect to BLE MAC '"+ d.address +"'...")
							try:
								client = BleakClient(d.address, loop=loop)
								await client.connect()
								print(">> '"+ d.address +"' connected...")
								__power_state = await client.read_gatt_char(__PWR_CHARACTERISTIC)
								print("Device power state: "+ __power_state.hex())
								await client.disconnect()
								print(">> disconnected. ")
							except Exception as e:
								print(">> ERROR: "+ str(e))
							print(" ")
						print(" ")
						lh_macs.append(d.address)
						deviceOk = True
			if not deviceOk:
				print(">> ERROR: Service or Characteristic not found.")
				print(">>        This is likely NOT a suitable Lighthouse V2.")
				print(" ")
		if len(lh_macs)>0:
			print(">> OK: At least one compatible V2 lighthouse was found.")
			print(" ")
			if createShortcuts:
				print(">> Trying to create Desktop Shortcuts...")
				import winshell
				from win32com.client import Dispatch
				desktop = winshell.desktop()
				path = os.path.join(desktop, "LHv2-ON.lnk")
				shell = Dispatch('WScript.Shell')
				shortcut = shell.CreateShortCut(path)
				if cmdName.find(".py")>0:
					shortcut.Targetpath = sys.executable
					shortcut.Arguments = '"' + cmdName + '" on '+ " ".join(lh_macs)
				else:
					shortcut.Targetpath = '"' + cmdPath + cmdName + '"'
					shortcut.Arguments = "on "+ " ".join(lh_macs)
				shortcut.WorkingDirectory = cmdPath[:-1]
				shortcut.IconLocation = cmdPath + "lhv2_on.ico"
				shortcut.save()
				print("   * OK: LHv2-ON.lnk was created successfully.")
				path = os.path.join(desktop, "LHv2-OFF.lnk")
				shell = Dispatch('WScript.Shell')
				shortcut = shell.CreateShortCut(path)
				if cmdName.find(".py")>0:
					shortcut.Targetpath = sys.executable
					shortcut.Arguments = '"' + cmdName + '" off '+ " ".join(lh_macs)
				else:
					shortcut.Targetpath = '"' + cmdPath + cmdName + '"'
					shortcut.Arguments = "off "+ " ".join(lh_macs)
				shortcut.WorkingDirectory = cmdPath[:-1]
				shortcut.IconLocation = cmdPath + "lhv2_off.ico"
				shortcut.save()
				print("   * OK: LHv2-OFF.lnk was created successfully.")
			else:
				print("   OK, you need to manually create two links, for example on your desktop:")
				print(" ")
				print("   To turn your lighthouses ON:")
				print("    * Link Target: "+ cmdStr +" on "+ " ".join(lh_macs))
				print(" ")
				print("   To turn your lighthouses OFF:")
				print("    * Link Target: "+ cmdStr +" off "+ " ".join(lh_macs))
		else:
			print(">> Sorry, not suitable V2 Lighthouses found.")
		print(" ")

	if command in ["on", "off", "toggle"]:
		print(">> MODE: switch lighthouses "+ command.upper())
		lh_macs.extend(sys.argv[2:])
		for mac in list(lh_macs):
			if re.match("[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}", mac):
				continue
			print("   * Invalid MAC address format: "+mac)
			lh_macs.remove(mac)
		if len(lh_macs) == 0:
			print(" ")
			print(">> ERROR: no (valid) base station MAC addresses given.")
			print(" ")
			sys.exit()
		for mac in lh_macs:
			print("   * "+mac)
		print(" ")
		for mac in lh_macs:
			if command.upper() == "TOGGLE":
				print(">> Trying to connect to BLE MAC '"+ mac +"'...")
				try:
					client = BleakClient(mac, loop=loop)
					await client.connect()
					print(">> '"+ mac +"' connected...")
					get_power_state = await client.read_gatt_char(__PWR_CHARACTERISTIC)
					print("Getting Basestation power state...")
					if get_power_state.hex() == "00":
						print("Basestation is off, turning on.")
						await client.write_gatt_char(__PWR_CHARACTERISTIC, __PWR_ON)
					else:
						print("Basestation is on, putting in standby.")
						await client.write_gatt_char(__PWR_CHARACTERISTIC, __PWR_STANDBY)
					await client.disconnect()
					print(">> disconnected. ")
					print("Basestation toggled.")
				except Exception as e:
					print(">> ERROR: "+ str(e))
				print(" ")
			elif command.upper() == "ON":
				print(">> Trying to connect to BLE MAC '"+ mac +"'...")
				try:
					client = BleakClient(mac, loop=loop)
					await client.connect()
					print(">> '"+ mac +"' connected...")
					print("Powering ON...")
					await client.write_gatt_char(__PWR_CHARACTERISTIC, __PWR_ON)
					await client.disconnect()
					print(">> disconnected. ")
					print("Basestation has been turned on.")
				except Exception as e:
					print(">> ERROR: "+ str(e))
				print(" ")
			else:
				print(">> Trying to connect to BLE MAC '"+ mac +"'...")
				try:
					client = BleakClient(mac, loop=loop)
					await client.connect()
					print(">> '"+ mac +"' connected...")
					print("Putting in STANDBY...")
					await client.write_gatt_char(__PWR_CHARACTERISTIC, __PWR_STANDBY)
					await client.disconnect()
					print(">> disconnected. ")
					print("Basestation has been put in standby.")
				except Exception as e:
					print(">> ERROR: "+ str(e))
				print(" ")

loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop, lh_macs))
