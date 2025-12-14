"""
Ejemplos de uso de OdontoVoice Analytics
Demuestra las diferentes formas de usar el sistema
"""

from main import OdontoVoiceAnalytics
import json
from pathlib import Path


def ejemplo_1_analisis_basico():
    """Ejemplo 1: Análisis básico de un texto"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Análisis Básico")
    print("="*60)
    
    sistema = OdontoVoiceAnalytics()
    
    textos = [
        "Hola, quisiera agendar una cita para limpiarme los dientes",
        "Tengo un dolor muy fuerte en la muela, es una emergencia",
        "Necesito cancelar mi cita de mañana"
    ]
    
    for texto in textos:
        print(f"\nTexto: {texto}")
        resultado = sistema.process_call(text=texto)
        
        print(f"  ✓ Categoría: {resultado['classification']['category']}")
        print(f"  ✓ Confianza: {resultado['classification']['confidence']}")
        print(f"  ✓ Urgencia: {resultado['classification']['urgency_level']}")


def ejemplo_2_extraccion_entidades():
    """Ejemplo 2: Extracción de entidades"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Extracción de Entidades")
    print("="*60)
    
    sistema = OdontoVoiceAnalytics()
    
    texto = "Quiero una cita el 15 de diciembre a las 3 de la tarde, mi teléfono es 3105551234"
    print(f"\nTexto: {texto}")
    
    entidades = sistema.extract_entities(texto)
    
    print("\nEntidades extraídas:")
    print(f"  • Fechas: {entidades['fecha']}")
    print(f"  • Contacto: {entidades['contacto']}")
    print(f"  • Tratamientos: {entidades['tratamiento']}")
    print(f"  • Números: {entidades['números']}")


def ejemplo_3_clasificacion_detallada():
    """Ejemplo 3: Clasificación con análisis detallado"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Clasificación Detallada")
    print("="*60)
    
    sistema = OdontoVoiceAnalytics()
    
    ejemplos = {
        "Cita": "Necesito agendar una cita lo antes posible",
        "Cancelación": "Lamentablemente debo cancelar mi cita",
        "Urgencia": "¡Ayuda! Tengo un dolor de muela insoportable",
        "Consulta": "¿Cuál es el precio de una endodoncia?",
        "Queja": "El servicio que recibí fue muy malo",
        "Tratamiento": "Quiero hacerme un blanqueamiento dental"
    }
    
    for tipo, texto in ejemplos.items():
        categoria, confianza, metadata = sistema.classify_call(texto)
        
        print(f"\n{tipo}:")
        print(f"  Texto: '{texto}'")
        print(f"  Resultado: {categoria} (confianza: {confianza:.2%})")
        print(f"  Urgencia: {metadata['urgency_level']}")


def ejemplo_4_procesamiento_lotes():
    """Ejemplo 4: Procesamiento de múltiples llamadas (batch)"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Procesamiento en Lotes")
    print("="*60)
    
    sistema = OdontoVoiceAnalytics()
    
    llamadas = [
        "Hola, quiero hacer una cita",
        "Necesito cancelar para mañana",
        "Tengo una emergencia dental",
        "¿Qué tratamientos ofrecen?",
        "Estoy insatisfecho con el servicio"
    ]
    
    print(f"\nProcesando {len(llamadas)} llamadas...\n")
    
    resultados = []
    for i, texto in enumerate(llamadas, 1):
        resultado = sistema.process_call(text=texto)
        resultados.append(resultado)
        
        print(f"{i}. {texto}")
        print(f"   → {resultado['classification']['category']} "
              f"({resultado['classification']['confidence']:.1%})")
    
    return resultados


def ejemplo_5_generar_reporte():
    """Ejemplo 5: Generar reporte de análisis"""
    print("\n" + "="*60)
    print("EJEMPLO 5: Generar Reporte")
    print("="*60)
    
    sistema = OdontoVoiceAnalytics()
    
    # Procesar múltiples llamadas
    textos = [
        "Quisiera agendar una cita",
        "Tengo un dolor urgente",
        "Necesito cancelar",
        "¿Cuánto cuesta?",
        "Mala atención"
    ]
    
    resultados = []
    for texto in textos:
        resultado = sistema.process_call(text=texto)
        resultados.append(resultado)
    
    # Crear reporte
    reporte = {
        'total_llamadas': len(resultados),
        'timestamp': resultados[0]['timestamp'] if resultados else None,
        'resumen_categorias': {},
        'urgencias': {},
        'llamadas': resultados
    }
    
    # Contar categorías y urgencias
    for resultado in resultados:
        cat = resultado['classification']['category']
        urgencia = resultado['classification']['urgency_level']
        
        reporte['resumen_categorias'][cat] = reporte['resumen_categorias'].get(cat, 0) + 1
        reporte['urgencias'][urgencia] = reporte['urgencias'].get(urgencia, 0) + 1
    
    print("\nReporte de Análisis:")
    print(f"  Total de llamadas: {reporte['total_llamadas']}")
    print(f"\n  Distribuición por categoría:")
    for cat, count in reporte['resumen_categorias'].items():
        print(f"    - {cat}: {count}")
    
    print(f"\n  Distribuición por urgencia:")
    for urgencia, count in reporte['urgencias'].items():
        print(f"    - {urgencia}: {count}")
    
    # Guardar reporte
    output_path = Path('resultados') / 'reporte_ejemplo.json'
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Reporte guardado en: {output_path}")


def ejemplo_6_deteccion_urgencia():
    """Ejemplo 6: Detección de niveles de urgencia"""
    print("\n" + "="*60)
    print("EJEMPLO 6: Detección de Urgencia")
    print("="*60)
    
    sistema = OdontoVoiceAnalytics()
    
    casos = [
        ("Urgencia Alta", "Tengo una emergencia, dolor insoportable, ayuda"),
        ("Urgencia Media", "Necesito reprogramar mi cita de mañana"),
        ("Urgencia Baja", "Quiero información sobre nuestros servicios"),
    ]
    
    for tipo, texto in casos:
        _, _, metadata = sistema.classify_call(texto)
        print(f"\n{tipo}:")
        print(f"  Texto: '{texto}'")
        print(f"  Nivel: {metadata['urgency_level']}")


def main():
    """Ejecuta todos los ejemplos"""
    print("\n" + "#"*60)
    print("# OdontoVoice Analytics - Ejemplos de Uso")
    print("#"*60)
    
    try:
        ejemplo_1_analisis_basico()
        ejemplo_2_extraccion_entidades()
        ejemplo_3_clasificacion_detallada()
        ejemplo_4_procesamiento_lotes()
        ejemplo_5_generar_reporte()
        ejemplo_6_deteccion_urgencia()
        
        print("\n" + "#"*60)
        print("# ✓ Todos los ejemplos ejecutados correctamente")
        print("#"*60)
        
    except Exception as e:
        print(f"\n✗ Error durante la ejecución: {e}")
        print("\nAsegúrate de haber ejecutado: pip install -r requirements.txt")


if __name__ == '__main__':
    main()
