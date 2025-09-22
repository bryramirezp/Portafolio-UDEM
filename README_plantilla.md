# 📋 Guía de Desarrollo - Portafolio Web Neo Brutalista

Esta guía completa documenta el sistema de diseño Neo Brutalista, la arquitectura del proyecto, y todas las directrices necesarias para desarrollar y mantener el portafolio web de manera consistente.

## 🎯 Propósito

Este documento sirve como:
- **Guía de desarrollo** para nuevos colaboradores
- **Documentación técnica** del sistema de diseño
- **Referencia** para mantener consistencia visual y funcional
- **Plantilla** para implementar nuevas páginas y componentes

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
Portafolio-UDEM/
├── index.html                          # Página principal
├── README.md                           # README para GitHub
├── README_plantilla.md                 # 📋 Esta guía de desarrollo
├── assets/                             # Recursos estáticos
│   ├── css/
│   │   ├── neo-brutalist.css          # 🎨 Sistema de diseño base
│   │   └── style.css                  # 🎨 Overrides y estilos específicos
│   └── js/
│       ├── neo-brutalist.js           # ⚙️ Sistema Neo Brutalist JS
│       ├── neo-header.js              # 🧭 Componente Header
│       └── main.js                    # 🚀 Funcionalidades principales
└── Integ_aplicaciones_computacion/     # 📚 Contenido académico
    ├── ejercicios-guiados.html        # Índice de ejercicios
    ├── tareas.html                    # Índice de tareas
    ├── parciales.html                 # Índice de parciales
    ├── proyecto-final.html            # Proyecto final
    └── [carpetas individuales]/       # Contenido específico
```

### Arquitectura de Componentes

```
📦 Sistema Neo Brutalist
├── 🎨 CSS Framework (neo-brutalist.css)
│   ├── Variables CSS personalizables
│   ├── Componentes base (botones, cards, headers)
│   ├── Utilidades y helpers
│   ├── Tema oscuro/claro automático
│   └── Animaciones y efectos
├── ⚙️ JavaScript System
│   ├── NeoBrutalist.js - Sistema principal
│   ├── NeoHeader.js - Componentes de navegación
│   └── Main.js - Funcionalidades específicas
└── 🏗️ HTML Templates
    ├── Header reutilizable
    ├── Cards para contenido
    └── Layouts responsive
```

## 🎨 Sistema de Diseño Neo Brutalista

### Paleta de Colores Oficial

| Color | Código Hex | Variable CSS | Uso Principal | Modo Oscuro |
|-------|------------|--------------|---------------|-------------|
| **Amarillo Neo** | `#FFD166` | `--neo-yellow` | Botones primarios, acentos | `#FFD166` |
| **Negro Neo** | `#073B4C` | `--neo-black` | Texto principal, fondos claros | `#FFFFFF` |
| **Blanco Neo** | `#FFFFFF` | `--neo-white` | Fondos, texto en modo oscuro | `#1A1A1A` |
| **Gris Claro** | `#F5F5F5` | `--neo-gray` | Fondos secundarios | `#073B4C` |
| **Gris Oscuro** | `#333333` | `--neo-dark-gray` | Texto secundario | `#E0E0E0` |

### Variables CSS Principales

```css
:root {
  /* Colores Neo Brutalist */
  --neo-yellow: #FFD166;
  --neo-black: #073B4C;
  --neo-white: #FFFFFF;
  --neo-gray: #F5F5F5;
  --neo-dark-gray: #333333;

  /* Bordes y Sombras */
  --border-width: 4px;
  --shadow-offset: 8px;
  --shadow-offset-hover: 6px;
  --border-radius: 4px;

  /* Transiciones */
  --transition-speed: 0.2s;
  --transition-easing: ease;
}

/* Modo Oscuro */
[data-theme="dark"] {
  --bg-primary: #073B4C;
  --bg-secondary: #1A1A1A;
  --text-primary: #FFFFFF;
  --text-secondary: #E0E0E0;
  --border-color: #FFFFFF;
  --shadow-color: #FFFFFF;
}
```

### Tipografía

#### Fuentes Oficiales

```css
/* Importación requerida en todas las páginas */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue:wght@400&family=Roboto+Mono:wght@400;500;600;700&display=swap');
```

#### Jerarquía Tipográfica

```css
/* Títulos - Bebas Neue */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Bebas Neue', sans-serif;
  letter-spacing: 2px;
  font-weight: 400;
  margin: 0;
}

/* Tamaños específicos */
h1 { font-size: 2.5rem; }    /* Headers principales */
h2 { font-size: 2rem; }      /* Títulos de sección */
h3 { font-size: 1.5rem; }    /* Subtítulos */
h4 { font-size: 1.25rem; }   /* Títulos de cards */
h5 { font-size: 1.125rem; }  /* Subtítulos pequeños */
h6 { font-size: 1rem; }      /* Mínimos */

/* Cuerpo de texto - Roboto Mono */
body, p, span, div, input, button {
  font-family: 'Roboto Mono', monospace;
  line-height: 1.6;
}
```

### Sistema de Espaciado

#### Variables de Espaciado

```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
--spacing-xxl: 48px;
```

#### Clases de Utilidad

```css
/* Márgenes */
.neo-mb-1 { margin-bottom: 8px; }   /* --spacing-sm */
.neo-mb-2 { margin-bottom: 16px; }  /* --spacing-md */
.neo-mb-3 { margin-bottom: 24px; }  /* --spacing-lg */
.neo-mb-4 { margin-bottom: 32px; }  /* --spacing-xl */

/* Paddings */
.neo-p-1 { padding: 8px; }           /* --spacing-sm */
.neo-p-2 { padding: 16px; }          /* --spacing-md */
.neo-p-3 { padding: 24px; }          /* --spacing-lg */
.neo-p-4 { padding: 32px; }          /* --spacing-xl */
```

## 🧩 Componentes del Sistema

### 1. Header Neo Brutalist (`neo-header`)

#### Estructura HTML

```html
<header class="neo-header">
  <div class="neo-header__left">
    <span class="neo-button neo-button--primary">#UDEM</span>
    <a href="#" class="neo-button neo-button--secondary">← Volver</a>
  </div>
  <div class="neo-header__center">
    <h1 class="neo-header__title">Título de la Página</h1>
    <p class="neo-header__subtitle">Subtítulo descriptivo</p>
  </div>
  <div class="neo-header__right">
    <!-- Toggle de tema se agrega automáticamente por JS -->
  </div>
</header>
```

#### Variantes del Header

```javascript
// Header principal (creado automáticamente)
const mainHeader = NeoHeaderFactory.createMainHeader();

// Header de categoría
const categoryHeader = NeoHeaderFactory.createCategoryHeader(
  "Ejercicios Guiados",
  "../index.html"
);

// Header de contenido específico
const contentHeader = NeoHeaderFactory.createContentHeader(
  "Mi Contenido",
  "../ejercicios-guiados.html"
);
```

### 2. Cards Neo Brutalist (`neo-card`)

#### Estructura Básica

```html
<div class="neo-card">
  <div class="neo-card__title">Título de la Card</div>
  <div class="neo-card__content">
    <p>Contenido de la card. Puede incluir texto, imágenes, botones, etc.</p>
    <button class="neo-button neo-button--primary">Acción</button>
  </div>
</div>
```

#### Cards Interactivas (para navegación)

```html
<a href="destino.html" class="neo-card" style="text-decoration: none; color: inherit;">
  <div class="neo-card__title">Título del Enlace</div>
  <div class="neo-card__content">
    <div style="display: flex; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
      <span style="font-size: 2rem;">🎯</span>
      <span style="font-size: 2rem;">📊</span>
    </div>
    <p>Descripción del contenido al que lleva este enlace.</p>
  </div>
</div>
```

### 3. Botones Neo Brutalist (`neo-button`)

#### Variantes de Botones

```html
<!-- Botón primario (acciones principales) -->
<button class="neo-button neo-button--primary">
  Acción Principal
</button>

<!-- Botón secundario (acciones secundarias) -->
<button class="neo-button neo-button--secondary">
  Acción Secundaria
</button>

<!-- Botón de peligro (eliminar, cancelar) -->
<button class="neo-button neo-button--danger">
  Eliminar
</button>

<!-- Botón deshabilitado -->
<button class="neo-button neo-button--primary" disabled>
  Cargando...
</button>
```

#### Estados de Botones

```css
/* Estados automáticos */
.neo-button:hover {
  transform: translate(2px, 2px);
  box-shadow: var(--shadow-offset-hover) var(--shadow-offset-hover) 0 var(--shadow-color);
}

.neo-button:active {
  transform: translate(0, 0);
  box-shadow: 2px 2px 0 var(--shadow-color);
}

.neo-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
```

### 4. Toggle de Tema (`neo-toggle`)

#### Implementación Automática

El toggle de tema se crea automáticamente por `neo-brutalist.js` y se inserta en el header. No requiere implementación manual.

#### Funcionamiento

- **Persistencia**: El tema se guarda en `localStorage`
- **Transiciones**: Cambios suaves entre modos
- **Estados**: "modo oscuro" / "modo claro"

### 5. Contenedores y Layout (`neo-container`, `neo-grid`)

#### Container Principal

```html
<main class="neo-container" style="padding: 3rem 0;">
  <!-- Contenido centrado con max-width -->
</main>
```

#### Sistema de Grids

```html
<!-- Grid de 2 columnas -->
<div class="neo-grid neo-grid--2">
  <div class="neo-card">Card 1</div>
  <div class="neo-card">Card 2</div>
</div>

<!-- Grid de 3 columnas -->
<div class="neo-grid neo-grid--3">
  <div class="neo-card">Card 1</div>
  <div class="neo-card">Card 2</div>
  <div class="neo-card">Card 3</div>
</div>

<!-- Grid responsive (auto-fit) -->
<div class="neo-grid">
  <!-- Mínimo 300px por columna, se adapta automáticamente -->
</div>
```

### 6. Footer Neo Brutalist (`neo-footer`)

```html
<footer class="neo-footer">
  <div class="neo-footer__center">
    <p class="neo-footer__text">Bryan Ramírez Palacios</p>
  </div>
</footer>
```

## 🔧 Guía de Implementación

### Creando una Nueva Página

#### Paso 1: Estructura HTML Base

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Título de la Página - Portafolio UDEM</title>

    <!-- CSS obligatorio - IMPORTANTE: Este orden -->
    <link rel="stylesheet" href="../assets/css/neo-brutalist.css">
    <link rel="stylesheet" href="../assets/css/style.css">

    <!-- Fuentes requeridas -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue:wght@400&family=Roboto+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>

    <!-- Header Neo Brutalist -->
    <header class="neo-header">
        <div class="neo-header__left">
            <a href="../index.html" class="neo-button neo-button--secondary">← Volver</a>
        </div>
        <div class="neo-header__center">
            <h1 class="neo-header__title">Título de la Página</h1>
            <p class="neo-header__subtitle">Subtítulo descriptivo</p>
        </div>
        <div class="neo-header__right">
            <!-- Toggle se agrega automáticamente por JS -->
        </div>
    </header>

    <!-- Contenido principal -->
    <main class="neo-container" style="padding: 3rem 0;">
        <!-- Contenido específico aquí -->
    </main>

    <!-- Footer Neo Brutalist -->
    <footer class="neo-footer">
        <div class="neo-footer__center">
            <p class="neo-footer__text">Bryan Ramírez Palacios</p>
        </div>
    </footer>

    <!-- Scripts obligatorios - IMPORTANTE: Este orden -->
    <script src="../assets/js/neo-brutalist.js"></script>
    <script src="../assets/js/main.js"></script>

    <!-- Script específico de la página (opcional) -->
    <script>
        // Funcionalidad específica aquí
    </script>

</body>
</html>
```

#### Paso 2: Agregar Contenido con Componentes

```html
<main class="neo-container" style="padding: 3rem 0;">
    <!-- Título de sección -->
    <h2 style="text-align: center; margin-bottom: 2rem;">Mi Nueva Sección</h2>

    <!-- Grid de contenido -->
    <div class="neo-grid neo-grid--2" style="max-width: 900px; margin: 0 auto;">

        <!-- Card informativa -->
        <div class="neo-card">
            <div class="neo-card__title">Información</div>
            <div class="neo-card__content">
                <p>Contenido explicativo sobre el tema.</p>
                <ul>
                    <li>Punto importante 1</li>
                    <li>Punto importante 2</li>
                    <li>Punto importante 3</li>
                </ul>
            </div>
        </div>

        <!-- Card con acción -->
        <div class="neo-card">
            <div class="neo-card__title">Acciones</div>
            <div class="neo-card__content">
                <p>Descripción de las acciones disponibles.</p>
                <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                    <button class="neo-button neo-button--primary">
                        Acción Principal
                    </button>
                    <button class="neo-button neo-button--secondary">
                        Acción Secundaria
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Contenido adicional -->
    <div style="max-width: 900px; margin: 3rem auto 0;">
        <div class="neo-card">
            <div class="neo-card__title">Contenido Detallado</div>
            <div class="neo-card__content">
                <p>Contenido más detallado aquí. Puede incluir:</p>

                <!-- Lista con viñetas -->
                <ul>
                    <li>Elementos de lista</li>
                    <li>Más elementos</li>
                </ul>

                <!-- Código inline -->
                <p>Para mostrar código: <code>console.log('Hola mundo');</code></p>

                <!-- Bloque de código -->
                <pre><code>// Bloque de código
function ejemplo() {
    console.log('Esto es un ejemplo');
}</code></pre>

                <!-- Imágenes -->
                <img src="imagen.jpg" alt="Descripción" class="article-image" style="margin-top: 1rem;">

                <!-- Cita -->
                <blockquote style="border-left: 4px solid var(--neo-yellow); padding-left: 1rem; margin: 1rem 0; font-style: italic;">
                    "Esta es una cita importante del contenido."
                </blockquote>
            </div>
        </div>
    </div>
</main>
```

#### Paso 3: Agregar Funcionalidad JavaScript (Opcional)

```html
<script>
document.addEventListener('DOMContentLoaded', () => {
    console.log('Página específica cargada');

    // Ejemplo: Interactividad básica
    const buttons = document.querySelectorAll('.neo-button');
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            console.log('Botón clickeado:', button.textContent.trim());

            // Efecto visual de "carga"
            button.classList.add('neo-loading');
            button.textContent = 'Cargando...';

            setTimeout(() => {
                button.classList.remove('neo-loading');
                button.textContent = button.textContent.replace('Cargando...', '¡Listo!');
            }, 1000);
        });
    });

    // Ejemplo: Validación de formulario (si existe)
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            // Lógica de validación aquí
            const inputs = form.querySelectorAll('input, textarea');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.style.borderColor = '#FF4444';
                    isValid = false;
                } else {
                    input.style.borderColor = 'var(--border-color)';
                }
            });

            if (isValid) {
                console.log('Formulario válido, procesando...');
                // Enviar formulario o procesar datos
            }
        });
    }
});
</script>
```

### Agregando una Nueva Categoría al Menú Principal

#### Paso 1: Actualizar `index.html`

```html
<!-- En index.html, dentro del main -->
<div class="neo-grid neo-grid--2" style="max-width: 900px; margin: 0 auto;">

    <!-- Categorías existentes -->
    <div class="neo-card" onclick="openFolder('ejercicios-guiados')" style="cursor: pointer;">
        <div class="neo-card__title">Ejercicios Guiados</div>
        <div class="neo-card__content">
            <div style="display: flex; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
                <span style="font-size: 2rem;">🐳</span>
                <span style="font-size: 2rem;">💬</span>
                <span style="font-size: 2rem;">📚</span>
            </div>
            <p>Explora los ejercicios prácticos de Docker, IA y XML/XSLT</p>
        </div>
    </div>

    <!-- Nueva categoría -->
    <div class="neo-card" onclick="openFolder('nueva-categoria')" style="cursor: pointer;">
        <div class="neo-card__title">Nueva Categoría</div>
        <div class="neo-card__content">
            <div style="display: flex; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
                <span style="font-size: 2rem;">🎯</span>
                <span style="font-size: 2rem;">📊</span>
            </div>
            <p>Descripción de la nueva categoría y sus contenidos</p>
        </div>
    </div>

</div>
```

#### Paso 2: Crear Página de Índice de la Categoría

```html
<!-- Integ_aplicaciones_computacion/nueva-categoria.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nueva Categoría - Portafolio UDEM</title>
    <link rel="stylesheet" href="../assets/css/neo-brutalist.css">
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue:wght@400&family=Roboto+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>

    <header class="neo-header">
        <div class="neo-header__left">
            <a href="../index.html" class="neo-button neo-button--secondary">← Volver</a>
        </div>
        <div class="neo-header__center">
            <h1 class="neo-header__title">Nueva Categoría</h1>
            <p class="neo-header__subtitle">Descripción de la categoría</p>
        </div>
        <div class="neo-header__right"></div>
    </header>

    <main class="neo-container" style="padding: 3rem 0;">
        <div class="neo-grid neo-grid--3" style="max-width: 1200px; margin: 0 auto;">

            <!-- Elemento 1 -->
            <a href="nueva-categoria/contenido-1.html" class="neo-card" style="text-decoration: none; color: inherit;">
                <div class="neo-card__title">Contenido 1</div>
                <div class="neo-card__content">
                    <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
                        <span style="font-size: 3rem;">🎯</span>
                    </div>
                    <p>Descripción del primer contenido</p>
                </div>
            </a>

            <!-- Más elementos aquí -->

        </div>
    </main>

    <footer class="neo-footer">
        <div class="neo-footer__center">
            <p class="neo-footer__text">Bryan Ramírez Palacios</p>
        </div>
    </footer>

    <script src="../assets/js/neo-brutalist.js"></script>
    <script src="../assets/js/main.js"></script>

</body>
</html>
```

## 🎭 Funcionalidades Especiales

### Sistema de Tema Oscuro/Claro

#### Funcionamiento Automático

- **Activación**: Toggle en esquina superior derecha
- **Persistencia**: Se guarda en `localStorage`
- **Transiciones**: Suaves entre modos
- **Alcance**: Afecta todos los componentes automáticamente

#### Variables que Cambian

```css
/* Modo Claro (por defecto) */
--bg-primary: #F5F5F5;      /* Fondo principal */
--bg-secondary: #FFFFFF;    /* Fondos de cards */
--text-primary: #073B4C;    /* Texto principal */
--text-secondary: #333333;  /* Texto secundario */
--border-color: #000000;    /* Bordes */
--shadow-color: #000000;    /* Sombras */

/* Modo Oscuro */
--bg-primary: #073B4C;      /* Fondo principal */
--bg-secondary: #1A1A1A;    /* Fondos de cards */
--text-primary: #FFFFFF;    /* Texto principal */
--text-secondary: #E0E0E0;  /* Texto secundario */
--border-color: #FFFFFF;    /* Bordes */
--shadow-color: #FFFFFF;    /* Sombras */
```

### Easter Egg: Sistema de Papas Fritas 🍟

#### Activación

Haz clic en el botón "#UDEM" en cualquier header para activar una animación especial de papas fritas.

#### Configuración

```javascript
// En main.js - Configuración del sistema de papas fritas
const FRIES_CONFIG = {
    count: 30,                    // Número de papas fritas
    colors: {                     // Colores disponibles
        golden: '#FFD700',
        lightGolden: '#FFA500',
        darkGolden: '#DAA520',
        crispy: '#CD853F',
        shadow: '#8B4513'
    },
    gravity: 0.4,                // Gravedad
    drag: 0.08,                  // Resistencia del aire
    terminalVelocity: 4,         // Velocidad máxima
    rotationSpeed: 0.05,         // Velocidad de rotación
    bounce: 0.6                  // Rebote
};
```

### Sistema de Analytics

#### Eventos Automáticos

```javascript
// Se trackean automáticamente
trackEvent('click', 'card', 'Ejercicios Guiados');
trackEvent('theme_change', 'toggle', 'dark');
trackEvent('easter_egg', 'french_fries', 'udem_button');
```

## 📱 Diseño Responsive

### Breakpoints

```css
/* Desktop grande */
@media (max-width: 1200px) {
    .neo-grid--3 { grid-template-columns: repeat(2, 1fr); }
}

/* Tablet */
@media (max-width: 768px) {
    .neo-header {
        padding: 12px 16px;
        flex-direction: column;
        gap: 12px;
    }

    .neo-grid--2,
    .neo-grid--3,
    .neo-grid--4 {
        grid-template-columns: 1fr;
    }

    h1 { font-size: 2rem; }
    h2 { font-size: 1.5rem; }
    h3 { font-size: 1.25rem; }
}

/* Móvil */
@media (max-width: 480px) {
    .neo-button {
        padding: 10px 20px;
        font-size: 0.9rem;
    }

    .neo-card {
        padding: 16px;
    }

    .neo-header__title {
        font-size: 1.5rem;
    }
}
```

### Consideraciones Responsive

- **Header**: Se apila verticalmente en móviles
- **Grids**: Se convierten a columna única
- **Tipografía**: Tamaños reducidos en pantallas pequeñas
- **Espaciado**: Paddings y márgenes ajustados
- **Botones**: Tamaños optimizados para touch

## 🔧 Lineamientos de Desarrollo

### Convenciones de Código

#### HTML
- Usar comillas dobles para atributos
- Cerrar todas las etiquetas
- Indentación consistente (2 espacios)
- Atributo `lang="es"` en `<html>`
- Meta viewport obligatorio

#### CSS
- Prefijo `neo-` para clases del sistema
- Variables CSS para colores y espaciado
- Comentarios descriptivos
- No usar `!important` sin justificación

#### JavaScript
- `const` y `let` en lugar de `var`
- Funciones arrow cuando apropiado
- Comentarios JSDoc para funciones públicas
- Event listeners con `addEventListener`

### Control de Calidad

#### Checklist Pre-commit

- [ ] **HTML**: Validación sintaxis, atributos completos
- [ ] **CSS**: Consistencia con sistema de diseño
- [ ] **JS**: Funcionalidad probada, errores manejados
- [ ] **Responsive**: Probado en diferentes tamaños
- [ ] **Tema**: Funciona en modo claro y oscuro
- [ ] **Accesibilidad**: Navegación por teclado, contraste

#### Pruebas Visuales

- [ ] Componentes renderizan correctamente
- [ ] Hover effects funcionan
- [ ] Transiciones son suaves
- [ ] Texto es legible
- [ ] Colores contrastan adecuadamente

### Manejo de Errores

#### JavaScript Error Handling

```javascript
// Global error handler
window.addEventListener('error', (e) => {
    console.error('🚨 Error en Neo Brutalist Portfolio:', e.error);

    // Analytics opcional
    if (typeof gtag !== 'undefined') {
        gtag('event', 'exception', {
            description: e.error.message,
            fatal: false
        });
    }
});

// Try-catch para operaciones críticas
try {
    // Código que puede fallar
    initializeComponent();
} catch (error) {
    console.error('Error inicializando componente:', error);
    // Fallback o mensaje de error
}
```

## 📚 Contenido Académico

### Estructura de Contenidos

Cada elemento académico debe seguir esta estructura:

```
categoria/
├── index.html                 # Página índice de la categoría
├── contenido-1/
│   ├── contenido-1.html      # Página principal
│   ├── assets/               # Recursos específicos (opcional)
│   └── *.png/*.jpg           # Imágenes
└── contenido-2/
    └── ...
```

### Tipos de Contenido

#### 1. Artículos Teóricos
- Explicaciones conceptuales
- Diagramas y esquemas
- Referencias bibliográficas

#### 2. Prácticas Guiadas
- Pasos detallados
- Código de ejemplo
- Capturas de pantalla
- Resultados esperados

#### 3. Proyectos Completos
- Arquitectura general
- Componentes individuales
- Instrucciones de despliegue
- Casos de uso

### Formato de Contenido

#### Encabezados Jerárquicos

```html
<h2>Título de Sección Principal</h2>
<p>Introducción a la sección.</p>

<h3>Subsección</h3>
<p>Contenido de la subsección.</p>

<h4>Sub-subsección</h4>
<p>Detalle específico.</p>
```

#### Elementos de Código

```html
<!-- Código inline -->
<p>Para declarar una variable: <code>const variable = 'valor';</code></p>

<!-- Bloque de código -->
<pre><code>// Función de ejemplo
function calcularTotal(items) {
    return items.reduce((total, item) => total + item.precio, 0);
}</code></pre>
```

#### Imágenes y Medios

```html
<!-- Imagen con caption -->
<figure>
    <img src="diagrama.png" alt="Diagrama de arquitectura" class="article-image">
    <figcaption class="image-caption">
        Figura 1: Arquitectura del sistema de microservicios
    </figcaption>
</figure>
```

## 🚀 Despliegue y Mantenimiento

### GitHub Pages

#### Configuración Automática

1. **Repositorio**: `https://github.com/bryramirezp/Portafolio-UDEM`
2. **Rama**: `main`
3. **Directorio**: `/` (raíz)
4. **URL**: `https://bryramirezp.github.io/Portafolio-UDEM/`

#### Actualización

```bash
# Commits regulares
git add .
git commit -m "feat: agregar nueva funcionalidad"
git push origin main

# GitHub Pages se actualiza automáticamente
```

### Mantenimiento del Sistema

#### Actualizaciones del Sistema Neo Brutalist

1. **CSS**: Modificar `neo-brutalist.css` para cambios globales
2. **JS**: Actualizar `neo-brutalist.js` para nuevas funcionalidades
3. **Componentes**: Mantener consistencia en todas las páginas

#### Checklist de Mantenimiento

- [ ] **Dependencias**: Verificar enlaces a fuentes y scripts externos
- [ ] **Compatibilidad**: Probar en navegadores modernos
- [ ] **Performance**: Optimizar imágenes y recursos
- [ ] **SEO**: Meta tags y estructura semántica
- [ ] **Analytics**: Monitoreo de uso y errores

## 📋 Checklist de Implementación

### Para Nuevas Páginas

- [ ] Estructura HTML base correcta
- [ ] CSS y JS incluidos en orden correcto
- [ ] Header Neo Brutalist implementado
- [ ] Contenido organizado en cards/grids
- [ ] Footer incluido
- [ ] Responsive design verificado
- [ ] Tema oscuro/claro probado
- [ ] Navegación funcional
- [ ] Contenido validado

### Para Nuevos Componentes

- [ ] Consistencia con sistema Neo Brutalist
- [ ] Variables CSS utilizadas
- [ ] Estados hover/active implementados
- [ ] Responsive design
- [ ] Tema oscuro/claro soportado
- [ ] Documentación actualizada

### Para Contenido Académico

- [ ] Estructura de directorios correcta
- [ ] Contenido completo y preciso
- [ ] Imágenes optimizadas
- [ ] Código bien formateado
- [ ] Referencias incluidas
- [ ] Enlaces funcionales

---

## 📞 Soporte y Contacto

**Desarrollador**: Bryan Ramírez Palacios
**Institución**: Universidad de Monterrey (UDEM)
**Proyecto**: Portafolio de Integración de Aplicaciones Computacionales

Para preguntas sobre desarrollo o implementación, referirse a esta documentación o contactar al desarrollador principal.

---

*Esta guía se mantiene actualizada con el desarrollo del proyecto. Última actualización: Diciembre 2024*