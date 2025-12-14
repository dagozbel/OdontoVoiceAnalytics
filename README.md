# OdontoVoice Analytics

Sistema inteligente de análisis de transcripciones de llamadas telefónicas 
para consultorios odontológicos, basado en Procesamiento de Lenguaje Natural (PLN).

## Características Principales

**Transcripción de Audio**: Convierte archivos de audio (.wav, .mp3) a texto 
usando Google Speech Recognition

**Clasificación Inteligente**: Identifica automáticamente la intención de la llamada:
- Solicitud de cita
- Cancelación
- Emergencia/urgencia
- Consulta general
- Queja o reclamo
- Procedimiento específico

**Detección de Urgencia**: Clasifica el nivel de urgencia (Alta, Media, Baja)

**Extracción de Entidades**: Detecta automáticamente:
- Fechas mencionadas
- Números de teléfono
- Tratamientos solicitados
- Información de contacto

**Generación de Reportes**: Crea reportes JSON con análisis completo

## Requisitos

- Python 3.8+
- Sistema operativo: Windows, macOS, Linux

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/dagozbel/OdontoVoiceAnalytics.git
cd OdontoVoice-Analytics
```

### 2. Crear un entorno virtual
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Uso

### Opción 1: Procesar texto directo
```python
from main import OdontoVoiceAnalytics

sistema = OdontoVoiceAnalytics()
texto = "Hola, quisiera agendar una cita para mañana"
resultado = sistema.process_call(text=texto)
print(resultado)
```

### Opción 2: Procesar archivo de audio
```python
from main import OdontoVoiceAnalytics

sistema = OdontoVoiceAnalytics()
resultado = sistema.process_call(audio_path="llamada.wav")
print(resultado)
```

### Opción 3: Ejecutar desde terminal
```bash
python main.py
```

Esto ejecutará ejemplos de demostración y guardará resultados en `resultados/`

## Estructura de Resultados
```json
{
  "status": "success",
  "transcription": "texto transcrito...",
  "classification": {
    "category": "cita",
    "confidence": 0.95,
    "urgency_level": "Baja"
  },
  "entities": {
    "fecha": ["15/12/2025"],
    "contacto": {
      "teléfono": ["3105551234"],
      "email": []
    },
    "tratamiento": [],
    "números": []
  }
}
```

## Categorías de Clasificación

| Categoría | Palabras Clave | Urgencia |
|-----------|---|---|
| **cita** | agendar, reservar, disponible | Baja |
| **cancelación** | cancelar, reprogramar, cambiar | Media |
| **urgencia** | emergencia, dolor, inmediato | Alta |
| **consulta** | información, pregunta, costo | Baja |
| **queja** | problema, insatisfecho, deficiente | Media |
| **tratamiento** | endodoncia, ortodoncia, limpiar | Baja |

## Estructura del Proyecto
```
OdontoVoice-Analytics/
├── main.py                 # Archivo principal
├── README.md              # Este archivo
├── models/                # Modelos (se crean automáticamente)
├── resultados/            # Reportes generados
└── ejemplo_uso.py         # Ejemplos
```
## Archivos de Audio Soportados

- .wav
- .mp3
- .flac
- .ogg

## Autor

**Diego Alberto Ortiz Beltrán**
Ingeniería en Ciencias de Datos - Corporación Universitaria Iberoamericana
