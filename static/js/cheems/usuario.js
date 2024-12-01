function save(){
    const nombre = document.getElementById('form-nombre').value;
    const contrasenia = document.getElementById('form-contrasenia').value;
    const ciudad = document.getElementById('form-ciudad').value;

    if (!nombre || !contrasenia || !ciudad) {
        alert('Todos los campos son obligatorios.');
        return; // Detener la ejecución si hay campos vacíos
    }

    const data = {nombre, contrasenia, ciudad};
    fetch('/registro', {
        method: 'POST',
        headers:{'Content-Type' : 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.status === 201) {
            alert('El registro se guardó correctamente');
            location.reload();
        } else {
            alert(`Ocurrió un error al guardar: ${response.status}`);
        }
    })
    .catch(error => console.error('Error:', error));
}

function login(){
    const nombre = document.getElementById('form-nombre').value;
    const contrasenia = document.getElementById('form-contrasenia').value;

    if (!nombre || !contrasenia ) {
        alert('Todos los campos son obligatorios.');
        return; // Detener la ejecución si hay campos vacíos
    }

    const data = {nombre, contrasenia};
    fetch('/inicio', {
        method: 'POST',
        headers:{'Content-Type' : 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.status === 201) {
            alert('Se inicio sesion correctamente');
            window.location.href = '/inicio';
        } else {
            alert(`Ocurrió un error al iniciar sesion: ${response.status}`);
        }
    })
    .catch(error => console.error('Error:', error));
}
