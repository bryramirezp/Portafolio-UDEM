/**
 * HEADER NEO BRUTALIST COMPONENT
 * Componente reutilizable para todas las páginas
 */

class NeoHeader {
  constructor(options = {}) {
    this.options = {
      title: 'Portafolio UDEM',
      subtitle: 'Integración de Aplicaciones Computacionales',
      showLogo: true,
      showThemeToggle: true,
      showBackButton: false,
      backButtonText: '← Volver',
      backButtonHref: '#',
      ...options
    };
    
    this.element = this.create();
  }

  /**
   * Crear el elemento header
   */
  create() {
    const header = document.createElement('header');
    header.className = 'neo-header';
    
    header.innerHTML = `
      <div class="neo-header__left">
        ${this.options.showLogo ? this.createLogo() : ''}
        ${this.options.showBackButton ? this.createBackButton() : ''}
      </div>
      <div class="neo-header__center">
        <h1 class="neo-header__title">${this.options.title}</h1>
        ${this.options.subtitle ? `<p class="neo-header__subtitle">${this.options.subtitle}</p>` : ''}
      </div>
      <div class="neo-header__right">
        ${this.options.showThemeToggle ? '<div class="neo-header__theme-toggle"></div>' : ''}
        <!-- Espacio para elementos adicionales -->
      </div>
    `;
    
    return header;
  }

  /**
   * Crear logo UDEM
   */
  createLogo() {
    return `<span class="neo-button neo-button--primary">#UDEM</span>`;
  }

  /**
   * Crear botón de regreso
   */
  createBackButton() {
    return `
      <a href="${this.options.backButtonHref}" class="neo-button neo-button--secondary">
        ${this.options.backButtonText}
      </a>
    `;
  }

  /**
   * Renderizar en el DOM
   */
  render(container) {
    if (typeof container === 'string') {
      container = document.querySelector(container);
    }
    
    if (container) {
      container.appendChild(this.element);
    }
    
    return this.element;
  }

  /**
   * Actualizar título
   */
  updateTitle(title) {
    const titleElement = this.element.querySelector('.neo-header__title');
    if (titleElement) {
      titleElement.textContent = title;
    }
  }

  /**
   * Actualizar subtítulo
   */
  updateSubtitle(subtitle) {
    const subtitleElement = this.element.querySelector('.neo-header__subtitle');
    if (subtitleElement) {
      subtitleElement.textContent = subtitle;
    }
  }

  /**
   * Agregar elemento a la sección derecha
   */
  addToRight(element) {
    const rightSection = this.element.querySelector('.neo-header__right');
    if (rightSection) {
      rightSection.appendChild(element);
    }
  }

  /**
   * Agregar elemento a la sección izquierda
   */
  addToLeft(element) {
    const leftSection = this.element.querySelector('.neo-header__left');
    if (leftSection) {
      leftSection.appendChild(element);
    }
  }

  /**
   * Obtener el elemento DOM
   */
  getElement() {
    return this.element;
  }
}

/**
 * FACTORY PARA CREAR HEADERS ESPECÍFICOS
 */
const NeoHeaderFactory = {
  /**
   * Header para página principal
   */
  createMainHeader() {
    return new NeoHeader({
      title: 'Portafolio de Tareas',
      subtitle: 'Integración de Aplicaciones Computacionales',
      showLogo: true,
      showThemeToggle: true,
      showBackButton: false
    });
  },

  /**
   * Header para páginas de categorías
   */
  createCategoryHeader(title, backHref = '../index.html') {
    return new NeoHeader({
      title: title,
      subtitle: '',
      showLogo: false,
      showThemeToggle: true,
      showBackButton: true,
      backButtonText: '← Volver',
      backButtonHref: backHref
    });
  },

  /**
   * Header para páginas de contenido
   */
  createContentHeader(title, backHref) {
    return new NeoHeader({
      title: title,
      subtitle: '',
      showLogo: false,
      showThemeToggle: true,
      showBackButton: true,
      backButtonText: '← Volver',
      backButtonHref: backHref
    });
  },

  /**
   * Header para ejercicios guiados
   */
  createExerciseHeader(exerciseNumber, exerciseTitle) {
    return new NeoHeader({
      title: `Ejercicio Guiado ${exerciseNumber}`,
      subtitle: exerciseTitle,
      showLogo: false,
      showThemeToggle: true,
      showBackButton: true,
      backButtonText: '← Volver a Ejercicios',
      backButtonHref: '../ejercicios-guiados.html'
    });
  },

  /**
   * Header para tareas
   */
  createTaskHeader(taskNumber, taskTitle) {
    return new NeoHeader({
      title: `Tarea ${taskNumber}`,
      subtitle: taskTitle,
      showLogo: false,
      showThemeToggle: true,
      showBackButton: true,
      backButtonText: '← Volver a Tareas',
      backButtonHref: '../tareas.html'
    });
  },

  /**
   * Header para parciales
   */
  createPartialHeader(partialNumber, partialTitle) {
    return new NeoHeader({
      title: `Parcial ${partialNumber}`,
      subtitle: partialTitle,
      showLogo: false,
      showThemeToggle: true,
      showBackButton: true,
      backButtonText: '← Volver a Parciales',
      backButtonHref: '../parciales.html'
    });
  },

  /**
   * Header para proyecto final
   */
  createProjectHeader(projectTitle) {
    return new NeoHeader({
      title: 'Proyecto Final',
      subtitle: projectTitle,
      showLogo: false,
      showThemeToggle: true,
      showBackButton: true,
      backButtonText: '← Volver',
      backButtonHref: '../index.html'
    });
  }
};

/**
 * FUNCIONES UTILITARIAS PARA HEADERS
 */
const NeoHeaderUtils = {
  /**
   * Reemplazar header existente
   */
  replaceExistingHeader(newHeader) {
    const existingHeader = document.querySelector('.neo-header, .file-system-header, .folder-page-header');
    if (existingHeader) {
      existingHeader.parentNode.replaceChild(newHeader.getElement(), existingHeader);
    } else {
      document.body.insertBefore(newHeader.getElement(), document.body.firstChild);
    }
  },

  /**
   * Convertir header existente a Neo Brutalist
   */
  convertExistingHeader() {
    const existingHeader = document.querySelector('.file-system-header, .folder-page-header');
    if (existingHeader) {
      existingHeader.classList.add('neo-header');
      
      // Convertir elementos existentes
      const logo = existingHeader.querySelector('.logo');
      if (logo) {
        logo.classList.add('neo-button', 'neo-button--primary');
      }
      
      const backBtn = existingHeader.querySelector('.back-btn');
      if (backBtn) {
        backBtn.classList.add('neo-button', 'neo-button--secondary');
      }
      
      const title = existingHeader.querySelector('h1, .folder-title');
      if (title) {
        title.classList.add('neo-header__title');
      }
    }
  },

  /**
   * Crear breadcrumb navigation
   */
  createBreadcrumb(items) {
    const breadcrumb = document.createElement('nav');
    breadcrumb.className = 'neo-nav';
    
    const list = document.createElement('ul');
    list.className = 'neo-nav__list';
    
    items.forEach((item, index) => {
      const li = document.createElement('li');
      
      if (index === items.length - 1) {
        // Último elemento sin enlace
        li.innerHTML = `<span class="neo-nav__link" style="color: var(--text-secondary);">${item.text}</span>`;
      } else {
        const a = document.createElement('a');
        a.href = item.href || '#';
        a.textContent = item.text;
        a.className = 'neo-nav__link';
        li.appendChild(a);
      }
      
      list.appendChild(li);
    });
    
    breadcrumb.appendChild(list);
    return breadcrumb;
  }
};

/**
 * EXPORTAR PARA USO GLOBAL
 */
if (typeof window !== 'undefined') {
  window.NeoHeader = NeoHeader;
  window.NeoHeaderFactory = NeoHeaderFactory;
  window.NeoHeaderUtils = NeoHeaderUtils;
}

/**
 * EXPORTAR PARA MÓDULOS
 */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { NeoHeader, NeoHeaderFactory, NeoHeaderUtils };
}
