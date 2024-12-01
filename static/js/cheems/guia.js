// Aquí pones tu código JavaScript necesario
document.getElementById('trackButton').addEventListener('click', function() {
    var guia = document.getElementById('searchList').value;
    if(guia.length === 10) {  // Asegúrate de que la guía tiene la longitud correcta
        window.location.href = `/guia/${guia}`;  // Redirige a guia.html pasando el número de guía
    } else {
        alert("Por favor ingresa un número de rastreo válido.");
    }
});
