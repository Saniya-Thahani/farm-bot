// Charts and data visualization for FarmBot

let cropChart = null;

/**
 * Update the crop suitability chart with new data
 * @param {Object} data - The chart data with labels and values
 */
function updateCropChart(data) {
    const ctx = document.getElementById('cropChart');
    
    if (!ctx) return;
    
    // Default data if none provided
    const chartData = data || {
        labels: ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane'],
        values: [90, 75, 85, 60, 70]
    };
    
    // Destroy existing chart if it exists
    if (cropChart) {
        cropChart.destroy();
    }
    
    // Create new chart
    cropChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Crop Suitability Score',
                data: chartData.values,
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Suitability: ${context.raw}/100`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Suitability Score (0-100)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Crop Type'
                    }
                }
            }
        }
    });
}

// Initialize chart with default data when document is ready
document.addEventListener('DOMContentLoaded', function() {
    const cropChartCanvas = document.getElementById('cropChart');
    if (cropChartCanvas) {
        updateCropChart();
    }
});

/**
 * Create a radar chart comparing multiple crops
 * @param {string} canvasId - The ID of the canvas element
 * @param {Object} data - The chart data
 */
function createCropComparisonChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Water Requirements', 'Temperature Tolerance', 'Disease Resistance', 'Yield Potential', 'Growth Speed'],
            datasets: data.datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            elements: {
                line: {
                    borderWidth: 2
                }
            },
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }
        }
    });
}
