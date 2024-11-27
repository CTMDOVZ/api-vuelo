import boto3
import json

def delete_vuelo(event, context):
    # Obtener el cuerpo de la solicitud y manejar el caso donde no haya cuerpo
    body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido
    
    # Obtener el ID del vuelo desde el cuerpo de la solicitud
    id_vuelo = body.get('id_vuelo')

    # Conectar con DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_vuelo')

    # Eliminar el ítem
    response = table.delete_item(
        Key={
            'id_vuelo': id_vuelo
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Vuelo con id_vuelo={id_vuelo} eliminado correctamente.'})
    }
