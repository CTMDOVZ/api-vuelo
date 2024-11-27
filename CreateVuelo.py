import boto3
import json

def lambda_handler(event, context):
    # Obtener el cuerpo de la solicitud y manejar el caso donde no haya cuerpo
    body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido

    # Obtener los datos del vuelo desde el cuerpo de la solicitud
    id_vuelo = body.get('id_vuelo')
    id_aerolinea = body.get('id_aerolinea')
    codigo_vuelo = body.get('codigo_vuelo')
    origen = body.get('origen')
    destino = body.get('destino')
    fecha_salida = body.get('fecha_salida')
    fecha_llegada = body.get('fecha_llegada')
    capacidad = body.get('capacidad')

    # Conectar con DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_vuelo')  # Asegúrate de usar el nombre correcto de la tabla

    # Crear el ítem del vuelo
    vuelo = {
        'id_vuelo': id_vuelo,
        'id_aerolinea': id_aerolinea,
        'codigo_vuelo': codigo_vuelo,
        'origen': origen,
        'destino': destino,
        'fecha_salida': fecha_salida,
        'fecha_llegada': fecha_llegada,
        'capacidad': capacidad
    }

    # Guardar el ítem en DynamoDB
    response = table.put_item(Item=vuelo)

    # Retornar una respuesta exitosa
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Vuelo creado con éxito'})
    }
