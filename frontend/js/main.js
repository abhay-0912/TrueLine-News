// TrueLine News - Frontend JavaScript
// Main application logic

// Use relative path to work correctly behind nginx proxy
const API_BASE_URL = '/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    console.log('TrueLine News platform initialized');
    loadArticles();
    setupEventListeners();
});

/**
 * Setup event listeners for interactive elements
 */
function setupEventListeners() {
    const verifyBtn = document.getElementById('verifyBtn');
    const newsInput = document.getElementById('newsInput');

    if (verifyBtn) {
        verifyBtn.addEventListener('click', verifyNews);
    }

    if (newsInput) {
        newsInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                verifyNews();
            }
        });
    }
}

/**
 * Load articles from the backend
 */
async function loadArticles() {
    try {
        const response = await fetch(`${API_BASE_URL}/articles`);
        if (!response.ok) {
            throw new Error('Failed to load articles');
        }

        const articles = await response.json();
        displayArticles(articles);
    } catch (error) {
        console.error('Error loading articles:', error);
        displayArticlesError();
    }
}

/**
 * Display articles in the grid
 */
function displayArticles(articles) {
    const container = document.getElementById('articlesContainer');
    
    if (!articles || articles.length === 0) {
        container.innerHTML = '<p>No verified articles available at the moment.</p>';
        return;
    }

    container.innerHTML = articles.map(article => `
        <div class="article-card">
            <div class="article-header">
                <h3 class="article-title">${escapeHtml(article.title)}</h3>
                <p class="article-source">Source: ${escapeHtml(article.source)}</p>
            </div>
            <div class="article-body">
                <p class="article-excerpt">${escapeHtml(article.excerpt)}</p>
                
                <div class="credibility-score">
                    <span class="score-badge ${getScoreBadgeClass(article.credibility_score)}">
                        Credibility: ${(article.credibility_score * 100).toFixed(0)}%
                    </span>
                </div>

                <div class="verification-indicators">
                    ${article.verified_sources > 1 ? '<span class="indicator verified">✓ Multi-source verified</span>' : ''}
                    ${article.cross_checked ? '<span class="indicator verified">✓ Cross-checked</span>' : ''}
                    ${article.is_original ? '<span class="indicator verified">✓ Original reporting</span>' : ''}
                </div>

                <a href="${escapeHtml(article.url)}" class="read-more" target="_blank">Read Full Article →</a>
            </div>
        </div>
    `).join('');
}

/**
 * Display error message when articles fail to load
 */
function displayArticlesError() {
    const container = document.getElementById('articlesContainer');
    container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center;">
            <p style="color: #dc2626;">Failed to load articles. Please try again later.</p>
        </div>
    `;
}

/**
 * Verify a news story
 */
async function verifyNews() {
    const newsInput = document.getElementById('newsInput');
    const query = newsInput.value.trim();

    if (!query) {
        alert('Please enter a news headline or URL to verify');
        return;
    }

    const verifyBtn = document.getElementById('verifyBtn');
    const resultContainer = document.getElementById('verificationResult');

    verifyBtn.disabled = true;
    verifyBtn.textContent = 'Verifying...';

    try {
        const response = await fetch(`${API_BASE_URL}/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            throw new Error('Verification failed');
        }

        const result = await response.json();
        displayVerificationResult(result, resultContainer);
    } catch (error) {
        console.error('Error verifying news:', error);
        resultContainer.innerHTML = `
            <p style="color: #dc2626;">Error verifying the news. Please try again.</p>
        `;
        resultContainer.classList.remove('hidden');
    } finally {
        verifyBtn.disabled = false;
        verifyBtn.textContent = 'Check Authenticity';
    }
}

/**
 * Display verification results
 */
function displayVerificationResult(result, container) {
    const verificationClass = result.is_verified ? 'verified' : 'unverified';
    const scoreClass = getScoreBadgeClass(result.credibility_score);

    container.innerHTML = `
        <div class="result-title ${verificationClass}">
            ${result.is_verified ? '✓ Verified News' : '⚠ Unverified or Suspicious'}
        </div>
        
        <div class="result-content">
            <div class="chart-container">
                <canvas id="credibilityChart"></canvas>
            </div>
            
            <div class="result-details">
                <div class="detail-item">
                    <strong>Credibility Score:</strong> 
                    <span class="score-badge ${scoreClass}">${(result.credibility_score * 100).toFixed(0)}%</span>
                </div>
                <div class="detail-item">
                    <strong>Verified Sources:</strong> ${result.verified_sources || 0}
                </div>
                <div class="detail-item">
                    <strong>Original Reporting:</strong> ${result.is_original ? 'Yes' : 'No'}
                </div>
                <div class="detail-item">
                    <strong>Status:</strong> ${result.status || 'Pending verification'}
                </div>
            </div>
        </div>
        
        ${result.sources ? `
            <div style="margin-top: 2rem;">
                <strong>Reporting Sources:</strong>
                <ul style="margin-top: 0.5rem;">
                    ${result.sources.map(source => `<li>${escapeHtml(source)}</li>`).join('')}
                </ul>
            </div>
        ` : ''}
    `;

    container.classList.remove('hidden');
    
    // Draw credibility chart
    setTimeout(() => {
        drawCredibilityChart(result.credibility_score);
    }, 100);
}

/**
 * Draw credibility visualization chart
 */
function drawCredibilityChart(score) {
    const ctx = document.getElementById('credibilityChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Credibility', 'Uncertainty'],
            datasets: [{
                data: [score * 100, (1 - score) * 100],
                backgroundColor: [
                    '#10b981',
                    '#e5e7eb'
                ],
                borderColor: ['#059669', '#d1d5db'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

/**
 * Get badge class based on credibility score
 */
function getScoreBadgeClass(score) {
    if (score >= 0.7) return 'high';
    if (score >= 0.4) return 'medium';
    return 'low';
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
