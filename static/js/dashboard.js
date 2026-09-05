/* ============================================
   UFA KENYA - DASHBOARD JAVASCRIPT
   All dashboard functionality
   ============================================ */

// ============================================
// 1. CHART INITIALIZATION
// ============================================

function initMemberGrowthChart(ctx, data) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'New Members',
                data: data.values || [12, 19, 15, 25, 22, 30],
                backgroundColor: 'rgba(21, 101, 192, 0.2)',
                borderColor: 'rgba(21, 101, 192, 1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 5
                    }
                }
            }
        }
    });
}

function initMembershipDistributionChart(ctx, data) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels || ['Youth', 'Student', 'Individual', 'Senior', 'Lifetime'],
            datasets: [{
                data: data.values || [45, 25, 15, 10, 5],
                backgroundColor: [
                    'rgba(21, 101, 192, 0.8)',
                    'rgba(46, 125, 50, 0.8)',
                    'rgba(249, 168, 37, 0.8)',
                    'rgba(198, 40, 40, 0.8)',
                    'rgba(108, 117, 125, 0.8)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        fontSize: 11,
                        boxWidth: 12
                    }
                }
            },
            cutout: '70%'
        }
    });
}

function initEventParticipationChart(ctx, data) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels || ['Workshop', 'Seminar', 'Conference', 'Training', 'Webinar', 'Social'],
            datasets: [{
                label: 'Registrations',
                data: data.values || [45, 30, 55, 40, 25, 20],
                backgroundColor: [
                    'rgba(21, 101, 192, 0.8)',
                    'rgba(46, 125, 50, 0.8)',
                    'rgba(249, 168, 37, 0.8)',
                    'rgba(198, 40, 40, 0.8)',
                    'rgba(108, 117, 125, 0.8)',
                    'rgba(21, 101, 192, 0.6)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function initProjectStatusChart(ctx, data) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels || ['Planning', 'Ongoing', 'Completed', 'On Hold', 'Cancelled'],
            datasets: [{
                data: data.values || [8, 12, 15, 3, 2],
                backgroundColor: [
                    'rgba(249, 168, 37, 0.8)',
                    'rgba(21, 101, 192, 0.8)',
                    'rgba(46, 125, 50, 0.8)',
                    'rgba(198, 40, 40, 0.8)',
                    'rgba(108, 117, 125, 0.8)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        fontSize: 12,
                        boxWidth: 14
                    }
                }
            },
            cutout: '65%'
        }
    });
}

function initMonthlyTrendsChart(ctx, data) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [
                {
                    label: 'New Members',
                    data: data.members || [12, 15, 18, 22, 25, 30, 28, 35, 40, 38, 42, 45],
                    borderColor: 'rgba(21, 101, 192, 1)',
                    backgroundColor: 'rgba(21, 101, 192, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Event Registrations',
                    data: data.registrations || [8, 10, 15, 20, 18, 25, 22, 30, 28, 32, 35, 40],
                    borderColor: 'rgba(46, 125, 50, 1)',
                    backgroundColor: 'rgba(46, 125, 50, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Events',
                    data: data.events || [3, 4, 5, 6, 5, 8, 7, 9, 8, 10, 11, 12],
                    borderColor: 'rgba(249, 168, 37, 1)',
                    backgroundColor: 'rgba(249, 168, 37, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        fontSize: 12
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// ============================================
// 2. DASHBOARD STATS UPDATER
// ============================================

function updateDashboardStats() {
    fetch('/dashboard/api/stats/')
        .then(response => response.json())
        .then(data => {
            document.querySelectorAll('.stat-number').forEach(el => {
                const label = el.closest('.stat-card')?.querySelector('.stat-label')?.textContent?.trim();
                if (label === 'Total Members') el.textContent = data.total_members;
                if (label === 'Active Members' || label === 'Total Members' && el.closest('.stat-card.green')) {
                    // Handle specific cases
                }
                if (label === 'Total Events') el.textContent = data.total_events;
                if (label === 'Upcoming Events') el.textContent = data.upcoming_events;
            });
        })
        .catch(error => console.error('Error fetching stats:', error));
}

// ============================================
// 3. NOTIFICATION SYSTEM
// ============================================

function showNotification(message, type = 'info') {
    const colors = {
        info: '#1565c0',
        success: '#2e7d32',
        warning: '#f9a825',
        danger: '#c62828'
    };
    
    const notification = document.createElement('div');
    notification.style.cssText = 
        position: fixed;
        top: 20px;
        right: 20px;
        background: ;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 5px 25px rgba(0,0,0,0.2);
        z-index: 9999;
        max-width: 400px;
        transform: translateX(400px);
        transition: transform 0.3s ease;
    ;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// ============================================
// 4. REPORT GENERATION
// ============================================

function generateReport(templateId, params = {}) {
    const url = /dashboard/api/report//?;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            showNotification('Report generated successfully!', 'success');
            console.log('Report data:', data);
        })
        .catch(error => {
            showNotification('Failed to generate report', 'danger');
            console.error('Error:', error);
        });
}

// ============================================
// 5. EVENT HANDLERS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Auto-refresh stats every 30 seconds
    setInterval(updateDashboardStats, 30000);
    
    // Handle report generation buttons
    document.querySelectorAll('.btn-generate-report').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const templateId = this.dataset.templateId;
            generateReport(templateId);
        });
    });
    
    // Handle refresh button
    document.querySelectorAll('.btn-refresh').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            updateDashboardStats();
            showNotification('Data refreshed!', 'success');
        });
    });
});

// ============================================
// 6. EXPORT FUNCTIONS
// ============================================

function exportChartAsImage(chartId, filename = 'chart.png') {
    const canvas = document.getElementById(chartId);
    if (canvas) {
        const link = document.createElement('a');
        link.download = filename;
        link.href = canvas.toDataURL('image/png');
        link.click();
    }
}

function exportDataAsCSV(data, filename = 'data.csv') {
    const csv = data.map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = filename;
    link.href = url;
    link.click();
}
