/**
 * Tailwind Slider & Interactive Components
 * Funcionalidades:
 * - Slider de promoción (navegación, paginación, auto-advance)
 * - Feedback de carrito
 * - Newsletter subscription
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('✓ Tailwind Slider initialized');
    initSlider();
    initCartFeedback();
    initNewsletter();
});

/**
 * Inicializar Slider Promocional
 */
function initSlider() {
    const slider = document.getElementById('slider');
    const dots = document.querySelectorAll('.slider-dot');
    const prevBtn = document.getElementById('prevSlide');
    const nextBtn = document.getElementById('nextSlide');
    
    // Si no existe slider, salir sin error
    if (!slider || !dots.length) {
        console.log('ℹ Slider no encontrado (no es página con slider)');
        return;
    }
    
    let currentSlide = 0;
    const totalSlides = dots.length;
    let autoAdvanceInterval;
    
    /**
     * Actualizar posición del slider y estado de dots
     */
    function updateSlider() {
        if (slider) {
            slider.style.transform = `translateX(-${currentSlide * 100}%)`;
        }
        
        dots.forEach((dot, index) => {
            if (index === currentSlide) {
                dot.classList.add('active', 'bg-white');
                dot.classList.remove('bg-white/40');
            } else {
                dot.classList.remove('active', 'bg-white');
                dot.classList.add('bg-white/40');
            }
        });
        
        // Reiniciar auto-advance
        clearInterval(autoAdvanceInterval);
        startAutoAdvance();
    }
    
    /**
     * Botón Siguiente
     */
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentSlide = (currentSlide + 1) % totalSlides;
            updateSlider();
        });
    }
    
    /**
     * Botón Anterior
     */
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
            updateSlider();
        });
    }
    
    /**
     * Click en dots de paginación
     */
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            updateSlider();
        });
    });
    
    /**
     * Auto-advance cada 6 segundos
     */
    function startAutoAdvance() {
        autoAdvanceInterval = setInterval(() => {
            currentSlide = (currentSlide + 1) % totalSlides;
            updateSlider();
        }, 6000);
    }
    
    startAutoAdvance();
    console.log('✓ Slider funcionando:', totalSlides, 'slides');
}

/**
 * Feedback de Carrito - Notificaciones al añadir productos
 */
function initCartFeedback() {
    const cartButtons = document.querySelectorAll('button');
    let cartCount = 0;
    
    cartButtons.forEach(btn => {
        // Buscar botones que contengan "Añadir"
        if (btn.innerText.includes('Añadir')) {
            btn.addEventListener('click', (e) => {
                // Prevenir comportamiento por defecto si no es form
                if (btn.type !== 'submit') {
                    e.preventDefault();
                }
                
                cartCount++;
                showNotification(`🛒 Producto añadido al carrito (${cartCount})`, 'success');
                
                // Efecto visual: cambiar escala del botón
                btn.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    btn.style.transform = 'scale(1)';
                }, 100);
            });
        }
    });
    
    if (cartButtons.length > 0) {
        console.log('✓ Cart feedback inicializado');
    }
}

/**
 * Newsletter Subscription Handler
 */
function initNewsletter() {
    // Buscar formulario en sección de newsletter
    const newsletterSections = document.querySelectorAll('section');
    let newsletterForm = null;
    
    newsletterSections.forEach(section => {
        if (section.classList.contains('bg-on-surface')) {
            const form = section.querySelector('form');
            if (form) {
                newsletterForm = form;
            }
        }
    });
    
    if (!newsletterForm) {
        console.log('ℹ Newsletter form no encontrado');
        return;
    }
    
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const emailInput = newsletterForm.querySelector('input[type="email"]');
        if (emailInput && emailInput.value) {
            const email = emailInput.value;
            
            // Mostrar mensaje de éxito
            showNotification('✓ ¡Suscripción exitosa! Te enviaremos ofertas exclusivas', 'success');
            
            // Limpiar campo
            emailInput.value = '';
            
            // Log para debugging (en producción: enviar a backend)
            console.log('Newsletter subscription:', email);
        }
    });
    
    console.log('✓ Newsletter handler inicializado');
}

/**
 * Mostrar notificación toast
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - 'success' o 'error'
 */
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 font-label-md animate-bounce-in`;
    
    if (type === 'success') {
        notification.classList.add('bg-green-500', 'text-white');
    } else if (type === 'error') {
        notification.classList.add('bg-red-500', 'text-white');
    }
    
    notification.innerText = message;
    document.body.appendChild(notification);
    
    // Eliminar después de 3 segundos
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(1rem)';
        notification.style.transition = 'all 0.3s ease';
        
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

/**
 * Utility: Scroll suave a elemento
 */
function smoothScroll(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Utility: Toggle clase en elemento
 */
function toggleClass(elementId, className) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.toggle(className);
    }
}

// Exportar funciones para uso global si es necesario
window.sliderUtils = {
    showNotification,
    smoothScroll,
    toggleClass,
};

console.log('✓ Todos los scripts cargados correctamente');
