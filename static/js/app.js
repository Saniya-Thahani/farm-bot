// Main application JavaScript for FarmBot

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const applyFiltersBtn = document.getElementById('apply-filters');
    const resetFiltersBtn = document.getElementById('reset-filters');
    
    // Initialize chatbot
    initChat();
    
    // Initialize filter functionality
    initFilters();
    
    // Load filter options from the server
    loadFilterOptions();
    
    /**
     * Initialize chat functionality
     */
    function initChat() {
        if (chatForm) {
            chatForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const message = userInput.value.trim();
                if (message === '') return;
                
                // Display user message
                addUserMessage(message);
                
                // Clear input
                userInput.value = '';
                
                // Show typing indicator
                addTypingIndicator();
                
                // Get current filters
                const filters = getCurrentFilters();
                
                // Send message to backend
                sendChatMessage(message, filters);
            });
        }
    }
    
    /**
     * Load filter options from server
     */
    function loadFilterOptions() {
        // Load soil types
        fetchOptions('SOIL TYPE', 'soil-type');
        
        // Load months
        fetchOptions('MONTH', 'month');
        
        // Load seasons
        fetchOptions('SEASON', 'season');
        
        // Load land types
        fetchOptions('LAND TYPE', 'land-type');
    }
    
    /**
     * Fetch options for a specific filter type
     */
    function fetchOptions(optionType, elementId) {
        fetch(`/api/options?type=${encodeURIComponent(optionType)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    populateDropdown(elementId, data.options);
                } else {
                    console.error(`Error fetching ${optionType} options:`, data.message);
                }
            })
            .catch(error => {
                console.error(`Fetch error for ${optionType}:`, error);
            });
    }
    
    /**
     * Populate a dropdown with options
     */
    function populateDropdown(elementId, options) {
        const dropdown = document.getElementById(elementId);
        if (!dropdown) return;
        
        // Keep the first "Any" option
        const firstOption = dropdown.options[0];
        dropdown.innerHTML = '';
        dropdown.appendChild(firstOption);
        
        // Add new options
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            dropdown.appendChild(optionElement);
        });
    }
    
    /**
     * Initialize filter functionality
     */
    function initFilters() {
        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', function() {
                // Get current message or use a generic one
                const message = "Please recommend crops based on the selected filters";
                
                // Display user message
                addUserMessage(message);
                
                // Show typing indicator
                addTypingIndicator();
                
                // Get current filters
                const filters = getCurrentFilters();
                
                // Send message to backend
                sendChatMessage(message, filters);
                
                // Update chart with new filters
                updateChartWithFilters(filters);
            });
        }
        
        if (resetFiltersBtn) {
            resetFiltersBtn.addEventListener('click', function() {
                // Reset all filter dropdowns
                document.getElementById('soil-type').value = '';
                document.getElementById('month').value = '';
                document.getElementById('season').value = '';
                document.getElementById('land-type').value = '';
                document.getElementById('land-size').value = '1';
                document.getElementById('climate-condition').value = '';
                
                // Update chart with default values
                updateChartWithFilters({});
            });
        }
    }
    
    /**
     * Get current filter values
     */
    function getCurrentFilters() {
        return {
            soil: document.getElementById('soil-type')?.value || '',
            month: document.getElementById('month')?.value || '',
            season: document.getElementById('season')?.value || '',
            land_type: document.getElementById('land-type')?.value || '',
            land_size: parseFloat(document.getElementById('land-size')?.value || '1'),
            climate_condition: document.getElementById('climate-condition')?.value || ''
        };
    }
    
    /**
     * Add user message to chat
     */
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'user-message mb-3';
        messageElement.innerHTML = `
            <div class="d-flex justify-content-end">
                <div class="message-content p-3 rounded">
                    ${message}
                </div>
                <div class="ms-2">
                    <i class="fas fa-user text-primary"></i>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    /**
     * Add bot message to chat
     */
    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'bot-message mb-3';
        messageElement.innerHTML = `
            <div class="d-flex">
                <div class="me-2">
                    <i class="fas fa-robot text-info"></i>
                </div>
                <div class="message-content p-3 rounded">
                    ${formatBotMessage(message)}
                </div>
            </div>
        `;
        
        // Remove typing indicator if present
        const typingIndicator = document.querySelector('.typing-indicator-container');
        if (typingIndicator) {
            chatMessages.removeChild(typingIndicator);
        }
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    /**
     * Add typing indicator to chat
     */
    function addTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.className = 'typing-indicator-container bot-message mb-3';
        typingElement.innerHTML = `
            <div class="d-flex">
                <div class="me-2">
                    <i class="fas fa-robot text-info"></i>
                </div>
                <div class="message-content p-3 rounded">
                    <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(typingElement);
        scrollToBottom();
    }
    
    /**
     * Format bot message with Markdown-like syntax
     * Simple formatting for bold, lists, and new lines
     */
    function formatBotMessage(message) {
        // Convert line breaks
        let formattedMessage = message.replace(/\n/g, '<br>');
        
        // Bold text (between ** **)
        formattedMessage = formattedMessage.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Convert lists (starting with - or * followed by space)
        formattedMessage = formattedMessage.replace(/(?:^|\<br\>)[\-\*]\s(.*?)(?=$|\<br\>)/g, 
            '<br>• $1');
        
        return formattedMessage;
    }
    
    /**
     * Scroll chat to bottom
     */
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    /**
     * Send chat message to backend
     */
    function sendChatMessage(message, filters) {
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                filters: filters
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                addBotMessage(data.response);
            } else {
                addBotMessage('Sorry, I encountered an error. Please try again.');
                console.error('Error from server:', data.message);
            }
        })
        .catch(error => {
            addBotMessage('Sorry, I encountered an error. Please try again.');
            console.error('Fetch error:', error);
        });
    }
    
    /**
     * Update chart with new filters
     */
    function updateChartWithFilters(filters) {
        const queryParams = new URLSearchParams();
        
        if (filters.soil) queryParams.append('soil', filters.soil);
        if (filters.month) queryParams.append('month', filters.month);
        if (filters.season) queryParams.append('season', filters.season);
        if (filters.land_type) queryParams.append('land_type', filters.land_type);
        if (filters.land_size) queryParams.append('land_size', filters.land_size);
        
        fetch(`/api/recommendations?${queryParams.toString()}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    // Update chart with new data
                    updateCropChart(data.data);
                } else {
                    console.error('Error getting chart data:', data.message);
                }
            })
            .catch(error => {
                console.error('Fetch error for chart data:', error);
            });
    }
    
    // Language functions removed - English only application
    
    // Initialize the chart with default data
    updateChartWithFilters({});
    
    // Initialize carousel for farming tips
    const tipsCarousel = document.getElementById('tips-carousel');
    if (tipsCarousel) {
        new bootstrap.Carousel(tipsCarousel, {
            interval: 5000,
            ride: 'carousel'
        });
    }
});
