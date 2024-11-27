import boto3

def delete_vuelo(event, context):
    # Obtener el ID del vuelo
    id_vuelo = event['id_vuelo']

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
        'body': f'Vuelo con id_vuelo={id_vuelo} eliminado correctamente.'
    }
