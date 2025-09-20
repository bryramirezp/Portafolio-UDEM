#!/usr/bin/env python3
"""
Script de prueba para el clasificador de servicios en la nube.
Demuestra diferentes casos de uso y escenarios de clasificación.
"""

from cloud_classifier import CloudServiceClassifier
import json

def test_basic_classification():
    """Prueba la clasificación básica con ejemplos simples."""
    print("🧪 PRUEBA 1: Clasificación Básica")
    print("=" * 50)
    
    classifier = CloudServiceClassifier()
    
    test_cases = [
        "Amazon EC2 es un servicio de infraestructura como servicio",
        "Google App Engine es una plataforma como servicio para desarrollo",
        "Salesforce es software como servicio para gestión de clientes",
        "AWS Lambda es función como servicio sin servidor"
    ]
    
    for i, text in enumerate(test_cases, 1):
        result = classifier.classify(text)
        print(f"{i}. Texto: {text}")
        print(f"   Clasificación: {result['classification']}")
        print(f"   Confianza: {result['confidence']}%")
        print()

def test_complex_texts():
    """Prueba con textos más complejos y realistas."""
    print("🧪 PRUEBA 2: Textos Complejos")
    print("=" * 50)
    
    classifier = CloudServiceClassifier()
    
    complex_cases = [
        {
            "text": "Microsoft Azure Virtual Machines proporciona instancias de computación escalables con diferentes configuraciones de CPU, RAM y almacenamiento SSD. Los usuarios pueden crear máquinas virtuales Windows o Linux según sus necesidades.",
            "expected": "IaaS"
        },
        {
            "text": "Heroku es una plataforma de desarrollo que permite a los desarrolladores desplegar aplicaciones web de forma automática. Incluye herramientas de CI/CD, monitoreo y escalado automático sin necesidad de gestionar la infraestructura subyacente.",
            "expected": "PaaS"
        },
        {
            "text": "Office 365 es una suite de aplicaciones de productividad que incluye Word, Excel, PowerPoint y Outlook. Los usuarios acceden a través del navegador web con una suscripción mensual o anual, sin necesidad de instalar software localmente.",
            "expected": "SaaS"
        },
        {
            "text": "Google Cloud Functions permite ejecutar código en respuesta a eventos como cambios en Cloud Storage, mensajes de Pub/Sub o solicitudes HTTP. Es un servicio serverless que escala automáticamente y solo cobra por el tiempo de ejecución.",
            "expected": "FaaS"
        }
    ]
    
    for i, case in enumerate(complex_cases, 1):
        result = classifier.classify(case["text"])
        correct = result['classification'] == case['expected']
        status = "✅" if correct else "❌"
        
        print(f"{i}. {status} Texto: {case['text'][:80]}...")
        print(f"   Esperado: {case['expected']}")
        print(f"   Obtenido: {result['classification']}")
        print(f"   Confianza: {result['confidence']}%")
        print()

def test_edge_cases():
    """Prueba casos límite y textos ambiguos."""
    print("🧪 PRUEBA 3: Casos Límite")
    print("=" * 50)
    
    classifier = CloudServiceClassifier()
    
    edge_cases = [
        "Este es un texto sobre cocina que no tiene nada que ver con la nube",
        "La nube es un concepto meteorológico que describe la acumulación de vapor de agua",
        "AWS ofrece múltiples servicios incluyendo EC2, Lambda y S3",
        "El desarrollo de software moderno utiliza herramientas en la nube",
        "Los servidores físicos son diferentes a los servicios en la nube"
    ]
    
    for i, text in enumerate(edge_cases, 1):
        result = classifier.classify(text)
        print(f"{i}. Texto: {text}")
        print(f"   Clasificación: {result['classification']}")
        print(f"   Es servicio en la nube: {result['is_cloud_service']}")
        print(f"   Confianza: {result['confidence']}%")
        print()

def test_multilingual():
    """Prueba clasificación en diferentes idiomas."""
    print("🧪 PRUEBA 4: Clasificación Multilingüe")
    print("=" * 50)
    
    classifier = CloudServiceClassifier()
    
    multilingual_cases = [
        ("Amazon EC2 provides virtual servers in the cloud", "IaaS"),
        ("Heroku is a development platform for deploying applications", "PaaS"),
        ("Salesforce is a CRM application accessible via web browser", "SaaS"),
        ("AWS Lambda executes serverless functions based on events", "FaaS"),
        ("Azure VM ofrece máquinas virtuales con CPU y RAM configurables", "IaaS"),
        ("Google App Engine proporciona un entorno de ejecución", "PaaS"),
        ("Office 365 es software como servicio para productividad", "SaaS"),
        ("Azure Functions permite crear funciones serverless", "FaaS")
    ]
    
    for i, (text, expected) in enumerate(multilingual_cases, 1):
        result = classifier.classify(text)
        correct = result['classification'] == expected
        status = "✅" if correct else "❌"
        
        print(f"{i}. {status} Texto: {text}")
        print(f"   Esperado: {expected}")
        print(f"   Obtenido: {result['classification']}")
        print(f"   Confianza: {result['confidence']}%")
        print()

def test_performance():
    """Prueba el rendimiento con múltiples clasificaciones."""
    print("🧪 PRUEBA 5: Rendimiento")
    print("=" * 50)
    
    import time
    
    classifier = CloudServiceClassifier()
    
    # Texto de prueba
    test_text = "Amazon EC2 proporciona servidores virtuales en la nube con CPU, RAM y almacenamiento configurables"
    
    # Medir tiempo de clasificación
    start_time = time.time()
    for _ in range(1000):
        result = classifier.classify(test_text)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time / 1000 * 1000  # Convertir a milisegundos
    
    print(f"Tiempo total para 1000 clasificaciones: {total_time:.3f} segundos")
    print(f"Tiempo promedio por clasificación: {avg_time:.3f} ms")
    print(f"Última clasificación: {result['classification']} ({result['confidence']}%)")

def export_results():
    """Exporta los resultados de clasificación a JSON."""
    print("🧪 PRUEBA 6: Exportación de Resultados")
    print("=" * 50)
    
    classifier = CloudServiceClassifier()
    
    test_texts = [
        "Amazon EC2 proporciona servidores virtuales",
        "Heroku es una plataforma de desarrollo",
        "Salesforce es una aplicación CRM",
        "AWS Lambda ejecuta funciones serverless"
    ]
    
    results = []
    for text in test_texts:
        result = classifier.classify(text)
        results.append({
            "text": text,
            "classification": result['classification'],
            "confidence": result['confidence'],
            "scores": result['scores'],
            "is_cloud_service": result['is_cloud_service']
        })
    
    # Guardar resultados en archivo JSON
    with open('classification_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resultados exportados a 'classification_results.json'")
    print(f"📊 Total de clasificaciones: {len(results)}")
    
    # Mostrar resumen
    for result in results:
        print(f"• {result['classification']}: {result['confidence']}%")

def main():
    """Ejecuta todas las pruebas."""
    print("🚀 INICIANDO PRUEBAS DEL CLASIFICADOR DE SERVICIOS EN LA NUBE")
    print("=" * 70)
    
    test_basic_classification()
    test_complex_texts()
    test_edge_cases()
    test_multilingual()
    test_performance()
    export_results()
    
    print("\n🎉 ¡Todas las pruebas completadas!")
    print("=" * 70)

if __name__ == "__main__":
    main()
