// Enable Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});

// Add confirmation for delete actions
document.querySelectorAll('.btn-danger').forEach(button => {
    button.addEventListener('click', (e) => {
        if (!confirm('Are you sure you want to proceed with this action?')) {
            e.preventDefault();
        }
    });
});
