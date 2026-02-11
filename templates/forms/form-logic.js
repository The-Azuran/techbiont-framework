/* Form Logic - Auto-save, Progress Tracking, Export */

const form = document.getElementById('form');
const progressFill = document.getElementById('progressFill');
const progressPercent = document.getElementById('progressPercent');
const answeredCount = document.getElementById('answeredCount');
const savedIndicator = document.getElementById('savedIndicator');

// Will be injected by form generator
const TOTAL_QUESTIONS = {{TOTAL_QUESTIONS}};
const STORAGE_KEY = '{{STORAGE_KEY}}';

function loadData() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
        const data = JSON.parse(saved);
        Object.keys(data).forEach(key => {
            const elements = form.elements[key];
            if (elements) {
                if (elements.length > 1) {
                    // Radio or checkbox group
                    for (let elem of elements) {
                        if (elem.type === 'radio') {
                            elem.checked = elem.value === data[key];
                        } else if (elem.type === 'checkbox') {
                            elem.checked = data[key] === true || data[key] === 'true';
                        }
                    }
                } else {
                    // Single element
                    if (elements.type === 'checkbox') {
                        elements.checked = data[key] === true || data[key] === 'true';
                    } else {
                        elements.value = data[key] || '';
                    }
                }
            }
        });
        updateProgress();
    }
}

function saveData() {
    const formData = new FormData(form);
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    // Also save unchecked checkboxes
    form.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        if (!data[cb.name]) {
            data[cb.name] = cb.checked;
        }
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));

    if (savedIndicator) {
        savedIndicator.classList.add('show');
        setTimeout(() => {
            savedIndicator.classList.remove('show');
        }, 2000);
    }
}

function updateProgress() {
    const questions = form.querySelectorAll('[data-question]');
    let answered = 0;

    questions.forEach(q => {
        const radios = q.querySelectorAll('input[type="radio"]');
        if (radios.length > 0) {
            // Get unique names
            const names = new Set();
            radios.forEach(r => names.add(r.name));
            // Check if any radio group is answered
            let hasAnswer = false;
            names.forEach(name => {
                if (form.querySelector(`input[name="${name}"]:checked`)) {
                    hasAnswer = true;
                }
            });
            if (hasAnswer) answered++;
        } else {
            // Has textareas or other inputs
            const inputs = q.querySelectorAll('textarea, input[type="text"], input[type="number"]');
            if (Array.from(inputs).some(i => i.value.trim())) {
                answered++;
            }
        }
    });

    const percent = Math.round((answered / TOTAL_QUESTIONS) * 100);
    if (progressFill) progressFill.style.width = percent + '%';
    if (progressPercent) progressPercent.textContent = percent;
    if (answeredCount) answeredCount.textContent = answered;
}

form.addEventListener('change', () => {
    saveData();
    updateProgress();
});

form.addEventListener('input', () => {
    saveData();
    updateProgress();
});

// Option highlighting
document.querySelectorAll('.option input[type="radio"]').forEach(radio => {
    radio.addEventListener('change', () => {
        const name = radio.name;
        document.querySelectorAll(`input[name="${name}"]`).forEach(r => {
            r.closest('.option')?.classList.remove('selected');
        });
        if (radio.checked) {
            radio.closest('.option')?.classList.add('selected');
        }
    });
});

document.getElementById('exportBtn')?.addEventListener('click', () => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
        const data = JSON.parse(saved);
        const exportData = {
            formTitle: document.querySelector('h1')?.textContent || 'Form',
            exportDate: new Date().toISOString(),
            data: data
        };
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = '{{EXPORT_FILENAME}}';
        a.click();
        URL.revokeObjectURL(url);
    } else {
        alert('No data to export. Fill out the form first.');
    }
});

document.getElementById('saveBtn')?.addEventListener('click', () => {
    saveData();
    alert('✓ Progress saved! (Also auto-saves as you type)');
});

document.getElementById('clearBtn')?.addEventListener('click', () => {
    if (confirm('⚠️ Are you sure you want to clear all your answers?')) {
        localStorage.removeItem(STORAGE_KEY);
        form.reset();
        updateProgress();
        document.querySelectorAll('.option.selected').forEach(opt => {
            opt.classList.remove('selected');
        });
        alert('✓ Form cleared.');
    }
});

document.getElementById('printBtn')?.addEventListener('click', () => {
    window.print();
});

// Range slider value display
document.querySelectorAll('.range-input input[type="range"]').forEach(slider => {
    const output = slider.nextElementSibling;
    if (output && output.tagName === 'OUTPUT') {
        slider.addEventListener('input', () => {
            const unit = output.textContent.match(/[^0-9.-]+$/)?.[0] || '';
            output.textContent = slider.value + unit;
        });
    }
});

// Importance gauge updates
document.querySelectorAll('.importance-gauge input[type="range"]').forEach(slider => {
    const gaugeFill = slider.closest('.importance-gauge').querySelector('.gauge-fill');
    const currentValue = slider.closest('.importance-gauge').querySelector('.gauge-current-value');

    slider.addEventListener('input', () => {
        const min = parseFloat(slider.min);
        const max = parseFloat(slider.max);
        const value = parseFloat(slider.value);
        const percent = ((value - min) / (max - min)) * 100;

        if (gaugeFill) {
            gaugeFill.style.width = percent + '%';
            gaugeFill.setAttribute('data-value', value);
        }

        if (currentValue) {
            currentValue.textContent = value;
        }
    });
});

// Initialize
loadData();
updateProgress();
document.querySelectorAll('input[type="radio"]:checked').forEach(radio => {
    radio.closest('.option')?.classList.add('selected');
});

/* Keyboard Navigation for Star Rating and Likert Scales */

// Arrow key navigation for star ratings
document.querySelectorAll('.star-rating').forEach(fieldset => {
    const inputs = Array.from(fieldset.querySelectorAll('input[type="radio"]'));
    if (inputs.length === 0) return;

    // Reverse the array because stars are rendered in reverse order
    const starsInOrder = inputs.reverse();

    fieldset.addEventListener('keydown', (e) => {
        if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) return;

        e.preventDefault();
        const currentIndex = starsInOrder.findIndex(input => input === document.activeElement);

        if (currentIndex === -1) {
            // No star focused, focus the first one
            starsInOrder[0].focus();
            return;
        }

        let nextIndex = currentIndex;
        if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
            nextIndex = Math.min(currentIndex + 1, starsInOrder.length - 1);
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
            nextIndex = Math.max(currentIndex - 1, 0);
        }

        if (nextIndex !== currentIndex) {
            starsInOrder[nextIndex].focus();
            starsInOrder[nextIndex].checked = true;
            starsInOrder[nextIndex].dispatchEvent(new Event('change', { bubbles: true }));
        }
    });

    // Make labels focusable and forward focus to inputs
    fieldset.querySelectorAll('label').forEach((label, idx) => {
        label.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const input = fieldset.querySelector(`#${label.getAttribute('for')}`);
                if (input) {
                    input.checked = true;
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    saveData();
                }
            }
        });
    });
});

// Arrow key navigation for likert scales
document.querySelectorAll('.likert-scale').forEach(fieldset => {
    const inputs = Array.from(fieldset.querySelectorAll('input[type="radio"]'));
    if (inputs.length === 0) return;

    fieldset.addEventListener('keydown', (e) => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) return;

        e.preventDefault();
        const currentIndex = inputs.findIndex(input => input === document.activeElement);

        let nextIndex = currentIndex;
        if (e.key === 'ArrowRight') {
            nextIndex = currentIndex === -1 ? 0 : Math.min(currentIndex + 1, inputs.length - 1);
        } else if (e.key === 'ArrowLeft') {
            nextIndex = currentIndex === -1 ? 0 : Math.max(currentIndex - 1, 0);
        } else if (e.key === 'Home') {
            nextIndex = 0;
        } else if (e.key === 'End') {
            nextIndex = inputs.length - 1;
        }

        if (nextIndex !== -1) {
            inputs[nextIndex].focus();
            inputs[nextIndex].checked = true;
            inputs[nextIndex].dispatchEvent(new Event('change', { bubbles: true }));
            saveData();
        }
    });

    // Space/Enter to select
    inputs.forEach(input => {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                input.checked = true;
                input.dispatchEvent(new Event('change', { bubbles: true }));
                saveData();
            }
        });
    });
});
