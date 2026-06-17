"""
Punto de entrada principal del sistema de captura de voz y envío en tiempo real a Meta Quest.
Este módulo se encarga de:
1. Selección del micrófono a usar
2. Descubrimiento del Meta Quest vía UDP (puerto 8888)
3. Captura de voz y detección de tono (YIN)
4. Envío de datos de voz al Meta Quest en tiempo real
"""
from main_realtime import iniciar_procesamiento_en_tiempo_real


def main():
    """Inicia el procesamiento en tiempo real de voz"""
    print("=" * 60)
    print("EtheriaVR Desktop - Sistema de Canto en Tiempo Real")
    print("=" * 60)
    
    try:
        iniciar_procesamiento_en_tiempo_real()
    except KeyboardInterrupt:
        print("\n\nSistema detenido por el usuario")
    except Exception as e:
        print(f"\n\nError: {e}")


if __name__ == "__main__":
    main()
