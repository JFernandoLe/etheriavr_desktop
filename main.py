"""
Punto de entrada principal del sistema de captura MIDI y envío en tiempo real a Meta Quest.
Este módulo se encarga de:
1. Descubrimiento del Meta Quest vía UDP
2. Captura de datos MIDI del instrumento conectado
3. Envío de eventos MIDI al Meta Quest en tiempo real
"""
from main_realtime import iniciar_procesamiento_en_tiempo_real


def main():
    """Inicia el procesamiento en tiempo real de MIDI"""
    print("=" * 60)
    print("EtheriaVR Desktop - Sistema de Captura MIDI")
    print("=" * 60)
    print("Esperando conexión del Meta Quest...")
    print("Asegúrate de que:")
    print("  1. El Meta Quest esté encendido")
    print("  2. Ambos dispositivos estén en la misma red Wi-Fi")
    print("  3. Tu instrumento MIDI esté conectado")
    print("=" * 60)
    
    try:
        iniciar_procesamiento_en_tiempo_real()
    except KeyboardInterrupt:
        print("\n\nSistema detenido por el usuario")
    except Exception as e:
        print(f"\n\nError: {e}")


if __name__ == "__main__":
    main()
