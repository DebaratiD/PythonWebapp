import pika, json
#pika is a package that will help send events
from main import Product, db

params = pika.URLParameters('amqps://vkwwrzbc:OqyV963L6I5iK4VN0LFaIWNKV-4n4xnW@beaver.rmq.cloudamqp.com/vkwwrzbc')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(chanl, method, properties, body):
    print('Received in admin')
    # convert data back to original form from JSON
    data = json.loads(body)
    print(data)

    # Object created in django app is added to sql db using flask app
    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image = data['image'])
        db.session.add(product)
        db.session.commit()

    elif properties.content_type=='product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()

    elif properties.content_type=='product_deleted':
        # Here data itself is the id, so no need to refer as data['id']
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()
channel.close()