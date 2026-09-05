/* ============================================
   UFA KENYA - MAIN JAVASCRIPT
   Unique Focus Association
   Professional Youth Organization Theme
   ============================================ */

// ============================================
// 1. NAVBAR SCROLL EFFECT
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar-custom');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
});

// ============================================
// 2. MOBILE MENU TOGGLE
// ============================================
document.querySelectorAll('.navbar-toggler').forEach(function(toggler) {
    toggler.addEventListener('click', function() {
        const target = document.querySelector(this.dataset.bsTarget);
        if (target) {
            target.classList.toggle('show');
        }
    });
});

// ============================================
// 3. FORM VALIDATION
// ============================================
document.querySelectorAll('form').forEach(function(form) {
    form.addEventListener('submit', function(e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(function(field) {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            const firstInvalid = form.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.focus();
            }
        }
    });
});

// ============================================
// 4. PASSWORD STRENGTH INDICATOR
// ============================================
document.querySelectorAll('input[type="password"]').forEach(function(passwordInput) {
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        const strengthIndicator = this.closest('.form-group')?.querySelector('.password-strength');
        
        if (strengthIndicator) {
            let strength = 0;
            if (password.length >= 8) strength++;
            if (password.match(/[a-z]+/)) strength++;
            if (password.match(/[A-Z]+/)) strength++;
            if (password.match(/[0-9]+/)) strength++;
            if (password.match(/[$@#&!]+/)) strength++;
            
            const strengthText = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
            const strengthColor = ['danger', 'warning', 'info', 'primary', 'success'];
            
            strengthIndicator.textContent = strengthText[strength] || '';
            strengthIndicator.className = 'password-strength text-' + (strengthColor[strength] || 'secondary');
        }
    });
});

// ============================================
// 5. ALERT AUTO-DISMISS
// ============================================
document.querySelectorAll('.alert').forEach(function(alert) {
    setTimeout(function() {
        alert.classList.add('fade');
        setTimeout(function() {
            alert.style.display = 'none';
        }, 500);
    }, 5000);
});

// ============================================
// 6. CARD ANIMATION ON SCROLL
// ============================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.card-custom, .stat-box').forEach(function(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    element.style.transition = 'all 0.6s ease';
    observer.observe(element);
});

// ============================================
// 7. DARK MODE TOGGLE (Optional)
// ============================================
// This can be enabled later for dark mode support
const toggleDarkMode = function() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
};

// Check saved preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// ============================================
// 8. CONSOLE WELCOME
// ============================================
console.log('%c UFA Kenya ', 'background: #1a3c6e; color: #f5a623; padding: 10px 20px; font-size: 20px; font-weight: bold; border-radius: 5px;');
console.log('%c Empowering Youth for a Better Kenya ', 'color: #2d6da8; font-size: 14px;');
