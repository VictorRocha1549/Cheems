from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash
from entities.ciudad import Ciudad
from entities.envio import Envio
from entities.usuario import Usuario
from entities.guia import Guia
app = Flask(__name__)

app.secret_key='Aqui se supone va una clave secreta, pero da igual, es un proyecto escolar'

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

@app.route('/ciudad/<int:id>', methods=['POST'])
def eliminar_ciudad(id):
    result = Ciudad.delete(id)
    if result == 0:
        # Puedes añadir un mensaje flash para notificar que la ciudad no existe.
        flash('La ciudad no existe o ya fue eliminada.', 'error')
    else:
        # Mensaje flash para notificar eliminación exitosa.
        flash('Ciudad eliminada exitosamente.', 'success')
    return redirect(url_for('ciudades'))

#Metodos para guia

@app.route('/guia')
def guia():
    guia = Guia.get_all() # Obtiene todos los datos de las guías (esto puede modificarse según tus necesidades)
    ciudades=[]
    for g in guia:
        ciudades.append(Ciudad.get_by_id(g['ciudad_id']))
    ciudades_dict = {c['id']: c['nombre'] for c in ciudades}
    for g in guia:
        g['ciudad_nombre'] = ciudades_dict.get(g['ciudad_id'], "Ciudad desconocida")
    usuario_id = session.get('usuario_id')  # Devuelve None si no existe
    usuario = Usuario.get_by_id(usuario_id) if usuario_id else None
    return render_template('guia.html', guia=guia, usuario=usuario)

    





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
    usuario=Usuario.get_by_id(session['usuario_id'])
    return render_template('envios.html', envios=envios, usuario=usuario)

@app.route('/envio-registro', methods=['GET'])
def envio_registro():  
    envio = Envio(remitente='', destinatario='', origen_id='', destino_id='', fecha_envio='', numero_guia='', estado='')
    ciudades = Ciudad.get_all()  # Obtén todas las ciudades para pasarlas al formulario
    usuario=Usuario.get_by_id(session['usuario_id'])
    return render_template('envio.html', envio=envio, ciudades=ciudades, usuario=usuario)


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


@app.route('/envio/<int:id>', methods=['POST'])
def eliminar_envio(id):
    result = Envio.delete(id)
    if result == 0:
        flash('El envío no existe o ya fue eliminado.', 'error')
    else:
        flash('Envío eliminado exitosamente.', 'success')

    return redirect(url_for('envios'))  # Redirigir a la página de envíos después de eliminar



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
    usuario=Usuario.get_by_id(session['usuario_id'])
    return render_template('envio.html', envio=envio, ciudades=ciudades, usuario=usuario)


@app.route('/crear_envio', methods=['POST', 'GET'])
def crear_envio():
    if request.method == 'POST':
        # Obtener los datos del formulario
        origen_id = request.form.get('origen_id')
        destino_id = request.form.get('destino_id')
        remitente = request.form.get('remitente')
        destinatario = request.form.get('destinatario')
        fecha_envio = request.form.get('fecha_envio')
        numero_guia = request.form.get('numero_guia')  # Número de guía proporcionado por el formulario

        # Si el número de guía no es proporcionado (vacío), generarlo automáticamente
        if not numero_guia:
            numero_guia = Envio.generar_numero_guia_unico()

        # Crear el objeto Envio
        nuevo_envio = Envio(
            origen_id=origen_id,
            destino_id=destino_id,
            remitente=remitente,
            destinatario=destinatario,
            fecha_envio=fecha_envio,
            numero_guia=numero_guia,
            estado="pendiente"
        )

        # Guardar el nuevo envío
        nuevo_envio.save()

        # Redirigir a la lista de envíos u otra página
        return redirect(url_for('envios'))

    # Si el método es GET, generar un número de guía único
    numero_guia = Envio.generar_numero_guia_unico()

    # Pasar el número de guía a la plantilla para el formulario
    return render_template('crear_envio.html', numero_guia=numero_guia)


@app.route('/costos.html')
def costos():
    usuario_id = session.get('usuario_id')  # Devuelve None si no existe
    usuario = Usuario.get_by_id(usuario_id) if usuario_id else None
    return render_template('costos.html', usuario=usuario)

#Rutas para usuarios

@app.route('/login', methods=['GET'])
def login():
    session.clear()
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

@app.route('/inicio', methods=['POST'])
def inicio_valido():
    data = request.json
    usuario=Usuario.get_by_name(data['nombre'])
    if not usuario or usuario['contrasenia'] != data['contrasenia']:
        return jsonify({'error': 'Usuario o contraseña incorrectos'}), 404

    session['usuario_id'] = usuario['id']
    return jsonify({'usuario': usuario['nombre']}), 201

@app.route('/inicio', methods=['GET'])
def inicio():
    usuario=Usuario.get_by_id(session['usuario_id'])
    return render_template('inicio.html', usuario=usuario)





if __name__ == '__main__':
    app.run(debug=True)