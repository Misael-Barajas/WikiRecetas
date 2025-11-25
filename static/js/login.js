document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('terms');
    const btnRegistrar = document.getElementById('btnRegistrar');
    
    function toggleButton() {
        if (checkbox.checked) {
            btnRegistrar.removeAttribute('disabled');
        } else {
            btnRegistrar.setAttribute('disabled', 'true');
        }
    }
    
    checkbox.addEventListener('change', toggleButton);
    });