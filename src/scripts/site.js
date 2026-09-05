import * as THREE from 'three';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// LaunchPoint - Modern Website Script

document.addEventListener('DOMContentLoaded', () => {
    // Prevent browser from restoring scroll position to bottom
    if ('scrollRestoration' in history) {
        history.scrollRestoration = 'manual';
    }
    window.scrollTo(0, 0);

    // Initialize animations & features
    initScrollAnimations();
    initNavigation();
    initFormHandling();
    // Initialize custom cursor and magnetic buttons
    initCursorAndMagnetic();

    // Initialize 3D Background
    initThreeJSBackground();
});

// Advanced scroll animations with GSAP
function initScrollAnimations() {
    gsap.registerPlugin(ScrollTrigger);

    // 1. Hero Section Entrance Animation
    const heroTl = gsap.timeline();
    heroTl.from(".hero-badge", { y: 20, opacity: 0, duration: 0.6, ease: "power3.out" })
          .from(".hero-title", { y: 30, opacity: 0, duration: 0.8, ease: "power3.out" }, "-=0.4")
          .from(".hero-subtitle", { y: 20, opacity: 0, duration: 0.6, ease: "power3.out" }, "-=0.4")
          .from(".hero-buttons .btn", { y: 20, opacity: 0, duration: 0.6, stagger: 0.1, ease: "power3.out" }, "-=0.4");

    // Parallax effect on the 3D canvas
    gsap.to('.hero-3d', {
        scrollTrigger: {
            trigger: '.hero',
            start: "top top",
            end: "bottom top",
            scrub: true
        },
        y: 150,
        ease: "none"
    });
}

// Active navigation link highlighting
function initNavigation() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    const updateActiveLink = () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current)) {
                link.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', updateActiveLink);
    updateActiveLink();
}

// Handle contact form submission
function initFormHandling() {
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        const submitBtn = contactForm.querySelector('.btn');
        if (submitBtn) {
            submitBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const emailInput = contactForm.querySelector('input[type="email"]');
                if (emailInput.value) {
                    console.log('Email submitted:', emailInput.value);
                    submitBtn.textContent = 'Email sent! ✓';
                    submitBtn.style.pointerEvents = 'none';
                    setTimeout(() => {
                        submitBtn.textContent = 'Schedule a Call';
                        submitBtn.style.pointerEvents = 'auto';
                        emailInput.value = '';
                    }, 3000);
                }
            });
        }
    }
}

// Custom Cursor and Interactive Elements
function initCursorAndMagnetic() {
    const cursor = document.querySelector('.custom-cursor');
    if (!cursor) return;

    // Center cursor around mouse position natively with GSAP (Arrow points top-left)
    gsap.set(cursor, { xPercent: 0, yPercent: 0 });

    // Move cursor with GSAP for smoothness
    window.addEventListener('mousemove', (e) => {
        gsap.to(cursor, { x: e.clientX, y: e.clientY, duration: 0.1, ease: "none" });
    });

    // Hover state for cursor
    const interactiveElements = document.querySelectorAll('a, button, .service-card, .project-card');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
    });

    // Magnetic Buttons Effect
    const magneticBtns = document.querySelectorAll('.btn');
    magneticBtns.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            gsap.to(btn, {
                x: x * 0.3, // Pull strength
                y: y * 0.3,
                duration: 0.6,
                ease: "power3.out"
            });
        });
        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, { x: 0, y: 0, duration: 0.6, ease: "power3.out" }); // Reset magnetic
        });
    });
}

console.log('✨ LaunchPoint modern website loaded successfully!');

// Three.js Interactive Background
function initThreeJSBackground() {
    const canvas = document.getElementById('hero-3d-canvas');
    if (!canvas || typeof THREE === 'undefined') return;

    const scene = new THREE.Scene();
    
    // Canvas now spans the wrapper containing both hero and services
    const wrapper = document.querySelector('.hero-services-wrapper');
    const getWidth = () => window.innerWidth;
    const getHeight = () => wrapper.clientHeight;

    const camera = new THREE.PerspectiveCamera(45, getWidth() / getHeight(), 0.1, 1000);
    // Pull camera back slightly to view the much larger scene
    camera.position.set(0, 0, 70);

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(getWidth(), getHeight());
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Create a CatmullRomCurve3 for the swooping arrow path
    // Starts completely flat off-screen left, swoops under the hero text, and curves high right
    // Y=30 is roughly the top of the hero, Y=-30 is the bottom of services
    const curve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-45, 2, -10),  // Off-screen left, vertically in the middle of hero/services
        new THREE.Vector3(-20, 2, -5),   // Flat trajectory moving right
        new THREE.Vector3(5, 5, 5),      // Starting to curve up 
        new THREE.Vector3(15, 12, 0),    // Angling up sharply
        new THREE.Vector3(35, 25, -15)   // End top right
    ]);

    // Tube geometry (Slightly smaller than before, 0.7 thickness)
    const tubeGeom = new THREE.TubeGeometry(curve, 100, 0.7, 16, false);
    const material = new THREE.MeshBasicMaterial({ 
        color: 0xf97316, 
        wireframe: true,
        transparent: true,
        opacity: 0.4
    });
    const tube = new THREE.Mesh(tubeGeom, material);
    
    // Cone geometry (Arrow head)
    const coneGeom = new THREE.ConeGeometry(2.5, 7, 16);
    const coneMat = new THREE.MeshBasicMaterial({
        color: 0xec4899,
        wireframe: true,
        transparent: true,
        opacity: 0.7
    });
    const cone = new THREE.Mesh(coneGeom, coneMat);

    // Position cone at the very end of the curve
    const endPt = curve.getPoint(1);
    const tangent = curve.getTangent(1).normalize();
    cone.position.copy(endPt);

    // Rotate cone to point along the tangent
    const axis = new THREE.Vector3(0, 1, 0);
    cone.quaternion.setFromUnitVectors(axis, tangent);
    // Shift cone forward by half its height (3.5) so base attaches to tube tip
    cone.position.add(tangent.clone().multiplyScalar(3.5));

    const arrowGroup = new THREE.Group();
    arrowGroup.add(tube);
    arrowGroup.add(cone);
    scene.add(arrowGroup);

    // Animation Loop for subtle floating
    let time = 0;
    function animate() {
        requestAnimationFrame(animate);
        time += 0.015;

        // Gentle hover effect
        arrowGroup.position.y = Math.sin(time) * 1.5;
        arrowGroup.rotation.x = Math.sin(time * 0.5) * 0.03;

        renderer.render(scene, camera);
    }
    animate();

    // Handle Resize
    window.addEventListener('resize', () => {
        const width = getWidth();
        const height = getHeight();
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    });
}
