from flask import Flask, request, render_template, jsonify, redirect, url_for
from entities.ciudad import Ciudad
from entities.envio import Envio
from entities.usuario import Usuario

app = Flask(__name__)

# Rutas para ciudades
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ciudades')
def ciudades():
    ciudades = Ciudad.get_all()
    return render_template('ciudades.html', ciudades=ciudades)

@app.route('/ciudad-registro', methods=['GET'])
def ciudad_registro():
    return render_template('ciudad.html')

@app.route('/ciudad', methods=['GET'])
def get_ciudades():
    ciudades = Ciudad.get_all()
    return jsonify(ciudades), 200

@app.route('/ciudad', methods=['POST'])
def save_ciudad():
    data = request.json
    ciudad = Ciudad(nombre=data['nombre'], codigo=data['codigo'])
    id = Ciudad.save(ciudad)
    return jsonify({'id': id}), 201

@app.route('/ciudad/<int:id>', methods=['PUT'])
def update_ciudad(id):
    data = request.json
    ciudad = Ciudad(nombre=data['nombre'], codigo=data['codigo'])
    result = Ciudad.update(id, ciudad)
    if result == 0:
        return jsonify({'error': 'El registro de ciudad no existe'}), 404
    return jsonify({'id': id}), 201

# Métodos para envíos

@app.route('/envios')
def envios():
    envios = Envio.get_all()  # Obtén todos los envíos

    # Depuración: Imprimir cada `envio` para verificar el valor de `id`
    for envio in envios:
        print(f"Envío ID: {envio.id}")  # Aquí verificamos si el id está presente

        origen = Ciudad.get_by_id(envio.origen_id)
        if origen:
            envio.origen_codigo = origen['codigo']
        else:
            envio.origen_codigo = "Desconocido"

        destino = Ciudad.get_by_id(envio.destino_id)
        if destino:
            envio.destino_codigo = destino['codigo']
        else:
            envio.destino_codigo = "Desconocido"

    return render_template('envios.html', envios=envios)

@app.route('/envio-registro', methods=['GET'])
def envio_registro():  
    envio = Envio(remitente='', destinatario='', origen_id='', destino_id='', fecha_envio='', numero_guia='', estado='')
    ciudades = Ciudad.get_all()  # Obtén todas las ciudades para pasarlas al formulario
    return render_template('envio.html', envio=envio, ciudades=ciudades)


@app.route('/envios', methods=['POST'])
def save_envio():
    data = request.form
    if not data.get('remitente') or not data.get('destinatario') or not data.get('origen_id') or not data.get('destino_id'):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400
    
    envio = Envio(
        origen_id=data['origen_id'],
        destino_id=data['destino_id'],
        remitente=data['remitente'],
        destinatario=data['destinatario'],
        fecha_envio=data['fecha_envio'],
        numero_guia=data['numero_guia'],
        estado=data['estado']
    )

    id = Envio.save(envio)
    if id:
        return redirect(url_for('envios'))
    else:
        return jsonify({'error': 'No se pudo crear el envío'}), 400


@app.route('/envio/<int:id>', methods=['GET'])
def get_envio(id):
    envio = Envio.get_by_id(id)
    if envio is None:
        return jsonify({'error': 'Envío no encontrado'}), 404
    return jsonify(envio), 200


@app.route('/envio/<int:id>', methods=['DELETE'])
def eliminar_envio(id):  # Cambié el nombre de la función
    result = Envio.delete(id)
    if result == 0:
        return jsonify({'error': 'El envío no existe'}), 404
    return jsonify({'message': 'Envío eliminado exitosamente'}), 200

@app.route('/envio/<int:id>/editar', methods=['GET', 'POST'])
def editar_envio(id):
    envio = Envio.get_by_id(id)
    if not envio:
        return jsonify({'error': 'Envío no encontrado'}), 404

    ciudades = Ciudad.get_all()

    if request.method == 'POST':
        # Obtener los datos del formulario
        data = request.form
        nuevo_numero_guia = data['numero_guia']
        
        # Verificar si el nuevo número de guía ya existe en otro envío
        envio_existente = Envio.query.filter_by(numero_guia=nuevo_numero_guia).first()
        if envio_existente and envio_existente.id != id:
            return render_template('envio.html', envio=envio, ciudades=ciudades, error="El número de guía ya está en uso")

        # Si no existe, actualizar el envío
        envio.origen_id = data['origen_id']
        envio.destino_id = data['destino_id']
        envio.remitente = data['remitente']
        envio.destinatario = data['destinatario']
        envio.fecha_envio = data['fecha_envio']
        envio.numero_guia = nuevo_numero_guia
        envio.estado = data['estado']

        rows_affected = Envio.update(id, envio)

        if rows_affected == 0:
            return jsonify({'error': 'No se pudo actualizar el envío'}), 400

        return redirect(url_for('envios')) 

    return render_template('envio.html', envio=envio, ciudades=ciudades)

@app.route('/costos.html')
def costos():
    return render_template('costos.html')

#Rutas para usuarios

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/registro', methods=['GET'])
def registro():
    ciudades=Ciudad.get_all()
    return render_template('registro.html', ciudades=ciudades)

@app.route('/registro', methods=['POST'])
def save_usuario():
    data = request.json
    ciudad=Ciudad.get_by_name(data['ciudad'])
    usuario = Usuario(nombre=data['nombre'], contrasenia=data['contrasenia'], ciudad_id=ciudad['id'])
    id = Usuario.save(usuario)
    return jsonify({'id': id}), 201


if __name__ == '__main__':
    app.run(debug=True)