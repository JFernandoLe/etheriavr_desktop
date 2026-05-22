import socket
import json
import time
import threading 
from midi_sender import capturadorMidi 

#Puerto UDP para descubrimiento
puertoUDP = 62001
peticion_descubrimiento = "DISCOVERY_REQUEST_ETHERIAVR"
respuesta_descubrimiento = json.dumps({"type": "DISCOVERY_RESPONSE", "server_name": "EtheriaVR Server"}).encode('utf-8')


def iniciar_procesamiento_en_tiempo_real():

    print("Iniciando procesamiento en tiempo real por medio de Socket UDP...")

    socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        socketUDP.bind(('0.0.0.0', puertoUDP))
        print(f"Socket UDP enlazado al puerto {puertoUDP} para descubrimiento.")
    except Exception as e:
        print(f"ERROR: No se pudo enlazar al puerto {puertoUDP}. {e}")
        return

 
    while True:
        try:
            data, direccion = socketUDP.recvfrom(1024)
            mensaje = data.decode('utf-8')
            
            if mensaje == peticion_descubrimiento:
                ipMetaQuest = direccion[0]
                
                print(f"Se recibió el mensaje de descubrimiento desde Meta quest con IP {ipMetaQuest}")
                
                socketUDP.sendto(respuesta_descubrimiento, direccion)
                print(f"Se envio la respuesta de descubrimiento a Meta Quest con IP {ipMetaQuest}")

                midiHilo = threading.Thread(target=capturadorMidi, args=(ipMetaQuest,), daemon=True)
                midiHilo.start()
                
                print(f"Hilo MIDI iniciado. Enviando datos a Meta Quest con IP: {ipMetaQuest}")
                

                socketUDP.close()
                return 

        except Exception as e:
            print(f"Error en el loop UDP: {e}")
            time.sleep(1)