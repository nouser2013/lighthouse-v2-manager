import asyncio
import sys
from bleak import discover, BleakClient

__PWR_SERVICE        = "00001523-1212-efde-1523-785feabcd124"
__PWR_CHARACTERISTIC = "00001525-1212-efde-1523-785feabcd124"
__PWR_ON             = bytearray([0x01])
__PWR_STANDBY        = bytearray([0x00])

command = "discover"
# hard code mac addresses here if you want, otherwise specify in command line
# lh_macs = ["AA:BB:CC:DD:EE:FF", "FF:EE:DD:CC:BB:AA"]
lh_macs = []

print(" ")
print("=== LightHouse V2 Manager ===")
print(" ")
if "--help" in sys.argv or "-?" in sys.argv:
	print(" discover lighthouses: "+sys.argv[0])
	print(" set state on/standby: "+sys.argv[0]+" [on|off] [MAC1] [MAC2] [MACn]")
	print(" ")
	sys.exit()

if len(sys.argv)==1:
	print(">> MODE: discover suitable V2 lighthouses")
	print(" ")
elif sys.argv[1] == "on":
	lh_macs.extend(sys.argv[2:])
	command = "on"
	print(">> MODE: switch lighthouses on")
	for mac in lh_macs: print("   * "+mac)
	print(" ")
elif sys.argv[1] == "off":
	lh_macs.extend(sys.argv[2:])
	command = "standby"
	print(">> MODE: switch lighthouses to standby")
	for mac in lh_macs: print("   * "+mac)
	print(" ")
else:
	print(">> ERROR: no suitable command given. Try running with --help or -?")
	print(" ")
	sys.exit()

async def run(loop):
	if command == "discover":
		print (">> Discovering BLE devices...")
		devices = await discover()
		for d in devices:
			deviceOk = False
			if d.name.find("LHB-") != 0:
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
							print(" ")
							deviceOk = True
			if not deviceOk:
				print(">> ERROR: Service or Characteristic not found.")
				print(">>        This is likely NOT a suitable Lighthouse V2.")
				print(" ")
	else:
		for mac in lh_macs:
			print(">> Trying to connect to BLE MAC '"+ mac +"'...")
			try:
				client = BleakClient(mac, loop=loop)
				await client.connect()
				print(">> '"+ mac +"' connected...")
				await client.write_gatt_char(__PWR_CHARACTERISTIC, __PWR_ON if command=="on" else __PWR_STANDBY)
				print(">> LH switched to '"+ command +"' successfully... ")
				await client.disconnect()
				print(">> disconnected. ")
			except Exception as e:
				print(">> ERROR: "+ str(e))
			print(" ")
loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
