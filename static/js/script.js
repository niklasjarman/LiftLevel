// Handle workout form submission
document.getElementById('workout-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        exercise_id: parseInt(document.getElementById('exercise').value),
        weight: parseFloat(document.getElementById('weight').value),
        reps: parseInt(document.getElementById('reps').value),
        sets: parseInt(document.getElementById('sets').value)
    };
    
    const resultDiv = document.getElementById('workout-result');
    resultDiv.className = 'workout-result';
    resultDiv.textContent = 'Logging workout...';
    resultDiv.style.display = 'block';
    
    try {
        const response = await fetch('/api/log-workout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.className = 'workout-result success';
            resultDiv.textContent = `✅ Workout logged! Earned ${data.xp_earned} XP. Total: ${data.total_xp} XP`;
            
            // Update UI
            updateUserStats(data);
            addWorkoutToHistory(formData, data);
            
            // Check for level up
            if (data.leveled_up) {
                showLevelUpModal(data.level);
            }
            
            // Reset form
            document.getElementById('workout-form').reset();
            
            // Hide result message after 5 seconds
            setTimeout(() => {
                resultDiv.style.display = 'none';
            }, 5000);
        } else {
            throw new Error('Failed to log workout');
        }
    } catch (error) {
        resultDiv.className = 'workout-result error';
        resultDiv.textContent = '❌ Error logging workout. Please try again.';
        console.error('Error:', error);
    }
});

// Update user stats on the page
function updateUserStats(data) {
    // Update level
    const levelElements = document.querySelectorAll('.level-number');
    levelElements.forEach(el => {
        el.textContent = `Level ${data.level}`;
    });
    
    // Update XP total
    const xpTotalElements = document.querySelectorAll('.xp-total');
    xpTotalElements.forEach(el => {
        el.textContent = `${data.total_xp} XP`;
    });
    
    // Update XP bar with animation
    const xpBar = document.querySelector('.xp-bar');
    xpBar.style.width = `${data.xp_progress.percentage}%`;
    
    // Update XP text
    const xpTextElements = document.querySelectorAll('.xp-text');
    xpTextElements.forEach(el => {
        el.textContent = `${data.xp_progress.current} / ${data.xp_progress.needed} XP to Level ${data.level + 1}`;
    });
    
    // Update character image
    const characterImage = document.getElementById('character-image');
    const newImageSrc = `/static/images/level_${data.level}.png`;
    characterImage.src = newImageSrc;
    characterImage.alt = `Level ${data.level} Character`;
    characterImage.onerror = function() {
        this.src = '/static/images/placeholder.svg';
    };
    
    // Update character label
    const characterLabel = document.querySelector('.character-label');
    characterLabel.textContent = `Level ${data.level} Evolution`;
}

// Add workout to history
function addWorkoutToHistory(formData, responseData) {
    const historyDiv = document.getElementById('workout-history');
    const noHistory = historyDiv.querySelector('.no-history');
    
    if (noHistory) {
        noHistory.remove();
    }
    
    // Get exercise name from select
    const exerciseSelect = document.getElementById('exercise');
    const selectedOption = exerciseSelect.options[exerciseSelect.selectedIndex];
    const exerciseName = selectedOption.text.split(' (')[0]; // Remove category from name
    
    const workoutEntry = document.createElement('div');
    workoutEntry.className = 'workout-entry';
    workoutEntry.style.animation = 'slideIn 0.3s ease';
    
    const date = new Date();
    const dateStr = date.toISOString().split('T')[0];
    
    workoutEntry.innerHTML = `
        <div class="workout-header">
            <span class="workout-exercise">${exerciseName}</span>
            <span class="workout-xp">+${responseData.xp_earned} XP</span>
        </div>
        <div class="workout-details">
            ${formData.weight} lbs × ${formData.reps} reps × ${formData.sets} sets
        </div>
        <div class="workout-date">${dateStr}</div>
    `;
    
    historyDiv.insertBefore(workoutEntry, historyDiv.firstChild);
    
    // Remove old entries if more than 10
    const entries = historyDiv.querySelectorAll('.workout-entry');
    if (entries.length > 10) {
        entries[entries.length - 1].remove();
    }
}

// Show level up modal
function showLevelUpModal(newLevel) {
    const modal = document.getElementById('level-up-modal');
    const newLevelSpan = document.getElementById('new-level');
    newLevelSpan.textContent = newLevel;
    modal.style.display = 'block';
    
    // Add celebration effect
    document.body.style.overflow = 'hidden';
}

// Close level up modal
function closeLevelUpModal() {
    const modal = document.getElementById('level-up-modal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('level-up-modal');
    if (event.target === modal) {
        closeLevelUpModal();
    }
}

// Close modal with X button
document.querySelector('.close').addEventListener('click', closeLevelUpModal);

// Add smooth scroll behavior
document.documentElement.style.scrollBehavior = 'smooth';

// Reset character functionality
document.getElementById('reset-btn').addEventListener('click', async () => {
    const confirmed = confirm(
        'Are you sure you want to reset your character?\n\n' +
        'This will:\n' +
        '• Reset your XP to 0\n' +
        '• Reset your level to 1\n' +
        '• Clear all workout history\n\n' +
        'This action cannot be undone!'
    );
    
    if (!confirmed) {
        return;
    }
    
    try {
        const response = await fetch('/api/reset-character', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update UI
            updateUserStats(data);
            
            // Clear workout history
            const historyDiv = document.getElementById('workout-history');
            historyDiv.innerHTML = '<p class="no-history">No workouts logged yet. Start your journey!</p>';
            
            // Show success message
            alert('Character reset successfully! You\'re back to Level 1.');
            
            // Reload page to ensure everything is in sync
            window.location.reload();
        } else {
            throw new Error('Failed to reset character');
        }
    } catch (error) {
        alert('Error resetting character. Please try again.');
        console.error('Error:', error);
    }
});

