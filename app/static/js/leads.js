/**
 * Funciones JavaScript para la página de Leads
 */

/**
 * Elimina un lead después de confirmar con el usuario
 * @param {number} leadId - ID del lead a eliminar
 */
async function deleteLead(leadId) {
    // Mostrar confirmación al usuario
    if (!confirm('¿Estás seguro de que deseas eliminar este lead?')) {
        return;
    }

    try {
        // Realizar petición DELETE a la API
        const response = await fetch(`/api/leads/${leadId}`, {
            method: 'DELETE'
        });

        // Parsear respuesta JSON
        const data = await response.json();

        if (data.success) {
            // Recargar la página para mostrar los cambios
            location.reload();
        } else {
            // Mostrar mensaje de error
            alert('Error al eliminar: ' + data.message);
        }
    } catch (error) {
        // Manejar errores de conexión
        console.error('Error:', error);
        alert('Error de conexión. Por favor, intenta nuevamente.');
    }
}

/**
 * Inicialización cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Página de leads cargada correctamente');
    
    // Aquí puedes agregar más inicializaciones si las necesitas
    // Por ejemplo: actualización automática, búsqueda en tiempo real, etc.
});