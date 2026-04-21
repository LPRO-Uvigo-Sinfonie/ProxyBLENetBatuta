import asyncio
from bleak import BleakClient
import socket

address = "1C:DB:D4:34:55:BA"
SERVICE_UUID = "12345678-1234-1234-1234-123456789abc"
CHARACTERISTIC_UUID = "abcd1234-5678-1234-5678-abcdef123456"

# --- TCP/UDP Cliente ---
UDP = 0
TCP = 1

mode = UDP # o UDP

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if mode == TCP else socket.SOCK_DGRAM)
SERVER_ADDR = ("localhost", 8090)

if mode == TCP:
    client_socket.connect(SERVER_ADDR)

def send_gesture(msg: bytes):
    if mode == TCP:
        client_socket.sendall(msg)
    else:
        client_socket.sendto(msg, SERVER_ADDR)

def notification_handler(characteristic: str, data: bytearray):
    print(f"Paquete: {data}")
    send_gesture(bytes([30]) + bytes(data))

async def main(address):
    disconnected_event = asyncio.Event()

    def disconnected_callback(client: BleakClient):
        print("Disconnected callback called!")
        disconnected_event.set()

    while True:
        try:
            async with BleakClient(address, disconnected_callback=disconnected_callback) as client:
                await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
                await disconnected_event.wait()
        except:
            print("Error connection")

asyncio.run(main(address))