/**
 * Table of Contents Generator for Legal Documents
 * Automatically generates TOC from headings and provides smooth scrolling
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        tocSelector: '#toc',
        contentSelector: '.legal-document',
        headingSelector: 'h2, h3, h4',
        tocClass: 'table-of-contents',
        tocListClass: 'toc-list',
        tocItemClass: 'toc-item',
        tocLinkClass: 'toc-link',
        activeClass: 'active',
        scrollOffset: 100, // Offset for sticky header
        throttleMs: 100
    };

    // Utility functions
    function throttle(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    function slugify(text) {
        return text
            .toLowerCase()
            .trim()
            .replace(/[^\w\s-]/g, '') // Remove special characters
            .replace(/[\s_-]+/g, '-') // Replace spaces and underscores with hyphens
            .replace(/^-+|-+$/g, ''); // Remove leading/trailing hyphens
    }

    function getHeadingLevel(heading) {
        return parseInt(heading.tagName.charAt(1));
    }

    // TOC Generator Class
    class TOCGenerator {
        constructor() {
            this.tocContainer = document.querySelector(CONFIG.tocSelector);
            this.contentContainer = document.querySelector(CONFIG.contentSelector);
            this.headings = [];
            this.tocItems = [];
            this.isScrolling = false;

            if (this.tocContainer && this.contentContainer) {
                this.init();
            }
        }

        init() {
            this.collectHeadings();
            if (this.headings.length > 0) {
                this.generateTOC();
                this.setupScrollSpy();
                this.setupSmoothScrolling();
                this.updateActiveSection();
            } else {
                // Hide TOC if no headings found
                this.tocContainer.style.display = 'none';
            }
        }

        collectHeadings() {
            const headingElements = this.contentContainer.querySelectorAll(CONFIG.headingSelector);
            
            headingElements.forEach((heading, index) => {
                // Ensure heading has an ID
                if (!heading.id) {
                    const text = heading.textContent || heading.innerText;
                    const slug = slugify(text.replace(/^\d+\.\s*/, ''));
                    heading.id = slug || `heading-${index}`;
                }

                // Store heading information
                this.headings.push({
                    element: heading,
                    id: heading.id,
                    text: heading.textContent || heading.innerText,
                    level: getHeadingLevel(heading)
                });
            });
        }

        generateTOC() {
            // Clear existing content
            this.tocContainer.innerHTML = '';

            // Create TOC structure
            const tocTitle = document.createElement('h3');
            tocTitle.textContent = 'Table of Contents';
            this.tocContainer.appendChild(tocTitle);

            const tocList = document.createElement('ol');
            tocList.className = CONFIG.tocListClass;

            this.headings.forEach((heading, index) => {
                const listItem = document.createElement('li');
                listItem.className = `${CONFIG.tocItemClass} toc-level-${heading.level}`;

                const link = document.createElement('a');
                link.href = `#${heading.id}`;
                link.className = CONFIG.tocLinkClass;
                link.textContent = heading.text;
                link.setAttribute('data-heading-id', heading.id);

                // Add aria-label for accessibility
                link.setAttribute('aria-label', `Go to section: ${heading.text}`);

                listItem.appendChild(link);
                tocList.appendChild(listItem);

                // Store reference for scroll spy
                this.tocItems.push({
                    link: link,
                    heading: heading
                });
            });

            this.tocContainer.appendChild(tocList);

            // Add CSS classes for styling
            this.tocContainer.classList.add(CONFIG.tocClass);
        }

        setupSmoothScrolling() {
            this.tocContainer.addEventListener('click', (e) => {
                if (e.target.classList.contains(CONFIG.tocLinkClass)) {
                    e.preventDefault();
                    
                    const targetId = e.target.getAttribute('data-heading-id');
                    const targetElement = document.getElementById(targetId);
                    
                    if (targetElement) {
                        this.isScrolling = true;
                        
                        // Calculate scroll position with offset
                        const targetPosition = targetElement.getBoundingClientRect().top + 
                                             window.pageYOffset - 
                                             CONFIG.scrollOffset;

                        // Smooth scroll
                        window.scrollTo({
                            top: targetPosition,
                            behavior: 'smooth'
                        });

                        // Update active state immediately
                        this.setActiveItem(e.target);

                        // Reset scrolling flag after animation
                        setTimeout(() => {
                            this.isScrolling = false;
                        }, 1000);

                        // Update URL hash
                        if (history.replaceState) {
                            history.replaceState(null, null, `#${targetId}`);
                        }
                    }
                }
            });
        }

        setupScrollSpy() {
            const throttledScrollHandler = throttle(() => {
                if (!this.isScrolling) {
                    this.updateActiveSection();
                }
            }, CONFIG.throttleMs);

            window.addEventListener('scroll', throttledScrollHandler, { passive: true });
            
            // Handle initial load with hash
            if (window.location.hash) {
                setTimeout(() => {
                    const targetElement = document.querySelector(window.location.hash);
                    if (targetElement) {
                        const targetPosition = targetElement.getBoundingClientRect().top + 
                                             window.pageYOffset - 
                                             CONFIG.scrollOffset;
                        window.scrollTo({
                            top: targetPosition,
                            behavior: 'smooth'
                        });
                    }
                }, 100);
            }
        }

        updateActiveSection() {
            let activeIndex = -1;
            const scrollPosition = window.pageYOffset + CONFIG.scrollOffset;

            // Find the currently visible section
            for (let i = this.headings.length - 1; i >= 0; i--) {
                const heading = this.headings[i];
                const headingPosition = heading.element.getBoundingClientRect().top + window.pageYOffset;
                
                if (scrollPosition >= headingPosition) {
                    activeIndex = i;
                    break;
                }
            }

            // Update active states
            this.tocItems.forEach((item, index) => {
                const isActive = index === activeIndex;
                item.link.classList.toggle(CONFIG.activeClass, isActive);
                item.link.parentElement.classList.toggle(CONFIG.activeClass, isActive);
                
                // Update aria-current for accessibility
                if (isActive) {
                    item.link.setAttribute('aria-current', 'location');
                } else {
                    item.link.removeAttribute('aria-current');
                }
            });
        }

        setActiveItem(activeLink) {
            // Remove active class from all items
            this.tocItems.forEach(item => {
                item.link.classList.remove(CONFIG.activeClass);
                item.link.parentElement.classList.remove(CONFIG.activeClass);
                item.link.removeAttribute('aria-current');
            });

            // Add active class to clicked item
            activeLink.classList.add(CONFIG.activeClass);
            activeLink.parentElement.classList.add(CONFIG.activeClass);
            activeLink.setAttribute('aria-current', 'location');
        }
    }

    // Initialize when DOM is ready
    function initTOC() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                new TOCGenerator();
            });
        } else {
            new TOCGenerator();
        }
    }

    // Auto-initialize
    initTOC();

    // Expose to global scope if needed
    window.TOCGenerator = TOCGenerator;

})();