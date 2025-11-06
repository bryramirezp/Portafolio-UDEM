/**
 * ========================================
 * SISTEMA CONSOLIDADO DEL PORTAFOLIO NEO BRUTALIST
 * * Combina la librería 'neo-brutalist.js' y la lógica
 * específica del sitio 'main.js' en un solo archivo.
 * ========================================
 */

class NeoBrutalistSystem {
  constructor() {
    this.isDarkMode = false;
    this.init();
  }

  /**
   * Inicializar el sistema completo
   */
  init() {
    console.log('🎨 Neo Brutalist Portfolio System Loading...');
    
    // 1. Cargar tema
    this.loadTheme();
    
    // 2. Crear el toggle de tema (solo uno)
    this.createThemeToggle();
    
    // 3. Convertir HTML existente
    this.initializeComponents();
    
    // 4. Configurar listeners de teclado/ratón
    this.setupGlobalEventListeners();
    
    // 5. Configurar lógica específica del portafolio (de main.js)
    this.setupNavigation();
    this.setupSpecialEffects();
    this.setupEnhancedHoverEffects(); // Reemplaza los listeners genéricos
    this.setupAnalytics();
    this.setupLazyLoading();
    this.setupGlobalErrorHandler();
    
    // 6. Añadir clase de inicialización
    document.body.classList.add('neo-portfolio-loaded');
    
    // 7. Animar entrada de elementos
    this.animatePageLoad();
    
    // 8. Exponer utilidades
    window.PortfolioUtils = this;

    console.log('✅ Neo Brutalist Portfolio System Ready!');
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

    // Trackear el evento
    const newTheme = this.isDarkMode ? 'dark' : 'light';
    this.trackEvent('theme_change', 'toggle', newTheme);
  }

  /**
   * Crear toggle de tema en el header
   */
  createThemeToggle() {
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
      let rightSection = header.querySelector('.neo-header__right, .header-right');
      if (!rightSection) {
        // Si no existe la sección derecha, crearla
        rightSection = document.createElement('div');
        rightSection.className = 'neo-header__right';
        header.appendChild(rightSection);
        console.log('🎨 Sección derecha del header creada');
      }
      
      rightSection.appendChild(toggleContainer);
      this.setupToggleFunctionality(toggleContainer.querySelector('.neo-toggle'));
      console.log('🎨 Toggle creado exitosamente en el header');
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

    // Sincronizar estado
    toggleInput.checked = this.isDarkMode;

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
  }

  /**
   * Convertir botones existentes a estilo Neo Brutalist
   */
  convertButtons() {
    const buttons = document.querySelectorAll('button, .back-btn, .logo');
    buttons.forEach(button => {
      if (!button.classList.contains('neo-button')) {
        button.classList.add('neo-button');
        if (button.classList.contains('back-btn')) button.classList.add('neo-button--secondary');
        if (button.classList.contains('logo')) button.classList.add('neo-button--primary');
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
        
        // Adaptación de 'main.js': No duplicar títulos/contenido si 'neo-brutalist.js' ya los crea
        const title = card.querySelector('h3, .folder-label, .file-name');
        if (title && !card.querySelector('.neo-card__title')) {
          const titleElement = document.createElement('div');
          titleElement.className = 'neo-card__title';
          titleElement.textContent = title.textContent;
          card.insertBefore(titleElement, card.firstChild);
        }

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
   * Configurar event listeners globales (solo teclado/ratón)
   */
  setupGlobalEventListeners() {
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

  // ========================================
  // MÉTODOS DE 'main.js' INTEGRADOS
  // ========================================

  /**
   * Configurar navegación de carpetas y archivos
   */
  setupNavigation() {
    // Configurar navegación de carpetas
    const folderCards = document.querySelectorAll('.neo-card[onclick*="openFolder"]');
    folderCards.forEach(card => {
      card.addEventListener('click', (e) => {
        e.preventDefault();
        const folderName = card.getAttribute('onclick').match(/'([^']+)'/)[1];
        this.navigateToFolder(folderName);
      });
    });

    // Configurar navegación de archivos
    const fileItems = document.querySelectorAll('.file-item');
    fileItems.forEach(item => {
      item.addEventListener('click', (e) => {
        item.classList.add('neo-loading');
        setTimeout(() => item.classList.remove('neo-loading'), 500);
      });
    });

    // Configurar botones de regreso
    const backButtons = document.querySelectorAll('.back-btn');
    backButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        document.body.style.opacity = '0.8';
        setTimeout(() => document.body.style.opacity = '1', 200);
      });
    });
  }

  /**
   * Navegar a una carpeta con efecto
   */
  navigateToFolder(folderName) {
    const main = document.querySelector('main');
    if (main) {
      main.style.transform = 'translateX(-20px)';
      main.style.opacity = '0.7';
    }
    setTimeout(() => {
      window.location.href = `templates/${folderName}.html`;
    }, 200);
  }

  /**
   * Navegar a un archivo con efecto
   */
  navigateToFile(filePath) {
    this.showLoadingEffect();
    setTimeout(() => {
      window.location.href = filePath;
    }, 300);
  }

  /**
   * Configurar efectos especiales de carga
   */
  setupSpecialEffects() {
    // Efecto de escritura en títulos
    const titles = document.querySelectorAll('.neo-header__title');
    titles.forEach(title => {
      if (title.textContent.includes('Portafolio')) {
        this.typeWriterEffect(title, title.textContent, 100);
      }
    });

    // Efecto de aparición escalonada en cards
    const cards = document.querySelectorAll('.neo-card');
    cards.forEach((card, index) => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(30px)';
      setTimeout(() => {
        card.style.transition = 'all 0.5s ease';
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, index * 150);
    });
  }

  /**
   * Animación de entrada de la página
   */
  animatePageLoad() {
    document.body.style.opacity = '0';
    document.body.style.transform = 'translateY(20px)';
    setTimeout(() => {
      document.body.style.transition = 'all 0.6s ease';
      document.body.style.opacity = '1';
      document.body.style.transform = 'translateY(0)';
    }, 100);
  }

  /**
   * Efecto de máquina de escribir
   */
  typeWriterEffect(element, text, speed = 50) {
    element.textContent = '';
    let i = 0;
    const timer = setInterval(() => {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        i++;
      } else {
        clearInterval(timer);
      }
    }, speed);
  }

  /**
   * Configurar efectos hover/click mejorados (reemplaza los genéricos)
   */
  setupEnhancedHoverEffects() {
    // Efectos especiales para cards
    const cards = document.querySelectorAll('.neo-card');
    cards.forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.style.boxShadow = 'var(--shadow-offset-hover) var(--shadow-offset-hover) 0 var(--shadow-color), 0 0 20px rgba(255, 209, 102, 0.3)';
      });
      card.addEventListener('mouseleave', () => {
        card.style.boxShadow = '';
      });
    });

    // Efectos para botones
    const buttons = document.querySelectorAll('.neo-button');
    buttons.forEach(button => {
      button.addEventListener('mousedown', () => {
        button.style.transform = 'translate(0, 0)';
        button.style.boxShadow = '2px 2px 0 var(--shadow-color)';
      });
      button.addEventListener('mouseup', () => {
        button.style.transform = 'translate(2px, 2px)';
        button.style.boxShadow = 'var(--shadow-offset-hover) var(--shadow-offset-hover) 0 var(--shadow-color)';
      });
    });
  }

  /**
   * Mostrar efecto de carga
   */
  showLoadingEffect() {
    const loader = document.createElement('div');
    loader.className = 'neo-loading-overlay';
    loader.innerHTML = `<div class="neo-loading-spinner"><div class="neo-spinner"></div><p>Cargando...</p></div>`;
    loader.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.8); display: flex;
        justify-content: center; align-items: center; z-index: 9999;
        color: white; font-family: 'Roboto Mono', monospace;
    `;
    document.body.appendChild(loader);
    setTimeout(() => {
      if (loader.parentNode) loader.parentNode.removeChild(loader);
    }, 2000);
  }

  /**
   * Configurar sistema de Analytics
   */
  setupAnalytics() {
    const trackableElements = document.querySelectorAll('.neo-card, .neo-button, .file-item');
    trackableElements.forEach(element => {
      element.addEventListener('click', (e) => {
        const elementType = element.classList.contains('neo-card') ? 'card' :
          element.classList.contains('neo-button') ? 'button' : 'file';
        this.trackEvent('click', elementType, element.textContent.trim());
      });
    });
  }

  /**
   * Trackear evento
   */
  trackEvent(action, category, label) {
    console.log(`📊 Event tracked: ${action} - ${category} - ${label}`);
    if (typeof gtag !== 'undefined') {
      gtag('event', action, {
        event_category: category,
        event_label: label
      });
    }
  }

  /**
   * Configurar lazy loading para imágenes
   */
  setupLazyLoading() {
    if ('IntersectionObserver' in window) {
      const images = document.querySelectorAll('img[data-src]');
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            observer.unobserve(img);
          }
        });
      });
      images.forEach(img => imageObserver.observe(img));
    }
  }

  /**
   * Configurar manejo de errores global
   */
  setupGlobalErrorHandler() {
    window.addEventListener('error', (e) => {
      console.error('🚨 Error en Neo Brutalist Portfolio:', e.error);
      if (typeof gtag !== 'undefined') {
        gtag('event', 'exception', {
          description: e.error.message,
          fatal: false
        });
      }
    });
  }
  
  // ========================================
  // MÉTODOS DE 'PortfolioUtils' INTEGRADOS
  // ========================================

  getCurrentPageInfo() {
    const path = window.location.pathname;
    const segments = path.split('/').filter(Boolean);
    return {
      isMainPage: segments.length === 0 || segments[segments.length - 1] === 'index.html',
      category: segments[segments.length - 2] || null,
      page: segments[segments.length - 1] || 'index.html',
      fullPath: path
    };
  }

  createBreadcrumb() {
    const info = this.getCurrentPageInfo();
    const breadcrumb = [];
    if (!info.isMainPage) {
      breadcrumb.push({ text: 'Inicio', href: '../index.html' });
      if (info.category) {
        const categoryNames = {
          'ejercicios-guiados': 'Ejercicios Guiados',
          'tareas': 'Tareas',
          'parciales': 'Parciales',
          'proyecto-final': 'Proyecto Final'
        };
        breadcrumb.push({
          text: categoryNames[info.category] || info.category,
          href: `../${info.category}.html`
        });
      }
    }
    return breadcrumb;
  }
  
  getSiteStats() {
    return {
      totalCards: document.querySelectorAll('.neo-card').length,
      totalButtons: document.querySelectorAll('.neo-button').length,
      currentTheme: this.isDarkMode ? 'dark' : 'light',
      loadTime: performance.now()
    };
  }

  exportUserSettings() {
    const settings = {
      theme: localStorage.getItem('neo-brutalist-theme') || 'light',
      lastVisit: new Date().toISOString(),
      preferences: { animations: true, sounds: false, notifications: true }
    };
    const blob = new Blob([JSON.stringify(settings, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'neo-brutalist-settings.json';
    a.click();
    URL.revokeObjectURL(url);
  }
}

// ========================================
// FUNCIONES GLOBALES DE COMPATIBILIDAD
// ========================================

/**
 * Función global para 'onclick' de las carpetas
 */
function openFolder(folderName) {
    if (window.NeoBrutalist) {
        window.NeoBrutalist.navigateToFolder(folderName);
    } else {
        // Fallback por si acaso
        window.location.href = `templates/${folderName}.html`;
    }
}

// ========================================
// INICIALIZACIÓN DEL SISTEMA
// ========================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. Inicializar el sistema principal
  window.NeoBrutalist = new NeoBrutalistSystem();
  
  // 2. Inicializar el Easter Egg (se auto-inicializa después)
  setTimeout(initFriesSystem, 500);
});

// ========================================
// ========================================
// EASTER EGG: FRENCH FRIES SYSTEM 🍟
// (Se mantiene separado de la clase principal)
// ========================================
// ========================================

const FRIES_CONFIG = {
  count: 30,
  colors: {
    golden: '#FFD700',
    lightGolden: '#FFA500',
    darkGolden: '#DAA520',
    crispy: '#CD853F',
    shadow: '#8B4513'
  },
  gravity: 0.4,
  drag: 0.08,
  terminalVelocity: 4,
  rotationSpeed: 0.05,
  bounce: 0.6
};

let friesCanvas = null;
let friesCtx = null;
let friesParticles = [];
let friesAnimationId = null;

function initFriesSystem() {
  friesCanvas = document.createElement('canvas');
  friesCanvas.id = 'fries-canvas';
  friesCanvas.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none; z-index: 9999; opacity: 0;
      transition: opacity 0.3s ease;
  `;
  document.body.appendChild(friesCanvas);
  friesCtx = friesCanvas.getContext('2d');
  
  resizeFriesCanvas();
  setupUDEMButton();
  window.addEventListener('resize', resizeFriesCanvas);
  console.log('🍟 French Fries system initialized!');
}

function setupUDEMButton() {
  const udemButton = document.querySelector('.neo-button.neo-button--primary');
  if (udemButton && udemButton.textContent.includes('#UDEM')) {
    udemButton.classList.add('udem-easter-egg');
    udemButton.addEventListener('click', (e) => {
      e.preventDefault();
      triggerFries();
    });
    udemButton.addEventListener('mouseenter', () => {
      udemButton.style.transform = 'translate(2px, 2px) scale(1.05)';
      udemButton.style.boxShadow = 'var(--shadow-offset-hover) var(--shadow-offset-hover) 0 var(--shadow-color), 0 0 20px rgba(255, 215, 0, 0.4)';
    });
    udemButton.addEventListener('mouseleave', () => {
      udemButton.style.transform = '';
      udemButton.style.boxShadow = '';
    });
    console.log('🍟 UDEM button configured for french fries!');
  } else {
    console.log('🍟 UDEM button not found or does not contain #UDEM text');
  }
}

class FrenchFry {
  constructor(x, y) {
    this.randomModifier = Math.random() * 99;
    this.length = Math.random() * 15 + 20;
    this.width = Math.random() * 3 + 2;
    this.position = { x, y };
    this.rotation = Math.random() * 2 * Math.PI;
    this.rotationSpeed = (Math.random() - 0.5) * FRIES_CONFIG.rotationSpeed;
    this.velocity = this.initVelocity();
    const colorKeys = Object.keys(FRIES_CONFIG.colors);
    this.color = FRIES_CONFIG.colors[colorKeys[Math.floor(Math.random() * (colorKeys.length - 1))]];
    this.shadowColor = FRIES_CONFIG.colors.shadow;
    this.bounce = FRIES_CONFIG.bounce;
    this.hasBounced = false;
    this.life = 1.0;
  }
  
  initVelocity() {
    const x = (Math.random() - 0.5) * 12;
    const y = Math.random() * 8 + 4;
    return { x, y: -y };
  }
  
  update() {
    this.velocity.x -= this.velocity.x * FRIES_CONFIG.drag;
    this.velocity.y = Math.min(this.velocity.y + FRIES_CONFIG.gravity, FRIES_CONFIG.terminalVelocity);
    this.velocity.x += (Math.random() - 0.5) * 0.5;
    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
    this.rotation += this.rotationSpeed;
    if (this.position.y >= friesCanvas.height - this.length && !this.hasBounced) {
      this.velocity.y *= -this.bounce;
      this.velocity.x *= 0.8;
      this.hasBounced = true;
    }
    this.life -= 0.002;
  }
  
  draw(ctx) {
    ctx.save();
    ctx.translate(this.position.x, this.position.y);
    ctx.rotate(this.rotation);
    ctx.globalAlpha = this.life;
    ctx.fillStyle = this.shadowColor;
    ctx.fillRect(-this.width / 2 + 1, -this.length / 2 + 1, this.width, this.length);
    ctx.fillStyle = this.color;
    ctx.fillRect(-this.width / 2, -this.length / 2, this.width, this.length);
    ctx.fillStyle = this.shadowColor;
    ctx.fillRect(-this.width / 2, -this.length / 2, this.width, 1);
    ctx.fillRect(-this.width / 2, this.length / 2 - 1, this.width, 1);
    ctx.restore();
  }
}

function triggerFries() {
  console.log('🍟 French Fries triggered!');
  friesCanvas.style.opacity = '1';
  const udemButton = document.querySelector('.udem-easter-egg');
  if (udemButton) {
    const rect = udemButton.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    for (let i = 0; i < FRIES_CONFIG.count; i++) {
      friesParticles.push(new FrenchFry(centerX, centerY));
    }
  }
  if (!friesAnimationId) {
    animateFries();
  }
  setTimeout(() => {
    friesCanvas.style.opacity = '0';
    setTimeout(() => {
      friesParticles = [];
      if (friesAnimationId) {
        cancelAnimationFrame(friesAnimationId);
        friesAnimationId = null;
      }
    }, 300);
  }, 5000);
  
  // Trackear
  if (window.NeoBrutalist) {
      window.NeoBrutalist.trackEvent('easter_egg', 'french_fries', 'udem_button');
  }
}

function animateFries() {
  friesCtx.clearRect(0, 0, friesCanvas.width, friesCanvas.height);
  friesParticles.forEach((fry, index) => {
    fry.update();
    fry.draw(friesCtx);
    if (fry.life <= 0 || fry.position.y > friesCanvas.height + 50) {
      friesParticles.splice(index, 1);
    }
  });
  if (friesParticles.length > 0) {
    friesAnimationId = requestAnimationFrame(animateFries);
  } else {
    friesAnimationId = null;
  }
}

function resizeFriesCanvas() {
  if (friesCanvas) {
    friesCanvas.width = window.innerWidth;
    friesCanvas.height = window.innerHeight;
  }
}