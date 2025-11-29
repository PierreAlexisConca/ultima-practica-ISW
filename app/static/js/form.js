document.getElementById('leadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch('/api/leads', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        const mensaje = document.getElementById('mensaje');
        
        if (result.success) {
            mensaje.className = 'alert alert-success mt-3';
            mensaje.innerHTML = '<i class="fas fa-check-circle"></i> ' + result.message;
            e.target.reset();
        } else {
            mensaje.className = 'alert alert-danger mt-3';
            mensaje.innerHTML = '<i class="fas fa-times-circle"></i> ' + result.message;
        }
        mensaje.style.display = 'block';
    } catch (error) {
        const mensaje = document.getElementById('mensaje');
        mensaje.className = 'alert alert-danger mt-3';
        mensaje.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error en la solicitud';
        mensaje.style.display = 'block';
    }
});
