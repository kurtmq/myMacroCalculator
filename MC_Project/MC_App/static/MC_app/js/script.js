// Enhanced modal functionality
class ModalManager {
    constructor() {
        this.modals = new Map();
        this.init();
    }

    init() {
        // Close modal on background click
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.hide(e.target.id);
            }
        });

        // Close modal on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideAll();
            }
        });
    }

    show(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
            this.modals.set(modalId, modal);
        }
    }

    hide(modalId) {
        const modal = this.modals.get(modalId);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
            this.modals.delete(modalId);
        }
    }

    hideAll() {
        this.modals.forEach((modal, id) => {
            modal.classList.remove('active');
        });
        this.modals.clear();
        document.body.style.overflow = '';
    }
}

// Initialize modal manager
const modalManager = new ModalManager();

// Tab functionality
function initTabs(container) {
    const tabBtns = container.querySelectorAll('.tab-btn');
    const tabContents = container.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            
            // Update active tab button
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Show corresponding content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `${tabName}-tab`) {
                    content.classList.add('active');
                }
            });
        });
    });
}

// Form validation enhancement
function enhanceFormValidation(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', () => {
            validateField(input);
        });
        
        input.addEventListener('input', () => {
            clearFieldError(input);
        });
    });
}

function validateField(field) {
    clearFieldError(field);
    
    if (!field.value.trim() && field.hasAttribute('required')) {
        showFieldError(field, 'This field is required');
        return false;
    }
    
    if (field.type === 'email' && field.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
            showFieldError(field, 'Please enter a valid email address');
            return false;
        }
    }
    
    return true;
}

function showFieldError(field, message) {
    field.style.borderColor = '#EF4444';
    
    let errorElement = field.parentNode.querySelector('.field-error');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        field.parentNode.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
    errorElement.style.color = '#EF4444';
    errorElement.style.fontSize = '12px';
    errorElement.style.marginTop = '4px';
}

function clearFieldError(field) {
    field.style.borderColor = '';
    
    const errorElement = field.parentNode.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tab containers
    document.querySelectorAll('.tab-container').forEach(initTabs);
    
    // Enhance all forms
    document.querySelectorAll('form').forEach(enhanceFormValidation);
    
    // Add loading states to buttons
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
            }
        });
    });
});

// Utility function for toast notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-left: 4px solid var(--accent-color);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    
    if (type === 'error') {
        toast.style.borderLeftColor = '#EF4444';
    } else if (type === 'success') {
        toast.style.borderLeftColor = '#10B981';
    }
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}