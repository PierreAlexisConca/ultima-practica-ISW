/**
 * Funciones JavaScript para la página principal (formulario de registro)
 */

/**
 * Muestra una alerta en la página
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo de alerta ('success' o 'error')
 */
function showAlert(message, type) {
    const alertContainer = document.getElementById('alertContainer');
    
    const alertClass = type === 'success' ? 
        'bg-green-50 border-green-500 text-green-700' : 
        'bg-red-50 border-red-500 text-red-700';
    
    const icon = type === 'success' ? 
        'fa-check-circle text-green-500' : 
        'fa-exclamation-circle text-red-500';
    
    alertContainer.innerHTML = `
        <div class="${alertClass} border-l-4 p-4 mb-6 rounded">
            <div class="flex items-center">
                <i class="fas ${icon} text-xl mr-3"></i>
                <p class="font-semibold">${message}</p>
            </div>
        </div>
    `;
    
    // Scroll suave al mensaje
    alertContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Maneja el envío del formulario de registro de leads
 * @param {Event} e - Evento del formulario
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    
    // Deshabilitar botón durante el envío
    submitBtn.disabled = true;
    btnText.textContent = 'Enviando...';
    
    // Recopilar datos del formulario
    const formData = {
        nombre_completo: document.getElementById('nombre_completo').value,
        correo_electronico: document.getElementById('correo_electronico').value,
        telefono: document.getElementById('telefono').value,
        interes: document.getElementById('interes').value
    };
    
    try {
        // Enviar petición POST a la API
        const response = await fetch('/api/leads', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Mostrar mensaje de éxito
            showAlert(data.message, 'success');
            
            // Limpiar formulario
            document.getElementById('leadForm').reset();
        } else {
            // Mostrar mensaje de error
            showAlert(data.message, 'error');
        }
    } catch (error) {
        // Manejar errores de conexión
        console.error('Error:', error);
        showAlert('Error de conexión. Por favor, intenta nuevamente.', 'error');
    } finally {
        // Rehabilitar botón
        submitBtn.disabled = false;
        btnText.textContent = 'Registrar Lead';
    }
}

/**
 * Inicialización cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', function() {
    // Adjuntar evento al formulario
    const leadForm = document.getElementById('leadForm');
    if (leadForm) {
        leadForm.addEventListener('submit', handleFormSubmit);
    }
    
    console.log('Formulario de leads inicializado correctamente');
});