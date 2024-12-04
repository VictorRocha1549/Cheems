// Aquí pones tu código JavaScript necesario
document.getElementById('trackButton').addEventListener('click', function() {
    var guia = document.getElementById('searchList').value;
    if(guia.length === 10) {  // Asegúrate de que la guía tiene la longitud correcta
        window.location.href = `/guia/${guia}`;  // Redirige a guia.html pasando el número de guía
    } else {
        alert("Por favor ingresa un número de rastreo válido.");
    }
});



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