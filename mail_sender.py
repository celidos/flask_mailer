import pika
from pika import PlainCredentials
from email.message import EmailMessage
import smtplib, ssl
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]
s.close()


def callback(ch, method, properties, body):
    context = ssl.create_default_context()
    msg = EmailMessage()
    msg.set_content("Please follow the link to confirm your email\nhttp://{ip}:5000/confirm/{email}/".format(
        ip=server_ip, email=body.decode('utf-8')))
    msg['Subject'] = 'Email confirmation'
    msg['From'] = "TETETESET@yandex.ru"
    msg['To'] = body.decode('utf-8')

    with smtplib.SMTP_SSL("smtp.yandex.ru", 465, context=context) as server:
        server.login("TETETESET@yandex.ru", 'BZ9EGA_vrTrf9Yg')
        server.send_message(msg)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672,
                                                               credentials=PlainCredentials('user', 'password')))
channel = connection.channel()

channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)
channel.start_consuming()