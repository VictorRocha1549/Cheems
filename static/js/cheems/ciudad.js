function registro(id) {
    var url = "/ciudad-registro/" + id;  // Asegúrate de que esta ruta sea correcta en Flask
    $.get(url, function(data) {
        $('#modal_info').html(data); // Se asegura de que el modal se actualice con la información de la ciudad
        $('#modal_info').modal({backdrop: 'static', keyboard: false});
        $('#modal_info').modal('show');
    });
}
function save(id) {
    const nombre = document.getElementById('form-nombre').value;
    const codigo = document.getElementById('form-codigo').value;

    const data = { nombre, codigo };

    // Asegúrate de que la URL esté correcta y use el método PUT para la actualización
    fetch('/ciudad/' + id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.status === 200) {
            alert('Ciudad actualizada correctamente');
            location.reload();  // Recarga la página para ver los cambios
        } else {
            alert(`Ocurrió un error al actualizar: ${response.status}`);
        }
    })
    .catch(error => console.error('Error:', error));
}
