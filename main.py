"""
OdontoVoice Analytics - Sistema de Análisis de Transcripciones Telefónicas
Procesa y clasifica llamadas telefónicas en consultorios odontológicos
"""

import os
import json
import warnings
from pathlib import Path
from datetime import datetime

warnings.filterwarnings('ignore')

try:
    import speech_recognition as sr
    from pydub import AudioSegment
    import spacy
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import SVC
    import pickle
    import numpy as np
except ImportError as e:
    print(f"Error: Falta instalar {e}. Ejecuta: pip install -r requirements.txt")
    exit(1)


class OdontoVoiceAnalytics:
    """Sistema de análisis de transcripciones de llamadas odontológicas"""
    
    def __init__(self, model_path='models'):
        """Inicializa el sistema con modelos preentrenados"""
        self.model_path = Path(model_path)
        self.model_path.mkdir(exist_ok=True)
        
        # Palabras clave por categoría
        self.keywords = {
            'cita': ['agendar', 'cita', 'disponible', 'horario', 'reservar', 'fecha', 'día', 'hora'],
            'cancelación': ['cancelar', 'no puedo', 'reprogramar', 'cambiar', 'no voy', 'imposible'],
            'urgencia': ['emergencia', 'dolor', 'infección', 'urgente', 'rápido', 'ayuda', 'inmediato'],
            'consulta': ['información', 'consulta', 'pregunta', 'saber', 'costo', 'precio', 'tratamiento'],
            'queja': ['problema', 'queja', 'insatisfecho', 'malo', 'deficiente', 'servicio', 'atención'],
            'tratamiento': ['tratamiento', 'limpiar', 'diente', 'muela', 'procedimiento', 'endodoncia', 'ortodoncia']
        }
        
        self.recognizer = sr.Recognizer()
        self.vectorizer = None
        self.classifier = None
        self.nlp = None
        
        self._load_or_train_models()
    
    def _load_or_train_models(self):
        """Carga modelos existentes o entrena nuevos"""
        vec_path = self.model_path / 'vectorizer.pkl'
        clf_path = self.model_path / 'classifier.pkl'
        
        if vec_path.exists() and clf_path.exists():
            with open(vec_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            with open(clf_path, 'rb') as f:
                self.classifier = pickle.load(f)
            print("✓ Modelos cargados correctamente")
        else:
            self._train_models()
    
    def _train_models(self):
        """Entrena modelos SVM con datos de ejemplo"""
        # Datos de entrenamiento de ejemplo
        training_texts = [
            "Hola, quiero agendar una cita para limpiar los dientes",
            "Necesito una cita lo antes posible",
            "¿Cuáles son los horarios disponibles?",
            "Debo cancelar mi cita de mañana",
            "No puedo asistir al tratamiento",
            "Necesito reprogramar mi fecha",
            "Tengo un dolor de muela insoportable",
            "Es una emergencia, me duele mucho",
            "Necesito atención urgente ahora",
            "¿Cuál es el costo del tratamiento?",
            "¿Cuáles son los precios de los servicios?",
            "Tengo una pregunta sobre ortodoncia",
            "El servicio fue muy malo",
            "Tengo una queja sobre la atención recibida",
            "Insatisfecho con el procedimiento",
            "Necesito una endodoncia",
            "Quiero hacerme un blanqueamiento"
        ]
        
        labels = [
            'cita', 'cita', 'cita',
            'cancelación', 'cancelación', 'cancelación',
            'urgencia', 'urgencia', 'urgencia',
            'consulta', 'consulta', 'consulta',
            'queja', 'queja', 'queja',
            'tratamiento', 'tratamiento'
        ]
        
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='spanish', max_features=100)
        X = self.vectorizer.fit_transform(training_texts)
        
        self.classifier = SVC(kernel='linear', probability=True)
        self.classifier.fit(X, labels)
        
        # Guarda modelos entrenados
        with open(self.model_path / 'vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)
        with open(self.model_path / 'classifier.pkl', 'wb') as f:
            pickle.dump(self.classifier, f)
        
        print("✓ Modelos entrenados y guardados")
    
    def transcribe_audio(self, audio_path):
        """Transcribe un archivo de audio a texto"""
        try:
            if not Path(audio_path).exists():
                return None, "Archivo no encontrado"
            
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language='es-ES')
                return text, None
        except sr.UnknownValueError:
            return None, "No se pudo reconocer el audio"
        except sr.RequestError:
            return None, "Error de conexión con el servicio de reconocimiento"
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def classify_call(self, text):
        """Clasifica la intención de la llamada"""
        if not text or len(text) < 3:
            return 'sin_clasificar', 0.0, {}
        
        X = self.vectorizer.transform([text.lower()])
        prediction = self.classifier.predict(X)[0]
        probability = float(self.classifier.predict_proba(X).max())
        
        # Detección de urgencia
        urgency_level = self._detect_urgency(text)
        
        return prediction, probability, {'urgency_level': urgency_level}
    
    def _detect_urgency(self, text):
        """Detecta el nivel de urgencia según palabras clave"""
        text_lower = text.lower()
        urgency_keywords = ['emergencia', 'dolor', 'urgente', 'inmediato', 'ayuda', 'rápido']
        
        if any(keyword in text_lower for keyword in urgency_keywords):
            return 'Alta'
        elif any(keyword in text_lower for keyword in ['no puedo', 'mañana', 'próximo']):
            return 'Media'
        else:
            return 'Baja'
    
    def extract_entities(self, text):
        """Extrae entidades clave del texto"""
        entities = {
            'fecha': self._extract_dates(text),
            'contacto': self._extract_contact(text),
            'tratamiento': self._extract_treatment(text),
            'números': self._extract_numbers(text)
        }
        return entities
    
    def _extract_dates(self, text):
        """Extrae fechas mencionadas"""
        import re
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\b'
        ]
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
        return dates
    
    def _extract_contact(self, text):
        """Extrae información de contacto"""
        import re
        phones = re.findall(r'\b\d{7,10}\b', text)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        return {'teléfono': phones, 'email': emails}
    
    def _extract_treatment(self, text):
        """Extrae procedimientos mencionados"""
        treatments = ['endodoncia', 'ortodoncia', 'limpiar', 'blanqueamiento', 'implante', 'corona']
        found = [t for t in treatments if t in text.lower()]
        return found
    
    def _extract_numbers(self, text):
        """Extrae números (precios, documentos)"""
        import re
        return re.findall(r'\b\d+\b', text)
    
    def generate_summary(self, text, category):
        """Genera un resumen de la llamada"""
        return {
            'original_text': text[:200] + '...' if len(text) > 200 else text,
            'categoria': category,
            'timestamp': datetime.now().isoformat(),
            'longitud': len(text.split())
        }
    
    def process_call(self, audio_path=None, text=None):
        """Procesa una llamada completa"""
        if audio_path:
            text, error = self.transcribe_audio(audio_path)
            if error:
                return {'error': error, 'status': 'failed'}
        
        if not text:
            return {'error': 'No hay texto para procesar', 'status': 'failed'}
        
        category, confidence, metadata = self.classify_call(text)
        entities = self.extract_entities(text)
        summary = self.generate_summary(text, category)
        
        result = {
            'status': 'success',
            'transcription': text,
            'classification': {
                'category': category,
                'confidence': round(confidence, 3),
                'urgency_level': metadata['urgency_level']
            },
            'entities': entities,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        }
        
        return result


def main():
    """Función principal de demostración"""
    print("=" * 60)
    print("OdontoVoice Analytics - Sistema de Análisis de Llamadas")
    print("=" * 60)
    
    system = OdontoVoiceAnalytics()
    
    # Ejemplos de textos para procesar
    examples = [
        "Hola, quisiera agendar una cita para mañana si es posible",
        "Tengo un dolor de muela muy fuerte, es una emergencia",
        "Necesito cancelar mi cita del viernes",
        "¿Cuánto cuesta una limpieza dental?",
        "Estoy muy insatisfecho con el servicio recibido"
    ]
    
    print("\nProcesando ejemplos de llamadas...\n")
    
    results = []
    for i, example in enumerate(examples, 1):
        print(f"Ejemplo {i}: {example}")
        result = system.process_call(text=example)
        results.append(result)
        
        print(f"  Categoría: {result['classification']['category']}")
        print(f"  Confianza: {result['classification']['confidence']}")
        print(f"  Urgencia: {result['classification']['urgency_level']}")
        print(f"  Entidades encontradas: {result['entities']}\n")
    
    # Guarda resultados
    output_path = Path('resultados')
    output_path.mkdir(exist_ok=True)
    
    output_file = output_path / f"analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Resultados guardados en: {output_file}")


if __name__ == '__main__':
    main()
