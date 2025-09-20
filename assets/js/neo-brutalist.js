/**
 * NEO BRUTALIST DESIGN SYSTEM - JAVASCRIPT
 * Sistema completo de componentes y funcionalidades
 */

class NeoBrutalistSystem {
  constructor() {
    this.isDarkMode = false;
    this.init();
  }

  /**
   * Inicializar el sistema
   */
  init() {
    this.loadTheme();
    this.createThemeToggle();
    this.initializeComponents();
    this.setupEventListeners();
    console.log('🎨 Neo Brutalist System initialized');
  }

  /**
   * Cargar tema guardado en localStorage
   */
  loadTheme() {
    const savedTheme = localStorage.getItem('neo-brutalist-theme');
    if (savedTheme) {
      this.isDarkMode = savedTheme === 'dark';
      this.applyTheme();
    }
  }

  /**
   * Aplicar tema actual
   */
  applyTheme() {
    const root = document.documentElement;
    root.setAttribute('data-theme', this.isDarkMode ? 'dark' : 'light');
    
    // Actualizar texto del toggle si existe
    const toggleText = document.querySelector('.neo-toggle__text');
    if (toggleText) {
      toggleText.textContent = this.isDarkMode ? 'modo claro' : 'modo oscuro';
    }
  }

  /**
   * Alternar entre modo claro y oscuro
   */
  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    this.applyTheme();
    localStorage.setItem('neo-brutalist-theme', this.isDarkMode ? 'dark' : 'light');
    
    // Efecto visual del toggle
    this.animateToggle();
  }

  /**
   * Crear toggle de tema en el header
   */
  createThemeToggle() {
    // Buscar header existente
    const header = document.querySelector('.neo-header, .file-system-header, .folder-page-header');
    
    if (header) {
      // Verificar si ya existe un toggle para evitar duplicación
      const existingToggle = header.querySelector('.neo-toggle');
      if (existingToggle) {
        console.log('🎨 Toggle ya existe, configurando funcionalidad');
        this.setupToggleFunctionality(existingToggle);
        return;
      }
      
      const toggleContainer = document.createElement('div');
      toggleContainer.className = 'neo-header__theme-toggle';
      
      toggleContainer.innerHTML = `
        <label class="neo-toggle">
          <span class="neo-toggle__text">${this.isDarkMode ? 'modo claro' : 'modo oscuro'}</span>
          <input type="checkbox" class="neo-toggle__input" ${this.isDarkMode ? 'checked' : ''}>
          <span class="neo-toggle__slider"></span>
        </label>
      `;
      
      // Insertar en la parte derecha del header
      const rightSection = header.querySelector('.neo-header__right, .header-right');
      if (rightSection) {
        rightSection.appendChild(toggleContainer);
      } else {
        // Si no hay sección derecha, crear una
        const rightDiv = document.createElement('div');
        rightDiv.className = 'neo-header__right';
        rightDiv.appendChild(toggleContainer);
        header.appendChild(rightDiv);
      }
      
      // Configurar funcionalidad del toggle
      this.setupToggleFunctionality(toggleContainer.querySelector('.neo-toggle'));
      
      console.log('🎨 Toggle creado exitosamente');
    } else {
      console.warn('⚠️ No se encontró header para crear el toggle');
    }
  }

  /**
   * Configurar funcionalidad del toggle
   */
  setupToggleFunctionality(toggleElement) {
    const toggleInput = toggleElement.querySelector('.neo-toggle__input');
    if (!toggleInput) return;
    
    // Obtener tema guardado
    const savedTheme = localStorage.getItem('neo-brutalist-theme');
    
    // Establecer estado inicial
    if (savedTheme === 'dark') {
      toggleInput.checked = true;
      this.isDarkMode = true;
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      toggleInput.checked = false;
      this.isDarkMode = false;
      document.documentElement.setAttribute('data-theme', 'light');
    }
    
    // Agregar listener para cambios
    toggleInput.addEventListener('change', () => {
      this.toggleTheme();
    });
    
    console.log('🎨 Funcionalidad del toggle configurada');
  }

  /**
   * Animación del toggle
   */
  animateToggle() {
    const toggle = document.querySelector('.neo-toggle__slider');
    if (toggle) {
      toggle.style.transform = 'scale(1.1)';
      setTimeout(() => {
        toggle.style.transform = '';
      }, 200);
    }
  }

  /**
   * Inicializar componentes existentes
   */
  initializeComponents() {
    this.convertButtons();
    this.convertCards();
    this.convertInputs();
    this.addHoverEffects();
  }

  /**
   * Convertir botones existentes a estilo Neo Brutalist
   */
  convertButtons() {
    const buttons = document.querySelectorAll('button, .back-btn, .logo');
    
    buttons.forEach(button => {
      if (!button.classList.contains('neo-button')) {
        button.classList.add('neo-button');
        
        // Mantener clases específicas
        if (button.classList.contains('back-btn')) {
          button.classList.add('neo-button--secondary');
        }
        if (button.classList.contains('logo')) {
          button.classList.add('neo-button--primary');
        }
      }
    });
  }

  /**
   * Convertir cards existentes a estilo Neo Brutalist
   */
  convertCards() {
    const cards = document.querySelectorAll('.folder-item, .file-item, .box, .article-content');
    
    cards.forEach(card => {
      if (!card.classList.contains('neo-card')) {
        card.classList.add('neo-card');
        
        // Agregar título si no existe
        const title = card.querySelector('h3, .folder-label, .file-name');
        if (title && !card.querySelector('.neo-card__title')) {
          const titleElement = document.createElement('div');
          titleElement.className = 'neo-card__title';
          titleElement.textContent = title.textContent;
          card.insertBefore(titleElement, card.firstChild);
        }
        
        // Agregar contenido si no existe
        const content = card.querySelector('p, .file-description');
        if (content && !card.querySelector('.neo-card__content')) {
          const contentElement = document.createElement('div');
          contentElement.className = 'neo-card__content';
          contentElement.textContent = content.textContent;
          card.appendChild(contentElement);
        }
      }
    });
  }

  /**
   * Convertir inputs existentes a estilo Neo Brutalist
   */
  convertInputs() {
    const inputs = document.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
      if (!input.classList.contains('neo-input')) {
        input.classList.add('neo-input');
      }
    });
  }

  /**
   * Agregar efectos hover a elementos
   */
  addHoverEffects() {
    const elements = document.querySelectorAll('.folder-item, .file-item, .box');
    
    elements.forEach(element => {
      element.addEventListener('mouseenter', () => {
        element.style.transform = 'translate(2px, 2px)';
      });
      
      element.addEventListener('mouseleave', () => {
        element.style.transform = '';
      });
    });
  }

  /**
   * Configurar event listeners globales
   */
  setupEventListeners() {
    // Efecto de clic en botones
    document.addEventListener('click', (e) => {
      if (e.target.matches('.neo-button, button')) {
        this.animateClick(e.target);
      }
    });

    // Efecto de hover en cards
    document.addEventListener('mouseenter', (e) => {
      if (e.target.matches('.neo-card, .folder-item, .file-item')) {
        this.animateHover(e.target);
      }
    }, true);

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
      }
    });

    document.addEventListener('mousedown', () => {
      document.body.classList.remove('keyboard-navigation');
    });
  }

  /**
   * Animación de clic
   */
  animateClick(element) {
    element.style.transform = 'translate(0, 0)';
    element.style.boxShadow = '2px 2px 0 var(--shadow-color)';
    
    setTimeout(() => {
      element.style.transform = '';
      element.style.boxShadow = '';
    }, 150);
  }

  /**
   * Animación de hover
   */
  animateHover(element) {
    element.style.transition = 'all 0.2s ease';
  }

  /**
   * Crear componente dinámicamente
   */
  createComponent(type, props = {}) {
    const container = document.createElement('div');
    
    switch (type) {
      case 'button':
        container.innerHTML = this.createButton(props);
        break;
      case 'card':
        container.innerHTML = this.createCard(props);
        break;
      case 'input':
        container.innerHTML = this.createInput(props);
        break;
      case 'toggle':
        container.innerHTML = this.createToggle(props);
        break;
      default:
        console.warn(`Component type "${type}" not found`);
    }
    
    return container.firstElementChild;
  }

  /**
   * Crear botón Neo Brutalist
   */
  createButton(props = {}) {
    const {
      text = 'Neo Button',
      variant = 'primary',
      size = 'medium',
      disabled = false
    } = props;
    
    const classes = [
      'neo-button',
      `neo-button--${variant}`,
      `neo-button--${size}`,
      disabled ? 'neo-disabled' : ''
    ].filter(Boolean).join(' ');
    
    return `<button class="${classes}" ${disabled ? 'disabled' : ''}>${text}</button>`;
  }

  /**
   * Crear card Neo Brutalist
   */
  createCard(props = {}) {
    const {
      title = 'Sample Card',
      content = 'A raw, functional Neo Brutalist card.',
      variant = 'default'
    } = props;
    
    return `
      <div class="neo-card neo-card--${variant}">
        <div class="neo-card__title">${title}</div>
        <div class="neo-card__content">${content}</div>
      </div>
    `;
  }

  /**
   * Crear input Neo Brutalist
   */
  createInput(props = {}) {
    const {
      type = 'text',
      placeholder = 'Type here...',
      value = '',
      disabled = false
    } = props;
    
    return `
      <input 
        type="${type}" 
        class="neo-input" 
        placeholder="${placeholder}" 
        value="${value}"
        ${disabled ? 'disabled' : ''}
      >
    `;
  }

  /**
   * Crear toggle Neo Brutalist
   */
  createToggle(props = {}) {
    const {
      label = 'modo oscuro',
      checked = false,
      onChange = null
    } = props;
    
    return `
      <label class="neo-toggle">
        <span class="neo-toggle__text">${label}</span>
        <input type="checkbox" class="neo-toggle__input" ${checked ? 'checked' : ''}>
        <span class="neo-toggle__slider"></span>
      </label>
    `;
  }

  /**
   * Aplicar tema a elementos específicos
   */
  applyThemeToElement(element) {
    if (this.isDarkMode) {
      element.classList.add('neo-dark');
    } else {
      element.classList.remove('neo-dark');
    }
  }

  /**
   * Obtener estado del tema
   */
  getTheme() {
    return this.isDarkMode ? 'dark' : 'light';
  }

  /**
   * Forzar tema específico
   */
  setTheme(theme) {
    this.isDarkMode = theme === 'dark';
    this.applyTheme();
    localStorage.setItem('neo-brutalist-theme', theme);
  }
}

/**
 * Utilidades adicionales
 */
const NeoUtils = {
  /**
   * Crear grid de componentes
   */
  createGrid(items, columns = 3) {
    const grid = document.createElement('div');
    grid.className = `neo-grid neo-grid--${columns}`;
    
    items.forEach(item => {
      const gridItem = document.createElement('div');
      gridItem.appendChild(item);
      grid.appendChild(gridItem);
    });
    
    return grid;
  },

  /**
   * Crear navegación
   */
  createNavigation(links) {
    const nav = document.createElement('nav');
    nav.className = 'neo-nav';
    
    const list = document.createElement('ul');
    list.className = 'neo-nav__list';
    
    links.forEach(link => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = link.href || '#';
      a.textContent = link.text;
      a.className = 'neo-nav__link';
      li.appendChild(a);
      list.appendChild(li);
    });
    
    nav.appendChild(list);
    return nav;
  },

  /**
   * Animar entrada de elementos
   */
  animateIn(element, delay = 0) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
      element.style.transition = 'all 0.5s ease';
      element.style.opacity = '1';
      element.style.transform = 'translateY(0)';
    }, delay);
  },

  /**
   * Crear efecto de escritura
   */
  typeWriter(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    
    const timer = setInterval(() => {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        i++;
      } else {
        clearInterval(timer);
      }
    }, speed);
  }
};

/**
 * Inicializar sistema cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', () => {
  window.NeoBrutalist = new NeoBrutalistSystem();
  window.NeoUtils = NeoUtils;
});

/**
 * Exportar para uso en módulos
 */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { NeoBrutalistSystem, NeoUtils };
}
