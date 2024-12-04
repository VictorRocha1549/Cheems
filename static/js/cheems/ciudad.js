function registro(id){
    var url = "/ciudad-registro";
    $.get(url, function(data){
        $('#modal_info').html(data);
        $('#modal_info').modal({backdrop: 'static', keyboard: false});
        $('#modal_info').modal('show');
    })
}

function editar(id){
    var url = `/ciudad/${id}`;
    $.get(url, function(data){
        $('#modal_info').html(data);
        $('#modal_info').modal({backdrop: 'static', keyboard: false});
        $('#modal_info').modal('show');
    })
}


function save(){
    const nombre = document.getElementById('form-nombre').value;
    const codigo = document.getElementById('form-codigo').value;

    const data = {nombre, codigo};
    fetch('/ciudad', {
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

function edit(id) {
    if (!id) {
        alert('ID de la ciudad no proporcionado.');
        return;
    }

    const nombre = document.getElementById('form-nombre').value.trim();
    const codigo = document.getElementById('form-codigo').value.trim();

    if (!nombre || !codigo) {
        alert('Por favor, complete todos los campos.');
        return;
    }

    const data = { nombre, codigo };
    fetch(`/ciudad/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.status === 201) {
            alert('El registro se actualizó correctamente');
            location.reload();
        } else if (response.status === 404) {
            alert('El registro no existe o ya fue eliminado.');
        } else {
            return response.json().then(err => alert(`Error: ${err.error}`));
        }
    })
    .catch(error => console.error('Error al actualizar:', error));
}

