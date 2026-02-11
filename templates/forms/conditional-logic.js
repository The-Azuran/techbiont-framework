/* Conditional Logic - MESO Forms v2.0 */

/**
 * Simple expression evaluator for conditional logic
 * Supports: ==, !=, >, <, >=, <=, AND, OR, is_empty, is_filled, contains
 */

/**
 * Get the current value of a field by ID
 */
function getFieldValue(fieldId) {
    // Try radio buttons first
    const radio = document.querySelector(`input[name="${fieldId}"]:checked`);
    if (radio) return radio.value;

    // Try checkbox
    const checkbox = document.querySelector(`input[name="${fieldId}"][type="checkbox"]`);
    if (checkbox) return checkbox.checked;

    // Try regular input/textarea/select
    const field = document.getElementById(fieldId) || document.querySelector(`[name="${fieldId}"]`);
    if (field) return field.value;

    return null;
}

/**
 * Evaluate a simple condition expression
 * Examples:
 *   "deployment-target == 'cloud'"
 *   "budget > 1000"
 *   "email is_filled"
 *   "deployment-target == 'cloud' AND budget > 1000"
 */
function evaluateExpression(expr) {
    if (!expr || expr.trim() === '') return true;

    // Handle AND/OR by splitting
    if (expr.includes(' AND ')) {
        const parts = expr.split(' AND ');
        return parts.every(part => evaluateExpression(part.trim()));
    }

    if (expr.includes(' OR ')) {
        const parts = expr.split(' OR ');
        return parts.some(part => evaluateExpression(part.trim()));
    }

    // Handle unary operators (is_empty, is_filled)
    const isEmptyMatch = expr.match(/^(\S+)\s+is_empty$/);
    if (isEmptyMatch) {
        const value = getFieldValue(isEmptyMatch[1]);
        return !value || value.toString().trim() === '';
    }

    const isFilledMatch = expr.match(/^(\S+)\s+is_filled$/);
    if (isFilledMatch) {
        const value = getFieldValue(isFilledMatch[1]);
        return value && value.toString().trim() !== '';
    }

    // Handle contains operator
    const containsMatch = expr.match(/^(\S+)\s+contains\s+['"](.+)['"]$/);
    if (containsMatch) {
        const value = getFieldValue(containsMatch[1]);
        const searchTerm = containsMatch[2];
        return value && value.toString().includes(searchTerm);
    }

    // Handle comparison operators (==, !=, >, <, >=, <=)
    const comparisonMatch = expr.match(/^(\S+)\s+(==|!=|>=|<=|>|<)\s+['"]?(.+?)['"]?$/);
    if (comparisonMatch) {
        const fieldId = comparisonMatch[1];
        const operator = comparisonMatch[2];
        let expectedValue = comparisonMatch[3].replace(/^['"]|['"]$/g, ''); // Remove quotes

        const actualValue = getFieldValue(fieldId);

        // Try numeric comparison first
        const actualNum = Number(actualValue);
        const expectedNum = Number(expectedValue);

        if (!isNaN(actualNum) && !isNaN(expectedNum)) {
            switch (operator) {
                case '==': return actualNum === expectedNum;
                case '!=': return actualNum !== expectedNum;
                case '>': return actualNum > expectedNum;
                case '<': return actualNum < expectedNum;
                case '>=': return actualNum >= expectedNum;
                case '<=': return actualNum <= expectedNum;
            }
        }

        // Fall back to string comparison
        const actualStr = actualValue ? actualValue.toString() : '';
        const expectedStr = expectedValue.toString();

        switch (operator) {
            case '==': return actualStr === expectedStr;
            case '!=': return actualStr !== expectedStr;
            case '>': return actualStr > expectedStr;
            case '<': return actualStr < expectedStr;
            case '>=': return actualStr >= expectedStr;
            case '<=': return actualStr <= expectedStr;
        }
    }

    console.warn('Could not evaluate expression:', expr);
    return true; // Default to showing the field
}

/**
 * Announce conditional field visibility changes to screen readers
 */
function announceFieldChange(fieldTitle, visible) {
    let statusRegion = document.getElementById('conditional-status');
    if (!statusRegion) {
        statusRegion = document.createElement('div');
        statusRegion.id = 'conditional-status';
        statusRegion.setAttribute('role', 'status');
        statusRegion.setAttribute('aria-live', 'polite');
        statusRegion.setAttribute('aria-atomic', 'true');
        statusRegion.className = 'sr-only';
        document.body.appendChild(statusRegion);
    }

    const message = visible ? `${fieldTitle} question now visible` : `${fieldTitle} question hidden`;
    statusRegion.textContent = message;

    // Clear after announcement to avoid repeat readings
    setTimeout(() => { statusRegion.textContent = ''; }, 1000);
}

/**
 * Update visibility of conditional fields
 */
function updateConditionalFields() {
    // Handle show_if conditions
    document.querySelectorAll('[data-show-if]').forEach(field => {
        const condition = field.getAttribute('data-show-if');
        const shouldShow = evaluateExpression(condition);

        const questionDiv = field.closest('.question');
        if (questionDiv) {
            const wasVisible = questionDiv.style.display !== 'none';

            if (shouldShow) {
                questionDiv.style.display = '';
                questionDiv.setAttribute('aria-hidden', 'false');

                // Announce if transitioning from hidden to visible
                if (!wasVisible) {
                    const questionTitle = questionDiv.querySelector('.question-title, legend, label');
                    const title = questionTitle ? questionTitle.textContent : 'A question';
                    announceFieldChange(title, true);
                }
            } else {
                questionDiv.style.display = 'none';
                questionDiv.setAttribute('aria-hidden', 'true');

                // Announce if transitioning from visible to hidden
                if (wasVisible) {
                    const questionTitle = questionDiv.querySelector('.question-title, legend, label');
                    const title = questionTitle ? questionTitle.textContent : 'A question';
                    announceFieldChange(title, false);
                }

                // Clear value when hidden
                if (field.type === 'radio' || field.type === 'checkbox') {
                    field.checked = false;
                } else {
                    field.value = '';
                }
            }
        }
    });

    // Handle required_if conditions
    document.querySelectorAll('[data-required-if]').forEach(field => {
        const condition = field.getAttribute('data-required-if');
        const shouldBeRequired = evaluateExpression(condition);

        if (shouldBeRequired) {
            field.setAttribute('required', 'true');
            field.setAttribute('aria-required', 'true');

            // Update validation rules
            const validationRules = field.getAttribute('data-validation');
            if (validationRules) {
                try {
                    const rules = JSON.parse(validationRules);
                    rules.required = true;
                    field.setAttribute('data-validation', JSON.stringify(rules));
                } catch (e) {
                    // If no validation rules, add required
                    field.setAttribute('data-validation', JSON.stringify({ required: true }));
                }
            } else {
                field.setAttribute('data-validation', JSON.stringify({ required: true }));
            }
        } else {
            field.removeAttribute('required');
            field.setAttribute('aria-required', 'false');

            // Update validation rules
            const validationRules = field.getAttribute('data-validation');
            if (validationRules) {
                try {
                    const rules = JSON.parse(validationRules);
                    delete rules.required;
                    field.setAttribute('data-validation', JSON.stringify(rules));
                } catch (e) {}
            }
        }
    });

    // Handle disabled_if conditions
    document.querySelectorAll('[data-disabled-if]').forEach(field => {
        const condition = field.getAttribute('data-disabled-if');
        const shouldBeDisabled = evaluateExpression(condition);

        field.disabled = shouldBeDisabled;

        if (shouldBeDisabled) {
            field.setAttribute('aria-disabled', 'true');
            field.classList.add('disabled');
        } else {
            field.setAttribute('aria-disabled', 'false');
            field.classList.remove('disabled');
        }
    });
}

/**
 * Initialize conditional logic
 */
function initConditionalLogic() {
    // Update on page load
    updateConditionalFields();

    // Update on any form change
    const form = document.getElementById('form');
    if (form) {
        form.addEventListener('change', updateConditionalFields);
        form.addEventListener('input', updateConditionalFields);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initConditionalLogic);
} else {
    initConditionalLogic();
}
