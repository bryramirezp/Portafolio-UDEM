#!/usr/bin/env python3
"""
Script interactivo para clasificar servicios en la nube.
Permite al usuario ingresar texto y ver la clasificación en tiempo real.
"""

from cloud_classifier import CloudServiceClassifier
import sys

def print_banner():
    """Imprime el banner del programa."""
    print("=" * 60)
    print("🌩️  CLASIFICADOR INTERACTIVO DE SERVICIOS EN LA NUBE 🌩️")
    print("=" * 60)
    print("Tipos de servicios que puede identificar:")
    print("• IaaS (Infrastructure as a Service)")
    print("• PaaS (Platform as a Service)")
    print("• SaaS (Software as a Service)")
    print("• FaaS (Function as a Service)")
    print("=" * 60)
    print("Comandos disponibles:")
    print("• 'salir' o 'exit' para terminar")
    print("• 'ayuda' o 'help' para mostrar esta información")
    print("• 'ejemplos' para ver ejemplos de clasificación")
    print("=" * 60)

def print_examples():
    """Muestra ejemplos de clasificación."""
    examples = [
        ("Amazon EC2 proporciona servidores virtuales en la nube", "IaaS"),
        ("Heroku es una plataforma de desarrollo para aplicaciones", "PaaS"),
        ("Salesforce es una aplicación CRM accesible desde el navegador", "SaaS"),
        ("AWS Lambda ejecuta funciones sin servidor basadas en eventos", "FaaS"),
        ("Microsoft Azure ofrece servicios de infraestructura en la nube", "IaaS"),
        ("Google App Engine proporciona un entorno de ejecución", "PaaS"),
        ("Office 365 es software como servicio para productividad", "SaaS"),
        ("Azure Functions permite crear funciones serverless", "FaaS")
    ]
    
    print("\n📋 EJEMPLOS DE CLASIFICACIÓN:")
    print("-" * 60)
    
    for i, (text, expected) in enumerate(examples, 1):
        print(f"{i}. Texto: {text}")
        print(f"   Esperado: {expected}")
        print()

def classify_text(classifier, text):
    """Clasifica un texto y muestra los resultados de forma formateada."""
    print(f"\n🔍 Analizando: '{text}'")
    print("-" * 50)
    
    result = classifier.classify(text)
    
    # Mostrar clasificación principal
    if result['is_cloud_service']:
        print(f"✅ CLASIFICACIÓN: {result['classification']}")
        print(f"📊 CONFIANZA: {result['confidence']}%")
    else:
        print("❌ NO CLASIFICADO COMO SERVICIO EN LA NUBE")
    
    # Mostrar puntajes detallados
    print(f"\n📈 PUNTAJES DETALLADOS:")
    scores = result['scores']
    for service_type, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        bar_length = int(score * 5)  # Escalar para visualización
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"   {service_type:4s}: {score:4.1f} {bar}")
    
    # Mostrar explicación
    explanation = classifier.get_explanation(result)
    print(f"\n💡 EXPLICACIÓN:")
    print(explanation)
    
    print("-" * 50)

def main():
    """Función principal del programa interactivo."""
    classifier = CloudServiceClassifier()
    
    print_banner()
    
    while True:
        try:
            # Obtener entrada del usuario
            user_input = input("\n🌩️  Ingrese texto para clasificar (o comando): ").strip()
            
            # Verificar comandos especiales
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego! Gracias por usar el clasificador.")
                break
            elif user_input.lower() in ['ayuda', 'help', 'h']:
                print_banner()
                continue
            elif user_input.lower() in ['ejemplos', 'examples', 'e']:
                print_examples()
                continue
            elif not user_input:
                print("⚠️  Por favor ingrese algún texto.")
                continue
            
            # Clasificar el texto
            classify_text(classifier, user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego! Gracias por usar el clasificador.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
