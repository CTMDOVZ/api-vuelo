import boto3
import json

def search_vuelo(event, context):
    # Obtener el cuerpo de la solicitud y manejar el caso donde no haya cuerpo
    body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido

    # Obtener el ID del vuelo desde el cuerpo de la solicitud
    id_vuelo = body.get('id_vuelo')

    if not id_vuelo:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Falta el parámetro id_vuelo'})
        }

    # Conectar con DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_vuelo')

    # Buscar el ítem
    response = table.get_item(
        Key={
            'id_vuelo': id_vuelo
        }
    )

    # Verificar si el ítem fue encontrado
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': f'Vuelo con id_vuelo={id_vuelo} no encontrado.'})
        }
