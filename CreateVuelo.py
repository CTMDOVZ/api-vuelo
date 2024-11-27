import boto3
import json

def lambda_handler(event, context):
    try:
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

        # Validar que todos los campos requeridos están presentes
        if not all([id_vuelo, id_aerolinea, codigo_vuelo, origen, destino, fecha_salida, fecha_llegada, capacidad]):
            raise ValueError("Faltan parámetros: id_vuelo, id_aerolinea, codigo_vuelo, origen, destino, fecha_salida, fecha_llegada o capacidad")

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

    except ValueError as ve:
        # Capturar errores de validación si faltan parámetros
        print(f"Error de validación: {str(ve)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(ve)})
        }

    except boto3.exceptions.S3UploadFailedError as db_err:
        # Error relacionado con DynamoDB o problemas con la conexión
        print(f"Error de DynamoDB: {str(db_err)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error al interactuar con DynamoDB', 'details': str(db_err)})
        }

    except json.JSONDecodeError as json_err:
        # Error al procesar el JSON en el cuerpo de la solicitud
        print(f"Error al procesar JSON: {str(json_err)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Error al procesar los datos JSON', 'details': str(json_err)})
        }

    except Exception as e:
        # Capturar cualquier otro tipo de error no esperado
        print(f"Error desconocido: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
