import pika, json, os, django
#pika is a package that will help send events

os.environ.setdefault("DJANGO_SETTINGS_MODULE","admin.settings")
django.setup()

from products.models import Product

params = pika.URLParameters('amqps://vkwwrzbc:OqyV963L6I5iK4VN0LFaIWNKV-4n4xnW@beaver.rmq.cloudamqp.com/vkwwrzbc')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(chanl, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes+1
    product.save()
    print('Product likes increased!')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()
channel.close()