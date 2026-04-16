document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analysis-form');
    const resumeInput = document.getElementById('resume-input');
    const fileNameDisplay = document.getElementById('file-name-display');
    const dropzone = document.getElementById('dropzone');
    
    // UI Panels
    const emptyState = document.getElementById('empty-state');
    const resultsDashboard = document.getElementById('results-dashboard');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    // Result elements
    const matchScore = document.getElementById('match-score');
    const matchProgress = document.getElementById('match-progress');
    const presentCount = document.getElementById('present-count');
    const missingCount = document.getElementById('missing-count');
    const presentTags = document.getElementById('present-skills-tags');
    const missingTags = document.getElementById('missing-skills-tags');
    const recommendationsList = document.getElementById('recommendations-list');
    
    let chartInstance = null;

    // File input changes
    resumeInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileNameDisplay.textContent = e.target.files[0].name;
            dropzone.classList.add('border-primary', 'bg-primary/5');
        } else {
            fileNameDisplay.textContent = "PDF, TXT up to 5MB";
            dropzone.classList.remove('border-primary', 'bg-primary/5');
        }
    });

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!resumeInput.files.length) return;
        
        const formData = new FormData(form);
        
        // Show loading state
        emptyState.classList.add('hidden');
        resultsDashboard.classList.add('hidden');
        loadingIndicator.classList.remove('hidden');
        
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                renderDashboard(data);
            } else {
                alert(data.error || "An error occurred during analysis.");
                loadingIndicator.classList.add('hidden');
                emptyState.classList.remove('hidden');
            }
        } catch (error) {
            console.error("Error analyzing:", error);
            alert("Network error occurred.");
            loadingIndicator.classList.add('hidden');
            emptyState.classList.remove('hidden');
        }
    });
    
    function renderDashboard(data) {
        // Hide loading, show results
        loadingIndicator.classList.add('hidden');
        resultsDashboard.classList.remove('hidden');
        
        // Populate stats
        const score = data.match_percentage;
        matchScore.textContent = `${score}%`;
        
        // Color coding progress bar
        matchProgress.style.width = `${score}%`;
        if (score < 50) matchProgress.className = "bg-red-500 h-1.5 rounded-full transition-all duration-1000";
        else if (score < 75) matchProgress.className = "bg-yellow-500 h-1.5 rounded-full transition-all duration-1000";
        else matchProgress.className = "bg-green-500 h-1.5 rounded-full transition-all duration-1000";
        
        presentCount.textContent = data.present_skills.length;
        missingCount.textContent = data.missing_skills.length;
        
        // Populate tags
        presentTags.innerHTML = data.present_skills.map(s => 
            `<span class="px-3 py-1 bg-green-500/20 text-green-400 border border-green-500/30 rounded-full text-xs font-medium">${s}</span>`
        ).join('');
        
        missingTags.innerHTML = data.missing_skills.map(s => 
            `<span class="px-3 py-1 bg-red-500/20 text-red-400 border border-red-500/30 rounded-full text-xs font-medium">${s}</span>`
        ).join('');
        
        // Populate recommendations
        if (data.recommendations.length > 0) {
            recommendationsList.innerHTML = data.recommendations.map(s => `
                <li class="flex items-center p-3 rounded-xl bg-slate-800/50 border border-gray-700/50 hover:bg-slate-800 transition-colors">
                    <div class="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center mr-3">
                        <i class="fa-solid fa-arrow-trend-up text-primary text-xs"></i>
                    </div>
                    <div>
                        <p class="text-sm font-medium text-gray-200">Learn ${s}</p>
                        <p class="text-xs text-gray-500">High impact for this role</p>
                    </div>
                </li>
            `).join('');
        } else {
            recommendationsList.innerHTML = `<li class="text-sm text-gray-400 p-3">Excellent! You meet all listed requirements.</li>`;
        }
        
        // Render Chart
        renderChart(data.present_skills.length, data.missing_skills.length);
    }
    
    function renderChart(present, missing) {
        const ctx = document.getElementById('distributionChart').getContext('2d');
        
        if (chartInstance) {
            chartInstance.destroy();
        }
        
        chartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Present Skills', 'Missing Skills'],
                datasets: [{
                    data: [present, missing],
                    backgroundColor: [
                        'rgba(16, 185, 129, 0.8)', // Green
                        'rgba(239, 68, 68, 0.8)'   // Red
                    ],
                    borderColor: [
                        'rgba(16, 185, 129, 1)',
                        'rgba(239, 68, 68, 1)'
                    ],
                    borderWidth: 1,
                    cutout: '70%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#cbd5e1'
                        }
                    }
                }
            }
        });
    }
});
