import socket
import json
import time
import mido

puertoUDPMidi = 62002

class UDPClient:
    def __init__(self, ip: str, port: int):
        self.address = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.setblocking(False) 

    def send(self, data: dict):
        try:
            self.sock.sendto(json.dumps(data).encode('utf-8'), self.address)
        except BlockingIOError:
            pass
        except Exception:
            pass


def capturadorMidi(ipDestinoMetaQuest: str):
    print(f"Inicializando MIDI Sender para Meta quest con IP: {ipDestinoMetaQuest} y puerto:{puertoUDPMidi}")
    
    clienteUdp = UDPClient(ipDestinoMetaQuest, puertoUDPMidi)
    
    try:
        puertoMidi = mido.get_input_names()[0]
        print(f"Dispositivo MIDI conectado, el puerto es: {puertoMidi}")
        
        with mido.open_input(puertoMidi) as puerto:
            for msg in puerto:
                if msg.type == "note_on" or msg.type == "note_off":
                    datoNota = analizarNota(msg)
                    
                    if datoNota:
                        print(f"Enviando dato MIDI por UDP a la direccion {ipDestinoMetaQuest} a traves del puerto {puertoUDPMidi} el siguiente diccionario: Evento: {datoNota['event']}, Nota: {datoNota['note']}, Velocidad: {datoNota['velocity']}, Timestamp: {datoNota['timestamp']}, ")
                        
                        clienteUdp.send(datoNota)
                        
    except IndexError:
        print("No se detectó ningún dispositivo MIDI conectado.")
    except Exception as e:
        print(f"Error en MIDI Listener: {e}")

def analizarNota(msg):
    timestamp_ms = int(time.time() * 1000) 
    
    if msg.type == "note_on" and msg.velocity == 0:
        msg_type = "note_off"
    else:
        msg_type = msg.type
    
    if msg.type == "note_on" or msg.type == "note_off":
        return {
            "event": msg_type, 
            "note": msg.note, 
            "velocity": msg.velocity,
            "timestamp": timestamp_ms
        }
    return None