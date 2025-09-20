import re
from typing import Dict, List, Tuple

class CloudServiceClassifier:
    """
    Clasificador de servicios en la nube basado en reglas.
    Identifica si un texto corresponde a IaaS, PaaS, SaaS o FaaS.
    """
    
    def __init__(self):
        # Definir palabras clave para cada tipo de servicio
        self.keywords = {
            'IaaS': [
                'infraestructura como servicio', 'infrastructure as a service',
                'servidor virtual', 'virtual server', 'vm', 'virtual machine',
                'almacenamiento', 'storage', 'red', 'network', 'computación',
                'cpu', 'ram', 'disco duro', 'hard disk', 'load balancer',
                'firewall', 'vpc', 'virtual private cloud', 'instancia',
                'ec2', 'azure vm', 'google compute engine', 'openstack'
            ],
            'PaaS': [
                'plataforma como servicio', 'platform as a service',
                'desarrollo', 'development', 'deployment', 'despliegue',
                'runtime', 'entorno de ejecución', 'middleware', 'framework',
                'app engine', 'elastic beanstalk', 'heroku', 'openshift',
                'build', 'compilación', 'testing', 'pruebas', 'ci/cd',
                'continuous integration', 'integración continua'
            ],
            'SaaS': [
                'software como servicio', 'software as a service',
                'aplicación', 'application', 'app', 'usuario final',
                'end user', 'interfaz', 'interface', 'dashboard', 'panel',
                'crm', 'erp', 'office 365', 'google workspace', 'salesforce',
                'dropbox', 'slack', 'zoom', 'web app', 'aplicación web',
                'subscription', 'suscripción', 'licencia'
            ],
            'FaaS': [
                'función como servicio', 'function as a service',
                'serverless', 'sin servidor', 'lambda', 'azure functions',
                'google cloud functions', 'event-driven', 'evento',
                'trigger', 'disparador', 'microservicio', 'microservice',
                'api', 'webhook', 'cron', 'scheduled', 'programado',
                'stateless', 'sin estado', 'ephemeral', 'efímero'
            ]
        }
        
        # Definir patrones específicos para cada servicio
        self.patterns = {
            'IaaS': [
                r'\b(proveedor|provider)\s+(de\s+)?(infraestructura|infrastructure)\b',
                r'\b(servidor|server)\s+(virtual|dedicado|dedicated)\b',
                r'\b(instancia|instance)\s+(de\s+)?(computación|compute)\b',
                r'\b(almacenamiento|storage)\s+(en\s+)?(la\s+)?nube\b',
                r'\b(red|network)\s+(virtual|virtualizada)\b'
            ],
            'PaaS': [
                r'\b(plataforma|platform)\s+(de\s+)?(desarrollo|development)\b',
                r'\b(entorno|environment)\s+(de\s+)?(ejecución|runtime)\b',
                r'\b(despliegue|deployment)\s+(automático|automatic)\b',
                r'\b(integración|integration)\s+(continua|continuous)\b',
                r'\b(build|compilación)\s+(automático|automatic)\b'
            ],
            'SaaS': [
                r'\b(aplicación|application)\s+(web|online|en\s+la\s+nube)\b',
                r'\b(software|programa)\s+(como\s+)?servicio\b',
                r'\b(usuario|user)\s+(final|end)\b',
                r'\b(suscripción|subscription)\s+(mensual|monthly|anual|yearly)\b',
                r'\b(interfaz|interface)\s+(de\s+)?usuario\b'
            ],
            'FaaS': [
                r'\b(función|function)\s+(como\s+)?servicio\b',
                r'\b(serverless|sin\s+servidor)\b',
                r'\b(evento|event)\s+(driven|dirigido)\b',
                r'\b(trigger|disparador)\s+(de\s+)?eventos\b',
                r'\b(microservicio|microservice)\s+(sin\s+estado|stateless)\b'
            ]
        }
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocesa el texto para mejorar la clasificación.
        """
        # Convertir a minúsculas
        text = text.lower()
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        # Remover caracteres especiales pero mantener acentos
        text = re.sub(r'[^\w\sáéíóúñü]', ' ', text)
        return text.strip()
    
    def calculate_score(self, text: str, service_type: str) -> float:
        """
        Calcula el puntaje para un tipo de servicio basado en palabras clave y patrones.
        """
        score = 0.0
        
        # Buscar palabras clave
        for keyword in self.keywords[service_type]:
            if keyword in text:
                score += 1.0
        
        # Buscar patrones específicos
        for pattern in self.patterns[service_type]:
            matches = re.findall(pattern, text, re.IGNORECASE)
            score += len(matches) * 2.0  # Los patrones tienen más peso
        
        return score
    
    def classify(self, text: str) -> Dict[str, any]:
        """
        Clasifica el texto y retorna el resultado con puntajes.
        """
        # Preprocesar el texto
        processed_text = self.preprocess_text(text)
        
        # Calcular puntajes para cada tipo de servicio
        scores = {}
        for service_type in self.keywords.keys():
            scores[service_type] = self.calculate_score(processed_text, service_type)
        
        # Encontrar el servicio con mayor puntaje
        best_service = max(scores, key=scores.get)
        max_score = scores[best_service]
        
        # Determinar confianza
        total_score = sum(scores.values())
        confidence = (max_score / total_score * 100) if total_score > 0 else 0
        
        # Determinar si hay suficiente evidencia
        is_cloud_service = max_score > 0
        
        return {
            'text': text,
            'classification': best_service if is_cloud_service else 'No clasificado',
            'confidence': round(confidence, 2),
            'scores': scores,
            'is_cloud_service': is_cloud_service
        }
    
    def get_explanation(self, result: Dict[str, any]) -> str:
        """
        Genera una explicación de la clasificación.
        """
        if not result['is_cloud_service']:
            return "El texto no contiene suficientes indicadores para clasificarlo como un servicio en la nube."
        
        service = result['classification']
        confidence = result['confidence']
        scores = result['scores']
        
        explanation = f"Clasificado como {service} con {confidence}% de confianza.\n\n"
        explanation += "Puntajes por tipo de servicio:\n"
        
        for service_type, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            explanation += f"- {service_type}: {score}\n"
        
        return explanation


def main():
    """
    Función principal para demostrar el uso del clasificador.
    """
    classifier = CloudServiceClassifier()
    
    # Ejemplos de texto para clasificar
    examples = [
        "Amazon EC2 proporciona servidores virtuales en la nube con CPU, RAM y almacenamiento configurables",
        "Heroku es una plataforma de desarrollo que permite desplegar aplicaciones web fácilmente",
        "Salesforce es una aplicación CRM que se accede a través del navegador web",
        "AWS Lambda permite ejecutar funciones sin servidor basadas en eventos",
        "Este es un texto sobre cocina que no tiene nada que ver con servicios en la nube"
    ]
    
    print("=== Clasificador de Servicios en la Nube ===\n")
    
    for i, example in enumerate(examples, 1):
        print(f"Ejemplo {i}:")
        print(f"Texto: {example}")
        
        result = classifier.classify(example)
        explanation = classifier.get_explanation(result)
        
        print(f"Resultado: {result['classification']}")
        print(f"Confianza: {result['confidence']}%")
        print(f"Explicación:\n{explanation}")
        print("-" * 50)


if __name__ == "__main__":
    main()
