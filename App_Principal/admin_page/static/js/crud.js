function enviarFormularioEditar() {
    // Capturar los datos del formulario
    document.getElementById('formulario-editar').style.display = 'block';
    var nombre = document.getElementById('nombre').value;
    var apellido = document.getElementById('apellido').value;
    // Obtener el ID del usuario desde alguna fuente, por ejemplo, un atributo data en el botón "Editar"
    var userId = document.getElementById('boton-editar').dataset.id;

    // Crear un objeto con los datos del formulario
    var formData = new FormData();
    formData.append('nombre', nombre);
    formData.append('apellido', apellido);
    formData.append('user_id', userId); // Asegúrate de enviar el ID del usuario

    // Enviar los datos al servidor mediante una petición AJAX
    fetch('/editar_usuario/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}', // Asegúrate de incluir el token CSRF
        },
    })
    .then(response => {
        // Manejar la respuesta del servidor
        if (response.ok) {
            // Actualizar la vista o realizar alguna acción adicional
            console.log('Usuario editado correctamente');
            // Cerrar el formulario emergente
            cerrarFormularioEditar();
        } else {
            console.error('Error al editar usuario');
        }
    })
    .catch(error => {
        console.error('Error de red:', error);
    });
}