import socket
import json
import time
import threading
import sounddevice as sd

# ========= CONFIGURACIÓN DE DESCUBRIMIENTO =========
# Puerto UDP para descubrimiento - DEBE coincidir con el de NetworkConfig.cs del Quest
PUERTO_DESCUBRIMIENTO = 8888
# Mensaje que envía el Quest 3 para descubrir servidores
PETICION_DESCUBRIMIENTO = "ETHERIA_SEARCH"
# Formato de respuesta que el Quest espera: "ETHERIA_SERVER_HERE:IP:PUERTO"
SERVER_IDENTIFIER = "ETHERIA_SERVER_HERE"

# Puerto donde corre el backend (API REST) - se lo decimos al Quest
BACKEND_API_PORT = 8000

# Puerto al que enviaremos datos de voz - el Quest escucha en 12345
PUERTO_VOZ = 12345


def get_all_local_ips():
    """Obtiene todas las IPs locales de todas las interfaces de red"""
    ips = []
    try:
        hostname = socket.gethostname()
        addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET)
        for info in addr_info:
            ip = info[4][0]
            if ip not in ips and not ip.startswith('127.'):
                ips.append(ip)
    except Exception as e:
        print(f"[!] Error obteniendo IPs: {e}")
    return ips


def get_matching_ip(client_addr, available_ips):
    """Encuentra la IP del servidor en la misma subred que el cliente"""
    try:
        client_subnet = '.'.join(client_addr.split('.')[:3])
        for ip in available_ips:
            server_subnet = '.'.join(ip.split('.')[:3])
            if client_subnet == server_subnet:
                return ip
        return available_ips[0] if available_ips else "127.0.0.1"
    except:
        return available_ips[0] if available_ips else "127.0.0.1"


def seleccionar_microfono():
    """Muestra los micrófonos disponibles y pide al usuario seleccionar uno"""
    print("\n" + "=" * 60)
    print("🎤 SELECCIÓN DE MICRÓFONO")
    print("=" * 60)
    
    dispositivos = sd.query_devices()
    dispositivos_mic = []
    
    print("\nMicrófonos disponibles:")
    print("-" * 60)
    
    for i, dispositivo in enumerate(dispositivos):
        if dispositivo['max_input_channels'] > 0:
            dispositivos_mic.append(i)
            nombre = dispositivo['name']
            print(f"  [{len(dispositivos_mic) - 1}] {nombre}")
    
    if not dispositivos_mic:
        print("\n❌ No se detectaron micrófonos en el sistema.")
        return None
    
    print("-" * 60)
    
    while True:
        try:
            seleccion = input(f"\nSelecciona el número del micrófono a usar [0-{len(dispositivos_mic) - 1}]: ").strip()
            indice = int(seleccion)
            if 0 <= indice < len(dispositivos_mic):
                indice_real = dispositivos_mic[indice]
                nombre = dispositivos[indice_real]['name']
                print(f"✅ Micrófono seleccionado: {nombre} (índice {indice_real})")
                return indice_real
            else:
                print(f"⛔ Número fuera de rango. Intenta de 0 a {len(dispositivos_mic) - 1}.")
        except ValueError:
            print("⛔ Ingresa un número válido.")
        except KeyboardInterrupt:
            print("\n\nSaliendo...")
            return None


def iniciar_procesamiento_en_tiempo_real():
    
    print("=" * 60)
    print("EtheriaVR Desktop - Sistema de Canto en Tiempo Real")
    print("=" * 60)
    
    # --- Seleccionar micrófono ---
    indice_mic = seleccionar_microfono()
    if indice_mic is None:
        return
    
    print("\n" + "=" * 60)
    print("📡 Esperando señal de descubrimiento del Meta Quest 3...")
    print(f"   Puerto UDP: {PUERTO_DESCUBRIMIENTO}")
    print(f"   Asegúrate de:")
    print(f"     1. El Meta Quest esté encendido y en la app de EtheriaVR")
    print(f"     2. Ambos dispositivos estén en la misma red Wi-Fi")
    print("=" * 60)

    socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        socketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketUDP.settimeout(1.0)
        socketUDP.bind(('0.0.0.0', PUERTO_DESCUBRIMIENTO))
        print(f"✅ Socket UDP enlazado al puerto {PUERTO_DESCUBRIMIENTO} para descubrimiento.")

        # Mostrar las IPs locales disponibles
        local_ips = get_all_local_ips()
        print(f"[*] Interfaces de red detectadas:")
        for ip in local_ips:
            print(f"    - {ip}")

    except Exception as e:
        print(f"❌ ERROR: No se pudo enlazar al puerto {PUERTO_DESCUBRIMIENTO}.")
        print(f"   {e}")
        print("   Posible causa: el backend ya está usando ese puerto.")
        print("   Sugerencia: Detén el backend o cambia el UDP_PORT en su .env")
        return

    quest_detectado = False
    
    while True:
        try:
            data, direccion = socketUDP.recvfrom(1024)
            mensaje = data.decode('utf-8')

            print(f"📩 Recibido mensaje desde {direccion[0]}: {mensaje}")

            if mensaje == PETICION_DESCUBRIMIENTO:
                ipMetaQuest = direccion[0]

                # Encontrar la IP local que coincide con la subred del Quest
                local_ips = get_all_local_ips()
                local_ip = get_matching_ip(ipMetaQuest, local_ips)

                # Responder en el formato que el Quest espera (NetworkConfig.cs)
                respuesta = f"{SERVER_IDENTIFIER}:{local_ip}:{BACKEND_API_PORT}"
                socketUDP.sendto(respuesta.encode('utf-8'), direccion)
                print(f"✅ Respondido a Meta Quest {ipMetaQuest}: {respuesta}")

                if not quest_detectado:
                    quest_detectado = True
                    
                    print("\n" + "=" * 60)
                    print(f"🎤 INICIANDO CAPTURA DE VOZ")
                    print(f"   Quest IP: {ipMetaQuest}")
                    print(f"   Puerto voz: {PUERTO_VOZ}")
                    print("=" * 60)
                    
                                                            
                    # Iniciar VocalManager (canto) con la IP del Quest
                    from services.vocal_service import VocalManager
                    vocal = VocalManager(quest_ip=ipMetaQuest, port=PUERTO_VOZ, device_index=indice_mic)
                    hilo_voz = threading.Thread(target=vocal.start_processing, daemon=True)
                    hilo_voz.start()

            else:
                print(f"⚠️ Mensaje desconocido desde {direccion[0]}: {mensaje}")

        except socket.timeout:
            continue
        except KeyboardInterrupt:
            print("\n\n👋 Sistema detenido por el usuario.")
            break
        except Exception as e:
            print(f"Error en el loop UDP: {e}")
            time.sleep(1)

    socketUDP.close()