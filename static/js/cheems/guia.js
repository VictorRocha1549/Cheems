function guias(){
    const guia = document.getElementById('searchList').value;

    if (!guia) {
        alert('Por favor, ingresa un número de guía válido.');
        return;
    }
    
    const data = {guia};
    fetch('/guia', {
        method: 'POST',
        headers:{'Content-Type' : 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.status === 201) {
            window.location.href = `/guia?guia=${encodeURIComponent(guia)}`;
        } else {
            // Leer el mensaje de error del servidor si está disponible
            response.text().then(message => {
                alert(`Ocurrió un error al buscar: ${response.status}. ${message}`);
            });
        }
    })
    .catch(error => console.error('Error:', error));
}
