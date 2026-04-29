import asyncio
import socket
from bleak import BleakClient

# Direccion batuta de probas: 1C:DB:D4:34:55:BA. Direccion batuta prototipo: 1C:DB:D4:34:55:BA
ADDRESS_TEST = "1C:DB:D4:34:55:BA"
ADDRESS_PROTOTYPE = "1C:DB:D4:36:9E:C2"

address = ADDRESS_TEST
CHARACTERISTIC_UUID = "abcd1234-5678-1234-5678-abcdef123456"

# --- TCP/UDP Cliente ---
UDP = 0
TCP = 1

mode = TCP # o UDP

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
    print(f"Pulso detectado. Datos crudos: {data}")
    # Se envía una cabecera [30] seguida de los datos de la batuta
    send_gesture(bytes([30]) + bytes(data))

async def main(address):
    disconnected_event = asyncio.Event()

    def disconnected_callback(client: BleakClient):
        print("[!] Desconectado de la batuta.")
        disconnected_event.set()

    while True:
        try:
            print(f"Conectando a {address}...")
            async with BleakClient(address, disconnected_callback=disconnected_callback) as client:
                print("Conectado. Esperando movimientos...")
                await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
                await disconnected_event.wait()
        except Exception as e:
            print(f"Error de conexión: {e}. Reintentando en 2 segundos...")
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main(address))