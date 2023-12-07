import pika, json
#pika is a package that will help send events

params = pika.URLParameters('amqps://vkwwrzbc:OqyV963L6I5iK4VN0LFaIWNKV-4n4xnW@beaver.rmq.cloudamqp.com/vkwwrzbc')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    # convert the body to JSON before sending it.
    # routing_key is the queue that we want to send the event in
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)