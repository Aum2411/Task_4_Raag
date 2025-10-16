// Smooth scroll helper function
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const navHeight = 80; // Height of fixed navbar
        const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
        const offsetPosition = elementPosition - navHeight;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

// Make scroll functions globally accessible
window.scrollToDemo = function() {
    smoothScrollTo('demo');
}

window.scrollToDocs = function() {
    smoothScrollTo('docs');
}

window.scrollToFeatures = function() {
    smoothScrollTo('features');
}

window.scrollToAPIs = function() {
    smoothScrollTo('apis');
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        smoothScrollTo(targetId);
    });
});

// Mobile menu toggle
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector('.nav-menu');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
    });
}

// Active navigation link highlighting
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

function highlightNav() {
    let scrollPosition = window.scrollY + 100;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');

        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

window.addEventListener('scroll', highlightNav);

// Terminal animation
const terminalLines = [
    { type: 'command', text: 'python main.py --mode interactive' },
    { type: 'output', text: '🚀 RAG Agent initialized successfully!' },
    { type: 'output', text: '✓ Vector store loaded with 1,247 documents' },
    { type: 'output', text: '✓ LLM connected (Groq - Llama 3.3)' },
    { type: 'output', text: '✓ Web search enabled (Serper API)' },
    { type: 'command', text: 'query: What are the latest advances in AI?' },
    { type: 'output', text: '🔍 Analyzing query and delegating tasks...' },
    { type: 'output', text: '📚 Searching knowledge base: 47 relevant docs found' },
    { type: 'output', text: '🌐 Web search: 15 recent articles retrieved' },
    { type: 'output', text: '✨ Generating comprehensive response...' }
];

let terminalIndex = 0;
const terminalBody = document.querySelector('.terminal-body');

function typeTerminalLine() {
    if (terminalIndex >= terminalLines.length) {
        terminalIndex = 0;
        if (terminalBody) {
            terminalBody.innerHTML = '';
        }
        setTimeout(typeTerminalLine, 2000);
        return;
    }

    const line = terminalLines[terminalIndex];
    const lineElement = document.createElement('div');
    lineElement.className = 'terminal-line';

    if (line.type === 'command') {
        lineElement.innerHTML = `<span class="prompt">$</span><span class="command">${line.text}</span>`;
    } else {
        lineElement.innerHTML = `<div class="output ${line.text.includes('✓') || line.text.includes('✨') ? 'success' : 'info'}">${line.text}</div>`;
    }

    if (terminalBody) {
        terminalBody.appendChild(lineElement);
        terminalBody.scrollTop = terminalBody.scrollHeight;
    }

    terminalIndex++;
    setTimeout(typeTerminalLine, 1000);
}

// Start terminal animation when page loads
setTimeout(typeTerminalLine, 1000);

// Chat demo functionality
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const clearChatBtn = document.getElementById('clearChat');

const exampleResponses = {
    'hello': 'Hello! I\'m the RAG Agent. I can help you with research, document analysis, and complex queries. What would you like to explore?',
    'how do you work': 'I combine multiple AI technologies:\n• Vector database (ChromaDB) for semantic search\n• LLM (Llama 3.3) for understanding and generation\n• Web search (Serper) for real-time information\n• Task delegation for complex queries\n\nAsk me anything!',
    'research': 'I can conduct deep research by:\n1. Breaking down complex queries into subtasks\n2. Searching my knowledge base for relevant documents\n3. Fetching real-time web information\n4. Synthesizing comprehensive answers\n\nWhat topic would you like me to research?',
    'default': 'Great question! In a full implementation, I would:\n• Analyze your query semantically\n• Search my vector database for relevant context\n• Optionally fetch real-time web data\n• Generate a comprehensive, cited response\n\nTry the Python CLI for the complete experience!'
};

function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'agent-message'}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    // Convert newlines to paragraphs and lists
    const lines = text.split('\n');
    let htmlContent = '';
    let inList = false;
    
    lines.forEach(line => {
        if (line.trim().startsWith('•') || line.trim().match(/^\d+\./)) {
            if (!inList) {
                htmlContent += '<ul>';
                inList = true;
            }
            htmlContent += `<li>${line.replace(/^[•\d+\.]\s*/, '')}</li>`;
        } else {
            if (inList) {
                htmlContent += '</ul>';
                inList = false;
            }
            if (line.trim()) {
                htmlContent += `<p>${line}</p>`;
            }
        }
    });
    
    if (inList) {
        htmlContent += '</ul>';
    }
    
    content.innerHTML = htmlContent;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    if (chatMessages) {
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function getResponse(userText) {
    const lowerText = userText.toLowerCase();
    
    for (const [key, response] of Object.entries(exampleResponses)) {
        if (key !== 'default' && lowerText.includes(key)) {
            return response;
        }
    }
    
    return exampleResponses.default;
}

// Make sendMessage globally accessible
window.sendMessage = function() {
    console.log('sendMessage called');
    if (!chatInput) {
        console.error('chatInput not found');
        return;
    }
    
    const text = chatInput.value.trim();
    console.log('User text:', text);
    if (!text) return;
    
    // Add user message
    addMessage(text, true);
    chatInput.value = '';
    
    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message agent-message typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar"><i class="fas fa-robot"></i></div>
        <div class="message-content"><div class="loading"></div></div>
    `;
    if (chatMessages) {
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Simulate processing delay
    setTimeout(() => {
        if (chatMessages && typingDiv.parentNode) {
            chatMessages.removeChild(typingDiv);
        }
        const response = getResponse(text);
        console.log('Agent response:', response);
        addMessage(response, false);
    }, 1500);
}

// Make clearChat globally accessible
window.clearChat = function() {
    console.log('clearChat called');
    if (chatMessages) {
        chatMessages.innerHTML = '';
    }
    addMessage('Chat cleared! How can I help you today?', false);
}

// Add keyboard support
if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// Quick action buttons
const actionButtons = document.querySelectorAll('.action-btn');

const actionExamples = {
    'rag-query': 'What is retrieval augmented generation and how does it improve AI responses?',
    'web-search': 'What are the latest developments in large language models?',
    'task-delegation': 'Compare and contrast different machine learning frameworks including their pros, cons, and use cases',
    'doc-analysis': 'Analyze the main concepts in this document and provide key insights'
};

actionButtons.forEach(button => {
    button.addEventListener('click', () => {
        const action = button.getAttribute('data-action');
        const example = actionExamples[action];
        
        if (example && chatInput) {
            chatInput.value = example;
            chatInput.focus();
        }
    });
});

// Add welcome message after page loads
window.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded');
    console.log('chatMessages element:', chatMessages);
    console.log('chatInput element:', chatInput);
    
    setTimeout(() => {
        addMessage('👋 Welcome to RAG Agent Demo! Ask me anything or try the quick actions on the left. This is a demo interface - use the Python CLI for full functionality.', false);
    }, 500);
});

// Animate feature cards on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '0';
            entry.target.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }, 100);
            
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.feature-card, .api-card, .doc-card').forEach(card => {
    observer.observe(card);
});

// Stats counter animation
function animateStats() {
    const stats = document.querySelectorAll('.stat-value');
    
    stats.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-target') || stat.textContent);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const counter = setInterval(() => {
            current += step;
            if (current >= target) {
                stat.textContent = target + (stat.textContent.includes('+') ? '+' : '');
                clearInterval(counter);
            } else {
                stat.textContent = Math.floor(current);
            }
        }, 16);
    });
}

// Trigger stats animation when visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateStats();
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.apis');
if (statsSection) {
    statsObserver.observe(statsSection);
}

// Copy code examples
document.querySelectorAll('.code-example code').forEach(codeBlock => {
    codeBlock.style.cursor = 'pointer';
    codeBlock.title = 'Click to copy';
    
    codeBlock.addEventListener('click', () => {
        const text = codeBlock.textContent;
        navigator.clipboard.writeText(text).then(() => {
            const originalText = codeBlock.textContent;
            codeBlock.textContent = '✓ Copied!';
            codeBlock.style.color = 'var(--success-color)';
            
            setTimeout(() => {
                codeBlock.textContent = originalText;
                codeBlock.style.color = '';
            }, 2000);
        });
    });
});

// Add floating particles background (optional enhancement)
function createParticles() {
    const hero = document.querySelector('.hero-background');
    if (!hero) return;
    
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = Math.random() * 4 + 1 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = 'rgba(99, 102, 241, 0.3)';
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animation = `float ${Math.random() * 10 + 10}s infinite ease-in-out`;
        hero.appendChild(particle);
    }
}

// Add float animation
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0%, 100% { transform: translateY(0px) translateX(0px); }
        25% { transform: translateY(-20px) translateX(10px); }
        50% { transform: translateY(-10px) translateX(-10px); }
        75% { transform: translateY(-30px) translateX(5px); }
    }
`;
document.head.appendChild(style);

// Initialize particles
createParticles();

console.log('🚀 RAG Agent Website loaded successfully!');