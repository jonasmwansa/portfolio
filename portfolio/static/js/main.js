// Ensure GSAP plugins are registered
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', function() {
    // --- 1. Theme Toggle Logic (Light/Dark Mode) ---
    const body = document.body;
    const themeToggleBtn = document.getElementById('themeToggle');
    const THEME_KEY = 'portfolioTheme';

    const switchTheme = (theme) => {
        body.setAttribute('data-bs-theme', theme);
        localStorage.setItem(THEME_KEY, theme);
        updateToggleIcon(theme);
    };

    const updateToggleIcon = (theme) => {
        if (theme === 'dark') {
            themeToggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            themeToggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
        }
    };

    // Initialize theme based on preference or system
    let preferredTheme = localStorage.getItem(THEME_KEY) || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    switchTheme(preferredTheme);
    
    // Toggle handler
    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = body.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        switchTheme(newTheme);
    });

    // --- 2. Scroll-based Animations (GSAP) ---
    const sections = document.querySelectorAll('section');

    sections.forEach(section => {
        // Initial state (hidden below or scaled down)
        gsap.from(section, {
            opacity: 0,
            y: 50,
            duration: 0.8,
            ease: "power2.out",
            scrollTrigger: {
                trigger: section,
                start: "top 85%", // Start animation when 85% of section is in view
                toggleActions: "play none none none" // Play only once
            }
        });
    });

    // Animate individual elements (like project cards) within sections
    gsap.utils.toArray('.animate-in').forEach((element, i) => {
        gsap.from(element, {
            opacity: 0,
            scale: 0.8,
            duration: 0.6,
            delay: i * 0.1, // Stagger delay
            ease: "back.out(1.2)",
            scrollTrigger: {
                trigger: element.closest('section'),
                start: "top 75%",
                toggleActions: "play none none none"
            }
        });
    });

    // --- 3. Sticky Navbar & Back-to-Top Button ---
    const navbar = document.querySelector('.navbar-custom');
    const backToTopBtn = document.getElementById('backToTop');
    
    window.addEventListener('scroll', () => {
        // Sticky Navbar Shadow
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Show/Hide Back-to-Top Button
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('show-link');
        } else {
            backToTopBtn.classList.remove('show-link');
        }
    });

    // --- 4. Smooth Scrolling for Anchors (Single Page App) ---
    document.querySelectorAll('a.scroll-link').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    // Smoothly scroll to the target element, factoring in fixed header height
                    const headerOffset = 70; // Height of the fixed header
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.scrollY - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: "smooth"
                    });
                    
                    // Collapse the navbar on mobile after clicking a link
                    const navbarCollapse = document.getElementById('navbarNav');
                    const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                    if (bsCollapse) {
                        bsCollapse.hide();
                    }
                }
            }
        });
    });

});
