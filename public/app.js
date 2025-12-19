// API Base URL
const API_URL = '/api/resources';

// DOM Elements
const resourceForm = document.getElementById('resource-form');
const resourcesList = document.getElementById('resources-list');
const loadingElement = document.getElementById('loading');
const messageContainer = document.getElementById('message-container');

// Show message (success or error)
function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    messageContainer.innerHTML = '';
    messageContainer.appendChild(messageDiv);
    
    // Auto-hide message after 5 seconds
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            messageDiv.remove();
        }, 300);
    }, 5000);
}

// Fetch and display resources
async function fetchResources() {
    try {
        loadingElement.style.display = 'block';
        resourcesList.innerHTML = '';
        
        const response = await fetch(API_URL);
        
        if (!response.ok) {
            throw new Error('Failed to fetch resources');
        }
        
        const result = await response.json();
        
        loadingElement.style.display = 'none';
        
        if (result.success && result.data.length > 0) {
            displayResources(result.data);
        } else {
            displayEmptyState();
        }
    } catch (error) {
        loadingElement.style.display = 'none';
        showMessage('Error fetching resources: ' + error.message, 'error');
        displayEmptyState();
    }
}

// Display resources in the list
function displayResources(resources) {
    resourcesList.innerHTML = '';
    
    resources.forEach(resource => {
        const card = createResourceCard(resource);
        resourcesList.appendChild(card);
    });
}

// Create a resource card element
function createResourceCard(resource) {
    const card = document.createElement('div');
    card.className = 'resource-card';
    
    card.innerHTML = `
        <span class="resource-id">ID: ${escapeHtml(String(resource.id))}</span>
        <h3>${escapeHtml(resource.name)}</h3>
        <p>${escapeHtml(resource.description)}</p>
        <a href="${escapeHtml(resource.url)}" target="_blank" rel="noopener noreferrer">
            🔗 ${escapeHtml(resource.url)}
        </a>
    `;
    
    return card;
}

// Display empty state when no resources
function displayEmptyState() {
    resourcesList.innerHTML = `
        <div class="empty-state">
            <p>📭 No resources available yet.</p>
            <p>Add your first resource using the form above!</p>
        </div>
    `;
}

// Handle form submission
resourceForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        url: document.getElementById('url').value
    };
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage(result.message || 'Resource added successfully!', 'success');
            resourceForm.reset();
            fetchResources(); // Refresh the list
        } else {
            showMessage(result.message || 'Failed to add resource', 'error');
        }
    } catch (error) {
        showMessage('Error adding resource: ' + error.message, 'error');
    }
});

// Utility function to escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    fetchResources();
});
