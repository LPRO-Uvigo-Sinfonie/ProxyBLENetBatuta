import asyncio
from bleak import BleakScanner

async def atopar_dispositivos():
    print("Iniciando escaneo de dispositivos Bluetooth (BLE)...")
    print("Agarda uns 5 segundos...\n")
    
    # O método discover() escoita os paquetes de anuncio (advertising packets)
    # emitidos polos dispositivos BLE próximos.
    dispositivos = await BleakScanner.discover()
    
    if not dispositivos:
        print("Non se atopou ningún dispositivo BLE.")
        return

    print(f"{'DIRECCIÓN MAC':<20} | {'NOME DO DISPOSITIVO'}")
    print("-" * 50)
    for d in dispositivos:
        # Algúns dispositivos non emiten nome, polo que d.name pode ser None
        nome = d.name if d.name else "Descoñecido / Sen nome"
        print(f"{d.address:<20} | {nome}")
    print("-" * 50)

if __name__ == "__main__":
    asyncio.run(atopar_dispositivos())