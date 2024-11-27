import boto3
import json

def update_vuelo(event, context):
    # Obtener el cuerpo de la solicitud y manejar el caso donde no haya cuerpo
    body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido

    # Obtener el ID del vuelo y los atributos a actualizar
    id_vuelo = body.get('id_vuelo')
    atributos_actualizar = body.get('atributos')  # Diccionario con los atributos y valores a actualizar

    if not id_vuelo or not atributos_actualizar:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Faltan parámetros: id_vuelo o atributos'})
        }

    # Conectar con DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_vuelo')

    # Construir la expresión de actualización
    update_expression = "SET " + ", ".join([f"{k} = :{k}" for k in atributos_actualizar.keys()])
    expression_attribute_values = {f":{k}": v for k, v in atributos_actualizar.items()}

    # Actualizar el ítem
    response = table.update_item(
        Key={
            'id_vuelo': id_vuelo
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Vuelo con id_vuelo={id_vuelo} actualizado correctamente.'})
    }
