/**
 * MAIN.JS - SISTEMA PRINCIPAL NEO BRUTALIST
 * Funcionalidades principales del portafolio
 */

// ========================================
// CONFIGURACIÓN INICIAL
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎨 Neo Brutalist Portfolio System Loading...');
    
    // Inicializar sistema principal
    initializePortfolioSystem();
    
    // Configurar navegación
    setupNavigation();
    
    // Configurar efectos especiales
    setupSpecialEffects();
    
    // Configurar analytics (opcional)
    setupAnalytics();
    
    console.log('✅ Neo Brutalist Portfolio System Ready!');
});

// ========================================
// SISTEMA PRINCIPAL DEL PORTAFOLIO
// ========================================

function initializePortfolioSystem() {
    // Esperar a que el sistema Neo Brutalist esté listo
    if (window.NeoBrutalist) {
        console.log('🎨 Neo Brutalist System detected');
        
        // Configurar tema inicial
        const savedTheme = localStorage.getItem('neo-brutalist-theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
        }
        
        // Agregar clase de inicialización
        document.body.classList.add('neo-portfolio-loaded');
        
        // NO crear toggle aquí - dejar que neo-brutalist.js lo maneje
        // Solo limpiar toggles duplicados si es necesario
        cleanupDuplicateToggles();
        
        // Animar entrada de elementos
        animatePageLoad();
    } else {
        console.warn('⚠️ Neo Brutalist System not found, retrying...');
        setTimeout(initializePortfolioSystem, 100);
    }
}

function cleanupDuplicateToggles() {
    // Encontrar todos los toggles existentes
    const allToggles = document.querySelectorAll('.neo-toggle');
    
    if (allToggles.length > 1) {
        console.log(`🧹 Limpiando ${allToggles.length - 1} toggles duplicados`);
        
        // Mantener solo el último toggle (el más reciente)
        for (let i = 0; i < allToggles.length - 1; i++) {
            allToggles[i].remove();
        }
    }
    
    // También limpiar cualquier toggle en la sección izquierda del header
    const leftSection = document.querySelector('.neo-header__left');
    if (leftSection) {
        const leftToggles = leftSection.querySelectorAll('.neo-toggle');
        leftToggles.forEach(toggle => toggle.remove());
    }
}

// Función eliminada - ahora se maneja en neo-brutalist.js

// Función eliminada - ahora se maneja en neo-brutalist.js

function animateThemeChange(isDark) {
    // Efecto de transición suave
    document.body.style.transition = 'all 0.3s ease';
    
    // Pequeño efecto visual en el toggle
    const toggle = document.querySelector('.neo-toggle');
    if (toggle) {
        toggle.style.transform = 'scale(1.05)';
        setTimeout(() => {
            toggle.style.transform = '';
        }, 150);
    }
    
    // Efecto en las cards
    const cards = document.querySelectorAll('.neo-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.transform = 'translateY(-2px)';
            setTimeout(() => {
                card.style.transform = '';
            }, 100);
        }, index * 50);
    });
}

// ========================================
// NAVEGACIÓN Y RUTAS
// ========================================

function setupNavigation() {
    // Configurar navegación de carpetas
    const folderCards = document.querySelectorAll('.neo-card[onclick*="openFolder"]');
    folderCards.forEach(card => {
        card.addEventListener('click', (e) => {
            e.preventDefault();
            const folderName = card.getAttribute('onclick').match(/'([^']+)'/)[1];
            navigateToFolder(folderName);
        });
        
        // Agregar efecto de hover mejorado
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translate(2px, 2px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
    
    // Configurar navegación de archivos
    const fileItems = document.querySelectorAll('.file-item');
    fileItems.forEach(item => {
        item.addEventListener('click', (e) => {
            // Agregar efecto de clic
            item.classList.add('neo-loading');
            setTimeout(() => {
                item.classList.remove('neo-loading');
            }, 500);
        });
    });
    
    // Configurar botones de regreso
    const backButtons = document.querySelectorAll('.back-btn');
    backButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            // Agregar efecto de navegación
            document.body.style.opacity = '0.8';
            setTimeout(() => {
                document.body.style.opacity = '1';
            }, 200);
        });
    });
}

// ========================================
// FUNCIONES DE NAVEGACIÓN
// ========================================

function navigateToFolder(folderName) {
    // Agregar efecto de transición
    const main = document.querySelector('main');
    if (main) {
        main.style.transform = 'translateX(-20px)';
        main.style.opacity = '0.7';
    }
    
    // Navegar después de un breve delay
    setTimeout(() => {
        window.location.href = `Integ_aplicaciones_computacion/${folderName}.html`;
    }, 200);
}

function navigateToFile(filePath) {
    // Efecto de carga
    showLoadingEffect();
    
    setTimeout(() => {
        window.location.href = filePath;
    }, 300);
}

// ========================================
// EFECTOS ESPECIALES
// ========================================

function setupSpecialEffects() {
    // Efecto de escritura en títulos
    const titles = document.querySelectorAll('.neo-header__title');
    titles.forEach(title => {
        if (title.textContent.includes('Portafolio')) {
            typeWriterEffect(title, title.textContent, 100);
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
    
    // Efecto de parallax sutil en scroll - DESHABILITADO para mantener header fijo
    // setupParallaxEffect();
    
    // Efectos de hover mejorados
    setupEnhancedHoverEffects();
}

function animatePageLoad() {
    // Animación de entrada de la página
    document.body.style.opacity = '0';
    document.body.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        document.body.style.transition = 'all 0.6s ease';
        document.body.style.opacity = '1';
        document.body.style.transform = 'translateY(0)';
    }, 100);
}

function typeWriterEffect(element, text, speed = 50) {
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

// Función deshabilitada - causaba que el header se moviera con el scroll
/*
function setupParallaxEffect() {
    let ticking = false;
    
    function updateParallax() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.neo-header');
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
}
*/

function setupEnhancedHoverEffects() {
    // Efectos especiales para cards
    const cards = document.querySelectorAll('.neo-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            // Efecto de brillo
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

// ========================================
// SISTEMA DE CARGA
// ========================================

function showLoadingEffect() {
    const loader = document.createElement('div');
    loader.className = 'neo-loading-overlay';
    loader.innerHTML = `
        <div class="neo-loading-spinner">
            <div class="neo-spinner"></div>
            <p>Cargando...</p>
        </div>
    `;
    
    // Estilos del loader
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        color: white;
        font-family: 'Roboto Mono', monospace;
    `;
    
    document.body.appendChild(loader);
    
    // Remover después de 2 segundos
    setTimeout(() => {
        if (loader.parentNode) {
            loader.parentNode.removeChild(loader);
        }
    }, 2000);
}

// ========================================
// ANALYTICS Y MÉTRICAS
// ========================================

function setupAnalytics() {
    // Trackear clics en elementos importantes
    const trackableElements = document.querySelectorAll('.neo-card, .neo-button, .file-item');
    
    trackableElements.forEach(element => {
        element.addEventListener('click', (e) => {
            const elementType = element.classList.contains('neo-card') ? 'card' : 
                              element.classList.contains('neo-button') ? 'button' : 'file';
            
            trackEvent('click', elementType, element.textContent.trim());
        });
    });
    
    // Trackear cambios de tema
    if (window.NeoBrutalist) {
        const originalToggleTheme = window.NeoBrutalist.toggleTheme;
        window.NeoBrutalist.toggleTheme = function() {
            const newTheme = this.isDarkMode ? 'light' : 'dark';
            trackEvent('theme_change', 'toggle', newTheme);
            return originalToggleTheme.call(this);
        };
    }
}

function trackEvent(action, category, label) {
    // Implementar tracking aquí (Google Analytics, etc.)
    console.log(`📊 Event tracked: ${action} - ${category} - ${label}`);
    
    // Ejemplo para Google Analytics
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            event_category: category,
            event_label: label
        });
    }
}

// ========================================
// UTILIDADES DEL PORTAFOLIO
// ========================================

const PortfolioUtils = {
    /**
     * Obtener información de la página actual
     */
    getCurrentPageInfo() {
        const path = window.location.pathname;
        const segments = path.split('/').filter(Boolean);
        
        return {
            isMainPage: segments.length === 0 || segments[segments.length - 1] === 'index.html',
            category: segments[segments.length - 2] || null,
            page: segments[segments.length - 1] || 'index.html',
            fullPath: path
        };
    },
    
    /**
     * Crear breadcrumb navigation
     */
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
    },
    
    /**
     * Obtener estadísticas del sitio
     */
    getSiteStats() {
        const cards = document.querySelectorAll('.neo-card').length;
        const buttons = document.querySelectorAll('.neo-button').length;
        const theme = localStorage.getItem('neo-brutalist-theme') || 'light';
        
        return {
            totalCards: cards,
            totalButtons: buttons,
            currentTheme: theme,
            loadTime: performance.now()
        };
    },
    
    /**
     * Exportar configuración del usuario
     */
    exportUserSettings() {
        const settings = {
            theme: localStorage.getItem('neo-brutalist-theme') || 'light',
            lastVisit: new Date().toISOString(),
            preferences: {
                animations: true,
                sounds: false,
                notifications: true
            }
        };
        
        const blob = new Blob([JSON.stringify(settings, null, 2)], {
            type: 'application/json'
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'neo-brutalist-settings.json';
        a.click();
        
        URL.revokeObjectURL(url);
    }
};

// ========================================
// FUNCIONES GLOBALES
// ========================================

// Mantener función original para compatibilidad
function openFolder(folderName) {
    navigateToFolder(folderName);
}

// Exportar utilidades globalmente
window.PortfolioUtils = PortfolioUtils;

// ========================================
// MANEJO DE ERRORES
// ========================================

window.addEventListener('error', (e) => {
    console.error('🚨 Error en Neo Brutalist Portfolio:', e.error);
    
    // Enviar error a analytics si está disponible
    if (typeof gtag !== 'undefined') {
        gtag('event', 'exception', {
            description: e.error.message,
            fatal: false
        });
    }
});

// ========================================
// OPTIMIZACIONES DE PERFORMANCE
// ========================================

// Lazy loading para imágenes
function setupLazyLoading() {
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

// Inicializar lazy loading si hay imágenes
document.addEventListener('DOMContentLoaded', () => {
    if ('IntersectionObserver' in window) {
        setupLazyLoading();
    }
});

// ========================================
// EXPORTAR PARA MÓDULOS
// ========================================

// ========================================
// EASTER EGG: FRENCH FRIES SYSTEM 🍟
// ========================================

// Configuración de las papas fritas
const FRIES_CONFIG = {
    count: 30,
    colors: {
        golden: '#FFD700',      // Dorado
        lightGolden: '#FFA500', // Dorado claro
        darkGolden: '#DAA520',  // Dorado oscuro
        crispy: '#CD853F',      // Crujiente
        shadow: '#8B4513'       // Sombra
    },
    gravity: 0.4,
    drag: 0.08,
    terminalVelocity: 4,
    rotationSpeed: 0.05,
    bounce: 0.6
};

// Variables globales de las papas fritas
let friesCanvas = null;
let friesCtx = null;
let friesParticles = [];
let friesAnimationId = null;

/**
 * Inicializar el sistema de papas fritas 🍟
 */
function initFriesSystem() {
    // Crear canvas para las papas fritas
    friesCanvas = document.createElement('canvas');
    friesCanvas.id = 'fries-canvas';
    friesCanvas.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    document.body.appendChild(friesCanvas);
    friesCtx = friesCanvas.getContext('2d');
    
    // Configurar canvas
    resizeFriesCanvas();
    
    // Configurar el botón UDEM
    setupUDEMButton();
    
    // Listener para resize
    window.addEventListener('resize', resizeFriesCanvas);
    
    console.log('🍟 French Fries system initialized!');
}

/**
 * Configurar el botón UDEM para activar el confeti
 */
function setupUDEMButton() {
    const udemButton = document.querySelector('.neo-button--primary');
    
    if (udemButton && udemButton.textContent.includes('#UDEM')) {
        // Agregar clase para identificación
        udemButton.classList.add('udem-easter-egg');
        
        // Agregar evento de clic
        udemButton.addEventListener('click', (e) => {
            e.preventDefault();
            triggerFries();
        });
        
        // Agregar efecto visual especial
        udemButton.addEventListener('mouseenter', () => {
            udemButton.style.transform = 'translate(2px, 2px) scale(1.05)';
            udemButton.style.boxShadow = 'var(--shadow-offset-hover) var(--shadow-offset-hover) 0 var(--shadow-color), 0 0 20px rgba(255, 215, 0, 0.4)';
        });
        
        udemButton.addEventListener('mouseleave', () => {
            udemButton.style.transform = '';
            udemButton.style.boxShadow = '';
        });
        
        console.log('🍟 UDEM button configured for french fries!');
    }
}

/**
 * Clase para papas fritas 🍟
 */
class FrenchFry {
    constructor(x, y) {
        this.randomModifier = Math.random() * 99;
        
        // Dimensiones variables para papas fritas más realistas
        this.length = Math.random() * 15 + 20; // 20-35px de largo
        this.width = Math.random() * 3 + 2;    // 2-5px de ancho
        
        this.position = { x, y };
        this.rotation = Math.random() * 2 * Math.PI;
        this.rotationSpeed = (Math.random() - 0.5) * FRIES_CONFIG.rotationSpeed;
        
        // Velocidad inicial
        this.velocity = this.initVelocity();
        
        // Color aleatorio de papas fritas
        const colorKeys = Object.keys(FRIES_CONFIG.colors);
        this.color = FRIES_CONFIG.colors[colorKeys[Math.floor(Math.random() * (colorKeys.length - 1))]];
        this.shadowColor = FRIES_CONFIG.colors.shadow;
        
        // Propiedades físicas
        this.bounce = FRIES_CONFIG.bounce;
        this.hasBounced = false;
        this.life = 1.0; // Para efecto de desvanecimiento
    }
    
    initVelocity() {
        // Velocidad más realista para papas fritas
        const x = (Math.random() - 0.5) * 12;
        const y = Math.random() * 8 + 4;
        return { x, y: -y };
    }
    
    update() {
        // Aplicar fuerzas físicas
        this.velocity.x -= this.velocity.x * FRIES_CONFIG.drag;
        this.velocity.y = Math.min(this.velocity.y + FRIES_CONFIG.gravity, FRIES_CONFIG.terminalVelocity);
        
        // Movimiento aleatorio sutil
        this.velocity.x += (Math.random() - 0.5) * 0.5;
        
        // Actualizar posición
        this.position.x += this.velocity.x;
        this.position.y += this.velocity.y;
        
        // Rotación continua
        this.rotation += this.rotationSpeed;
        
        // Rebote en el suelo
        if (this.position.y >= friesCanvas.height - this.length && !this.hasBounced) {
            this.velocity.y *= -this.bounce;
            this.velocity.x *= 0.8; // Reducir velocidad horizontal al rebotar
            this.hasBounced = true;
        }
        
        // Reducir vida gradualmente
        this.life -= 0.002;
    }
    
    draw(ctx) {
        ctx.save();
        
        // Mover al centro de la papa frita
        ctx.translate(this.position.x, this.position.y);
        ctx.rotate(this.rotation);
        
        // Aplicar transparencia basada en la vida
        ctx.globalAlpha = this.life;
        
        // Dibujar sombra
        ctx.fillStyle = this.shadowColor;
        ctx.fillRect(-this.width/2 + 1, -this.length/2 + 1, this.width, this.length);
        
        // Dibujar la papa frita principal
        ctx.fillStyle = this.color;
        ctx.fillRect(-this.width/2, -this.length/2, this.width, this.length);
        
        // Añadir detalles de textura
        ctx.fillStyle = this.shadowColor;
        ctx.fillRect(-this.width/2, -this.length/2, this.width, 1);
        ctx.fillRect(-this.width/2, this.length/2 - 1, this.width, 1);
        
        // Restaurar contexto
        ctx.restore();
    }
}

/**
 * Activar las papas fritas 🍟
 */
function triggerFries() {
    console.log('🍟 French Fries triggered!');
    
    // Mostrar canvas
    friesCanvas.style.opacity = '1';
    
    // Crear papas fritas desde el botón UDEM
    const udemButton = document.querySelector('.udem-easter-egg');
    if (udemButton) {
        const rect = udemButton.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        // Crear papas fritas
        for (let i = 0; i < FRIES_CONFIG.count; i++) {
            friesParticles.push(new FrenchFry(centerX, centerY));
        }
    }
    
    // Iniciar animación
    if (!friesAnimationId) {
        animateFries();
    }
    
    // Ocultar después de 5 segundos (más tiempo para disfrutar las papas)
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
    
    // Trackear el easter egg
    trackEvent('easter_egg', 'french_fries', 'udem_button');
}

/**
 * Animar las papas fritas 🍟
 */
function animateFries() {
    // Limpiar canvas
    friesCtx.clearRect(0, 0, friesCanvas.width, friesCanvas.height);
    
    // Dibujar cada papa frita
    friesParticles.forEach((fry, index) => {
        // Actualizar física
        fry.update();
        
        // Dibujar la papa frita
        fry.draw(friesCtx);
        
        // Remover papas fritas que se desvanecen o salen de pantalla
        if (fry.life <= 0 || fry.position.y > friesCanvas.height + 50) {
            friesParticles.splice(index, 1);
        }
    });
    
    // Continuar animación si hay papas fritas
    if (friesParticles.length > 0) {
        friesAnimationId = requestAnimationFrame(animateFries);
    } else {
        friesAnimationId = null;
    }
}

/**
 * Redimensionar canvas de papas fritas
 */
function resizeFriesCanvas() {
    if (friesCanvas) {
        friesCanvas.width = window.innerWidth;
        friesCanvas.height = window.innerHeight;
    }
}

// Inicializar sistema de papas fritas cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Esperar un poco para que el sistema principal se inicialice
    setTimeout(initFriesSystem, 500);
});

// ========================================
// EXPORTAR PARA MÓDULOS
// ========================================
