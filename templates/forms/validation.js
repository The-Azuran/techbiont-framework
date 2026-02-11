/* Validation Framework - MESO Forms v2.0 */

// Validation presets (injected from YAML)
const VALIDATION_PRESETS = {{VALIDATION_PRESETS}};

// Validation rule functions
const validators = {
    required: (value) => {
        if (typeof value === 'string') {
            return value.trim().length > 0;
        }
        return value !== null && value !== undefined && value !== '';
    },

    pattern: (value, regex) => {
        if (!value) return true; // Empty is valid (use 'required' for required fields)
        try {
            return new RegExp(regex).test(value);
        } catch (error) {
            console.error('Invalid regex pattern:', regex, error);
            return false; // Treat invalid regex as validation failure
        }
    },

    min_length: (value, min) => {
        if (!value) return true;
        return value.length >= min;
    },

    max_length: (value, max) => {
        if (!value) return true;
        return value.length <= max;
    },

    min: (value, min) => {
        if (!value) return true;
        return Number(value) >= min;
    },

    max: (value, max) => {
        if (!value) return true;
        return Number(value) <= max;
    },

    email: (value) => {
        if (!value) return true;
        return /^[^@]+@[^@]+\.[^@]+$/.test(value);
    },

    url: (value) => {
        if (!value) return true;
        return /^https?:\/\/.*/.test(value);
    },

    slug: (value) => {
        if (!value) return true;
        return /^[a-z0-9-]+$/.test(value);
    }
};

// Default error messages
const defaultMessages = {
    required: 'This field is required',
    pattern: 'Invalid format',
    min_length: 'Too short',
    max_length: 'Too long',
    min: 'Value too low',
    max: 'Value too high',
    email: 'Enter a valid email address',
    url: 'Enter a valid URL',
    slug: 'Use lowercase letters, numbers, and hyphens only'
};

/**
 * Validate a field based on its validation rules
 * @param {HTMLElement} field - The input/textarea/select element
 * @param {Object} rules - Validation rules from data attributes
 * @returns {Object} - {valid: boolean, errors: string[]}
 */
function validateField(field, rules) {
    const value = field.value;
    const errors = [];

    // Apply preset if specified
    if (rules.preset && VALIDATION_PRESETS[rules.preset]) {
        const preset = VALIDATION_PRESETS[rules.preset];
        Object.assign(rules, preset);
    }

    // Check each validation rule
    for (const [rule, constraint] of Object.entries(rules)) {
        if (rule === 'preset' || rule === 'error_message') continue;

        const validator = validators[rule];
        if (validator && !validator(value, constraint)) {
            const errorMsg = rules.error_message || defaultMessages[rule] || 'Invalid value';
            errors.push(errorMsg);
            break; // Only show first error
        }
    }

    return {
        valid: errors.length === 0,
        errors: errors
    };
}

/**
 * Show validation error for a field
 */
function showError(field, errorMessage) {
    const questionDiv = field.closest('.question');
    if (!questionDiv) return;

    let errorDiv = questionDiv.querySelector('.error-message');

    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.setAttribute('role', 'alert');
        errorDiv.setAttribute('aria-live', 'assertive');
        errorDiv.setAttribute('aria-atomic', 'true');
        errorDiv.id = `${field.id}-error`;
        field.setAttribute('aria-describedby', errorDiv.id);

        // Insert after the field
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }

    errorDiv.textContent = errorMessage;
    errorDiv.hidden = false;
    field.setAttribute('aria-invalid', 'true');
    field.classList.add('invalid');
}

/**
 * Clear validation error for a field
 */
function clearError(field) {
    const questionDiv = field.closest('.question');
    if (!questionDiv) return;

    const errorDiv = questionDiv.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.hidden = true;
        errorDiv.textContent = '';
    }

    field.setAttribute('aria-invalid', 'false');
    field.classList.remove('invalid');
}

/**
 * Initialize validation for all fields with validation rules
 */
function initValidation() {
    const fields = document.querySelectorAll('[data-validation]');

    fields.forEach(field => {
        const rulesJson = field.getAttribute('data-validation');
        if (!rulesJson) return;

        let rules;
        try {
            rules = JSON.parse(rulesJson);
        } catch (e) {
            console.error('Invalid validation rules:', rulesJson);
            return;
        }

        // Validate on blur
        field.addEventListener('blur', () => {
            const result = validateField(field, rules);

            if (!result.valid) {
                showError(field, result.errors[0]);
            } else {
                clearError(field);
            }
        });

        // Clear error on input (after error shown)
        field.addEventListener('input', () => {
            if (field.classList.contains('invalid')) {
                const result = validateField(field, rules);
                if (result.valid) {
                    clearError(field);
                }
            }
        });
    });
}

/**
 * Validate all fields (used before form submission)
 * @returns {boolean} - True if all fields valid
 */
function validateAll() {
    const fields = document.querySelectorAll('[data-validation]');
    let allValid = true;
    let firstInvalidField = null;

    fields.forEach(field => {
        const rulesJson = field.getAttribute('data-validation');
        if (!rulesJson) return;

        let rules;
        try {
            rules = JSON.parse(rulesJson);
        } catch (e) {
            return;
        }

        const result = validateField(field, rules);

        if (!result.valid) {
            showError(field, result.errors[0]);
            allValid = false;
            if (!firstInvalidField) {
                firstInvalidField = field;
            }
        } else {
            clearError(field);
        }
    });

    // Focus first invalid field
    if (firstInvalidField) {
        firstInvalidField.focus();
        firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    return allValid;
}

// Initialize validation when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initValidation);
} else {
    initValidation();
}
