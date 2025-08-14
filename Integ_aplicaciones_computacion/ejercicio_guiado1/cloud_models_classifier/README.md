# Clasificador de Servicios en la Nube

Este proyecto implementa un clasificador basado en reglas que identifica si un texto corresponde a uno de los cuatro tipos principales de servicios en la nube:

- **IaaS** (Infrastructure as a Service)
- **PaaS** (Platform as a Service) 
- **SaaS** (Software as a Service)
- **FaaS** (Function as a Service)

## Características

- Clasificación basada en palabras clave y patrones regex
- Soporte para texto en español e inglés
- Cálculo de puntajes de confianza
- Explicaciones detalladas de la clasificación
- Preprocesamiento de texto automático

## Uso

### Ejecución básica

```python
from cloud_classifier import CloudServiceClassifier

# Crear instancia del clasificador
classifier = CloudServiceClassifier()

# Clasificar un texto
texto = "Amazon EC2 proporciona servidores virtuales en la nube"
resultado = classifier.classify(texto)

print(f"Clasificación: {resultado['classification']}")
print(f"Confianza: {resultado['confidence']}%")
```

### Ejecutar ejemplos

```bash
python cloud_classifier.py
```

## Ejemplos de clasificación

### IaaS (Infrastructure as a Service)
- "Amazon EC2 proporciona servidores virtuales en la nube"
- "Azure VM ofrece instancias de computación con CPU y RAM configurables"
- "Google Compute Engine permite crear máquinas virtuales"

### PaaS (Platform as a Service)
- "Heroku es una plataforma de desarrollo para desplegar aplicaciones"
- "Google App Engine proporciona un entorno de ejecución para aplicaciones"
- "Azure App Service permite el despliegue automático de aplicaciones"

### SaaS (Software as a Service)
- "Salesforce es una aplicación CRM accesible desde el navegador"
- "Office 365 es software como servicio para productividad"
- "Dropbox es una aplicación web para almacenamiento en la nube"

### FaaS (Function as a Service)
- "AWS Lambda ejecuta funciones sin servidor basadas en eventos"
- "Azure Functions permite crear funciones serverless"
- "Google Cloud Functions ejecuta código en respuesta a eventos"

## Estructura del código

### Clase CloudServiceClassifier

- **`__init__()`**: Inicializa palabras clave y patrones para cada tipo de servicio
- **`preprocess_text(text)`**: Preprocesa el texto para mejorar la clasificación
- **`calculate_score(text, service_type)`**: Calcula el puntaje para un tipo de servicio
- **`classify(text)`**: Clasifica el texto y retorna el resultado
- **`get_explanation(result)`**: Genera una explicación de la clasificación

### Resultado de clasificación

El método `classify()` retorna un diccionario con:

```python
{
    'text': 'texto original',
    'classification': 'IaaS|PaaS|SaaS|FaaS|No clasificado',
    'confidence': 85.5,  # Porcentaje de confianza
    'scores': {          # Puntajes por tipo de servicio
        'IaaS': 5.0,
        'PaaS': 2.0,
        'SaaS': 1.0,
        'FaaS': 0.0
    },
    'is_cloud_service': True  # Si se detectó como servicio en la nube
}
```

## Algoritmo de clasificación

1. **Preprocesamiento**: El texto se convierte a minúsculas y se normaliza
2. **Búsqueda de palabras clave**: Se buscan términos específicos para cada tipo de servicio
3. **Análisis de patrones**: Se aplican expresiones regulares para detectar frases específicas
4. **Cálculo de puntajes**: Se asignan puntajes basados en coincidencias encontradas
5. **Clasificación**: Se selecciona el tipo con mayor puntaje
6. **Cálculo de confianza**: Se determina el nivel de confianza basado en la distribución de puntajes

## Requisitos

- Python 3.6+
- No se requieren dependencias externas (solo módulos estándar de Python)

## Limitaciones

- Clasificación basada en reglas simples, no en machine learning
- Puede tener falsos positivos con textos que contengan palabras clave sin ser servicios en la nube
- La precisión depende de la calidad y cobertura de las palabras clave definidas
- No considera el contexto semántico completo del texto

## Mejoras futuras

- Integración con modelos de machine learning
- Análisis de sentimientos y contexto
- Base de datos de ejemplos para entrenamiento
- API REST para uso web
- Interfaz gráfica de usuario
