# Análisis de Estilos Hardcodeados en Template

Este documento identifica todos los estilos inline (`style=""`) encontrados en los archivos HTML de la carpeta `template` y recomienda moverlos al archivo CSS centralizado.

## Resumen Ejecutivo

- **Total de archivos con estilos inline**: 18 archivos HTML
- **Categorías principales de estilos hardcodeados**:
  1. Layout y espaciado (padding, margin, flex)
  2. Enlaces y cards (text-decoration, color)
  3. Contenedores de emojis (display: flex, justify-content)
  4. Estilos de body (min-height, flex-direction)
  5. Estilos específicos de contenido (text-align, list-style)

## Estilos Hardcodeados por Categoría

### 1. Layout y Espaciado del Main

**Ubicación**: Todos los archivos principales y de contenido

**Estilos encontrados**:
```html
<main class="neo-container" style="padding: 3rem 0;">
<main class="neo-container" style="padding: 3rem 0; flex: 1;">
```

**Archivos afectados**:
- `ejercicios-guiados.html`
- `tareas.html`
- `proyecto-final.html`
- `parciales.html`
- Todos los archivos de ejercicios guiados (1-9)
- Todos los archivos de tareas (1-3)
- `parcial_1/index.html`
- `primer_avance_proyecto/primer-avance.html`
- `tarea_3/tarea-3.html`

**Recomendación**: Crear clases CSS:
```css
.neo-container--spaced {
  padding: 3rem 0;
}

.neo-container--flex {
  padding: 3rem 0;
  flex: 1;
}
```

---

### 2. Grids con Max-Width

**Ubicación**: Archivos de listado principal

**Estilos encontrados**:
```html
<div class="neo-grid neo-grid--3" style="max-width: 1200px; margin: 0 auto;">
<div class="neo-grid neo-grid--1" style="max-width: 800px; margin: 0 auto;">
```

**Archivos afectados**:
- `ejercicios-guiados.html` (max-width: 1200px)
- `tareas.html` (max-width: 1200px)
- `proyecto-final.html` (max-width: 800px)
- `parciales.html` (max-width: 800px)

**Recomendación**: Crear clases CSS:
```css
.neo-grid--max-1200 {
  max-width: 1200px;
  margin: 0 auto;
}

.neo-grid--max-800 {
  max-width: 800px;
  margin: 0 auto;
}
```

---

### 3. Enlaces de Cards (text-decoration y color)

**Ubicación**: Todos los archivos de listado

**Estilos encontrados**:
```html
<a href="..." class="neo-card" style="text-decoration: none; color: inherit;">
<a href="..." class="neo-card" style="text-decoration: none; color: inherit; opacity: 1; transform: translateY(0px); transition: 0.2s;">
```

**Archivos afectados**:
- `ejercicios-guiados.html` (múltiples instancias)
- `tareas.html` (múltiples instancias)
- `proyecto-final.html`
- `parciales.html`
- `tarea_3/tarea-3.html`

**Recomendación**: Agregar al CSS:
```css
a.neo-card {
  text-decoration: none;
  color: inherit;
  display: block;
}
```

---

### 4. Contenedores de Emojis

**Ubicación**: Todos los archivos de listado

**Estilos encontrados**:
```html
<div style="display: flex; justify-content: center; margin-bottom: 1rem;">
```

**Archivos afectados**:
- `ejercicios-guiados.html` (9 instancias)
- `tareas.html` (3 instancias)
- `proyecto-final.html`
- `parciales.html`

**Recomendación**: Crear clase CSS:
```css
.neo-emoji-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}
```

---

### 5. Estilos de Body (Flex Layout)

**Ubicación**: Archivos de contenido individual

**Estilos encontrados**:
```html
<body style="min-height: 100vh; display: flex; flex-direction: column;">
```

**Archivos afectados**:
- `tarea_3/tarea-3.html`
- `primer_avance_proyecto/primer-avance.html`
- `tarea_2/tarea-2.html`

**Recomendación**: Ya existe en CSS base, pero verificar que se aplique correctamente. El body ya tiene `min-height: 100vh` y `display: flex; flex-direction: column;` en el CSS.

---

### 6. Estilos Específicos de Contenido

#### 6.1 Text-align y Margin en Párrafos

**Ubicación**: `tarea_3/tarea-3.html`

**Estilos encontrados**:
```html
<p style="text-align: center; margin-bottom: 2rem; font-style: italic;">
<div style="text-align: center; margin: 2rem 0;">
```

**Recomendación**: Crear clases utilitarias:
```css
.neo-text-center-italic {
  text-align: center;
  margin-bottom: 2rem;
  font-style: italic;
}

.neo-center-spaced {
  text-align: center;
  margin: 2rem 0;
}
```

#### 6.2 Imágenes con Estilos Completos

**Ubicación**: `tarea_3/tarea-3.html`

**Estilos encontrados**:
```html
<img ... style="max-width: 100%; height: auto; border-radius: var(--border-radius); border: var(--border-width) solid var(--border-color); box-shadow: var(--shadow-offset) var(--shadow-offset) 0 var(--shadow-color);">
```

**Recomendación**: Ya existe la clase `.article-image` en CSS, usar esa clase en lugar de estilos inline.

#### 6.3 Cards con Max-Width

**Ubicación**: `tarea_3/tarea-3.html`

**Estilos encontrados**:
```html
<a href="./" class="neo-card" style="max-width: 600px; margin: 0 auto; text-decoration: none; color: inherit; display: block;">
```

**Recomendación**: Crear clase CSS:
```css
.neo-card--max-600 {
  max-width: 600px;
  margin: 0 auto;
}
```

---

### 7. Estilos en `primer_avance_proyecto/primer-avance.html`

Este archivo tiene múltiples estilos inline que deberían moverse al CSS:

#### 7.1 Listas sin Estilo

**Estilos encontrados**:
```html
<ul style="list-style: none; padding: 0;">
<ol style="padding-left: 0;">
```

**Recomendación**: Crear clases CSS:
```css
.neo-list-unstyled {
  list-style: none;
  padding: 0;
}

.neo-list-unstyled ol {
  padding-left: 0;
}
```

#### 7.2 Items de Lista con Estilos Neo Brutalist

**Estilos encontrados**:
```html
<li style="margin-bottom: 1rem; padding: 1rem; background: var(--bg-secondary); border: 2px solid var(--border-color); border-radius: var(--border-radius);">
<li style="margin-bottom: 0.5rem; padding: 0.5rem; background: var(--bg-secondary); border: 2px solid var(--border-color); border-radius: var(--border-radius);">
```

**Recomendación**: Crear clases CSS:
```css
.neo-list-item {
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius);
}

.neo-list-item--small {
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: var(--bg-secondary);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius);
}
```

#### 7.3 Títulos H3 con Estilos

**Estilos encontrados**:
```html
<h3 style="color: var(--text-primary); margin-bottom: 1rem; font-size: 1.5rem;">
<h3 style="color: var(--text-primary); margin: 2rem 0 1rem 0; font-size: 1.5rem;">
```

**Recomendación**: Los h3 ya tienen estilos en CSS, pero se puede crear una variante:
```css
.neo-content-title {
  color: var(--text-primary);
  margin-bottom: 1rem;
  font-size: 1.5rem;
}
```

#### 7.4 Pre y Code con Estilos

**Estilos encontrados**:
```html
<pre style="background: var(--bg-secondary); padding: 1.5rem; border: 2px solid var(--border-color); border-radius: var(--border-radius); overflow-x: auto; font-family: 'Roboto Mono', monospace; font-size: 0.9rem;">
<pre style="background: var(--bg-primary); padding: 0.5rem; margin-top: 0.5rem; border-radius: var(--border-radius); font-size: 0.8rem;">
```

**Recomendación**: Ya existen estilos para `pre` y `code` en CSS, pero se puede crear una variante:
```css
.neo-code-block {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow-x: auto;
  font-family: 'Inter', 'Courier New', Courier, monospace;
  font-size: 0.9rem;
}

.neo-code-inline {
  background: var(--bg-primary);
  padding: 0.5rem;
  margin-top: 0.5rem;
  border-radius: var(--border-radius);
  font-size: 0.8rem;
}
```

#### 7.5 Grid de Dos Columnas

**Estilos encontrados**:
```html
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
```

**Recomendación**: Crear clase CSS:
```css
.neo-grid-2cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .neo-grid-2cols {
    grid-template-columns: 1fr;
  }
}
```

---

### 8. Estilos en `<style>` Tags (tarea_1/tarea-1.html)

**Ubicación**: `tarea_1/tarea-1.html`

**Problema**: Este archivo tiene un bloque `<style>` con estilos específicos para el mapa conceptual.

**Recomendación**: Mover estos estilos al archivo CSS principal en una sección específica para mapas conceptuales, o crear un archivo CSS separado para componentes especiales.

---

## Prioridad de Refactorización

### Alta Prioridad (Usado en múltiples archivos)
1. ✅ Estilos de enlaces de cards (`text-decoration: none; color: inherit;`)
2. ✅ Contenedores de emojis (`display: flex; justify-content: center;`)
3. ✅ Padding del main (`padding: 3rem 0;`)
4. ✅ Max-width de grids (`max-width: 1200px/800px; margin: 0 auto;`)

### Media Prioridad (Usado en algunos archivos)
5. ✅ Estilos de listas sin estilo (`list-style: none; padding: 0;`)
6. ✅ Items de lista con estilos Neo Brutalist
7. ✅ Grid de dos columnas

### Baja Prioridad (Específicos de un archivo)
8. ✅ Estilos de pre/code específicos
9. ✅ Estilos de títulos H3 específicos
10. ✅ Estilos de body flex (ya debería estar en CSS base)

---

## Plan de Acción Recomendado

1. **Fase 1**: ✅ COMPLETADA - Mover estilos de alta prioridad al CSS
   - ✅ Crear clases para enlaces de cards (`a.neo-card`)
   - ✅ Crear clase para contenedores de emojis (`.neo-emoji-container`)
   - ✅ Crear clases para padding del main (`.neo-container--spaced`, `.neo-container--flex`)
   - ✅ Crear clases para max-width de grids (`.neo-grid--max-1200`, `.neo-grid--max-800`)
   - ✅ Actualizar todos los archivos HTML para usar las nuevas clases

2. **Fase 2**: ✅ COMPLETADA - Mover estilos de media prioridad
   - ✅ Crear clases para listas sin estilo (`.neo-list-unstyled`)
   - ✅ Crear clases para items de lista (`.neo-list-item`, `.neo-list-item--small`)
   - ✅ Crear clase para grid de dos columnas (`.neo-grid-2cols`)
   - ✅ Actualizar `primer_avance_proyecto/primer-avance.html` para usar las nuevas clases

3. **Fase 3**: ✅ COMPLETADA - Limpiar estilos específicos
   - ✅ Revisar y consolidar estilos de pre/code (`.neo-code-block`, `.neo-code-inline`)
   - ✅ Mover estilos del `<style>` tag de tarea_1 al CSS principal (todos los estilos de mapas conceptuales)
   - ✅ Verificar que estilos de body estén correctamente aplicados (eliminados estilos inline, ya están en CSS base)
   - ✅ Actualizar archivos HTML para usar las nuevas clases

4. **Fase 4**: ✅ COMPLETADA - Actualizar todos los archivos HTML
   - ✅ Reemplazar estilos inline por clases CSS
   - ✅ Crear clases adicionales para estilos específicos (títulos, imágenes, grids, alertas, etc.)
   - ✅ Verificar que no haya errores de linting
   - ⚠️ Pendiente: Probar en diferentes tamaños de pantalla (requiere testing manual)

---

## Notas Adicionales

- Algunos estilos inline pueden ser necesarios para casos específicos (como animaciones dinámicas), pero la mayoría debería moverse al CSS.
- Los estilos que usan variables CSS (`var(--variable)`) son buenos candidatos para mover al CSS, ya que ya están usando el sistema de diseño.
- Los estilos de transición y animación deberían estar en el CSS para mejor rendimiento y mantenibilidad.

---

---

## Resumen de Refactorización Completada

### ✅ Todas las Fases Completadas

**Fase 1**: Estilos de alta prioridad movidos al CSS
- 18 archivos HTML actualizados
- 4 clases CSS principales creadas

**Fase 2**: Estilos de media prioridad movidos al CSS
- 1 archivo HTML actualizado (`primer_avance_proyecto/primer-avance.html`)
- 4 clases CSS creadas

**Fase 3**: Estilos específicos consolidados
- 177 líneas de CSS movidas desde `<style>` tag
- 3 archivos HTML actualizados
- 2 clases CSS para pre/code creadas

**Fase 4**: Limpieza final de estilos inline
- Todos los archivos HTML actualizados
- 15+ clases CSS adicionales creadas
- 0 estilos inline restantes en archivos HTML

### Estadísticas Finales

- **Total de clases CSS creadas**: 30+ clases nuevas
- **Total de archivos HTML actualizados**: 18 archivos
- **Total de estilos inline eliminados**: 95+ instancias
- **Bloques `<style>` eliminados**: 1 (tarea_1/tarea-1.html)
- **Líneas de CSS movidas al archivo principal**: 177+ líneas

### Clases CSS Creadas (Resumen)

**Layout y Espaciado:**
- `.neo-container--spaced`, `.neo-container--flex`
- `.neo-grid--max-1200`, `.neo-grid--max-800`
- `.neo-card--max-600`, `.neo-card--max-900`
- `.neo-card__inner`

**Componentes:**
- `.neo-emoji-container`
- `.neo-list-unstyled`, `.neo-list-item`, `.neo-list-item--small`
- `.neo-grid-2cols`, `.neo-grid-auto-fit`, `.neo-grid-auto-fit--large`
- `.neo-code-block`, `.neo-code-inline`

**Utilidades:**
- `.neo-text-center-italic`, `.neo-center-spaced`, `.neo-center-top`
- `.neo-content-title`, `.neo-content-title--spaced`, `.neo-content-title--small`
- `.neo-title-large`
- `.neo-card-box`, `.neo-card-box--large`
- `.neo-mb-3rem`, `.neo-mt-2rem`, `.neo-mb-2rem`
- `.neo-text-margin-small`, `.neo-text-margin-top`, `.neo-text-italic-secondary`
- `.neo-divider-yellow`
- `.neo-svg-absolute`
- `.neo-footer-sticky`
- `.neo-alert-warning`
- `.neo-image-container`, `.neo-image-caption`
- `.neo-image-max-600`, `.neo-image-max-800`
- `.neo-info-box`
- `.neo-text-small-gray`
- `.control-label--iaas`, `.control-label--paas`, `.control-label--saas`, `.control-label--faas`

---

**Última actualización**: 2025-01-27
**Archivos analizados**: 18 archivos HTML en la carpeta `template/`
**Estado**: ✅ Refactorización completa - Todos los estilos inline han sido movidos al CSS

