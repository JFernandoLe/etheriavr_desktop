# EtheriaVR Desktop - Sistema de Captura MIDI

Cliente de escritorio para EtheriaVR que captura datos MIDI de instrumentos físicos y los envía en tiempo real al Meta Quest.

## 🚀 Descripción

Aplicación de escritorio que:
1. Descubre automáticamente el Meta Quest en la red local vía UDP
2. Captura eventos MIDI del instrumento conectado (piano, teclado, etc.)
3. Envía los datos MIDI en tiempo real al Quest para visualización en VR

## 📋 Requisitos

- Python 3.8+
- Instrumento MIDI conectado al PC (USB o MIDI tradicional)
- Meta Quest conectado a la misma red Wi-Fi
- Dependencias Python: `mido`, `python-rtmidi`

## 🔧 Instalación

```bash
# Instalar dependencias
pip install mido python-rtmidi
```

### En Windows
Si tienes problemas con `python-rtmidi`, instala:
```bash
pip install python-rtmidi-wheel
```

## ▶️ Ejecución

```bash
# Desde la carpeta etheriavr_desktop
cd etheriavr_desktop
python main.py
```

## 🎹 Conectar Instrumento MIDI

1. Conecta tu instrumento MIDI al PC (USB o interfaz MIDI)
2. Verifica que Windows lo reconoce en "Dispositivos y sonido"
3. Ejecuta el programa - detectará automáticamente el primer dispositivo MIDI

## 📡 Conexión con Meta Quest

1. Asegúrate de que el PC y el Meta Quest están en la misma red Wi-Fi
2. Ejecuta esta aplicación primero
3. Luego inicia la aplicación de EtheriaVR en el Quest
4. La conexión se establecerá automáticamente vía UDP

### Puertos utilizados:
- **62001**: Puerto UDP para descubrimiento del Quest
- **62002**: Puerto UDP para envío de datos MIDI

## 📁 Archivos

- `main.py` - Punto de entrada principal
- `main_realtime.py` - Manejo de conexión UDP y descubrimiento
- `midi_sender.py` - Captura y envío de eventos MIDI

## 🔍 Solución de Problemas

### "No se detectó ningún dispositivo MIDI conectado"
- Verifica que tu instrumento esté encendido y conectado
- Prueba con `python -c "import mido; print(mido.get_input_names())"`

### "No se pudo enlazar al puerto 62001"
- Otro programa está usando el puerto
- Cierra otras instancias de la aplicación
- Verifica con `netstat -ano | findstr 62001`

### El Quest no se conecta
- Verifica que ambos están en la misma red Wi-Fi
- Desactiva temporalmente el firewall de Windows
- Verifica que no hay VPN activa
