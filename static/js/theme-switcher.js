// Theme Switcher
class ThemeSwitcher {
    constructor() {
        this.themes = ['dark', 'light', 'black'];
        this.currentThemeIdx = 0;
        this.init();
    }

    init() {
        // Get saved theme from localStorage or use system preference
        const savedTheme = localStorage.getItem('theme') || 'dark';
        this.setTheme(savedTheme);
        this.setupEventListeners();
    }

    setupEventListeners() {
        const toggleBtn = document.querySelector('.theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleDropdown();
            });
        }

        const options = document.querySelectorAll('.theme-option');
        options.forEach(option => {
            option.addEventListener('click', (e) => {
                const theme = e.target.dataset.theme;
                this.setTheme(theme);
                this.closeDropdown();
            });
        });

        // Close dropdown when clicking elsewhere
        document.addEventListener('click', () => {
            this.closeDropdown();
        });
    }

    setTheme(theme) {
        if (!this.themes.includes(theme)) {
            theme = 'dark';
        }

        // Set HTML attribute
        document.documentElement.setAttribute('data-theme', theme);
        
        // Save to localStorage
        localStorage.setItem('theme', theme);

        // Update button icon and text
        this.updateThemeButton(theme);

        // Update active state in dropdown
        this.updateActiveOption(theme);
    }

    updateThemeButton(theme) {
        const toggleBtn = document.querySelector('.theme-toggle');
        if (!toggleBtn) return;

        const iconMap = {
            'dark': '🌙',
            'light': '☀️',
            'black': '🌑'
        };

        const labelMap = {
            'dark': 'Dark',
            'light': 'Light',
            'black': 'Black'
        };

        const icon = toggleBtn.querySelector('.theme-icon');
        if (icon) {
            icon.textContent = iconMap[theme];
        }

        // Update text if it exists
        const textSpan = toggleBtn.querySelector('.theme-text');
        if (textSpan) {
            textSpan.textContent = labelMap[theme];
        }
    }

    updateActiveOption(theme) {
        const options = document.querySelectorAll('.theme-option');
        options.forEach(option => {
            if (option.dataset.theme === theme) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    }

    toggleDropdown() {
        const dropdown = document.querySelector('.theme-dropdown');
        if (dropdown) {
            dropdown.classList.toggle('active');
        }
    }

    closeDropdown() {
        const dropdown = document.querySelector('.theme-dropdown');
        if (dropdown) {
            dropdown.classList.remove('active');
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ThemeSwitcher();
});
