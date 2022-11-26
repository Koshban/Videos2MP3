import pika
import sys
import os
import time
from pymongo import MongoClient
import gridfs
from convert import to_mp3

def main():
    client = MongoClient("host.minikube.internal", 27017)  # MongoDB is on Local Host, so use minikube.internal to resolve
    """ Create the MongoDB Databases"""
    db_videos = client.videos
    db_mp3s = client.mp3s
    """ Create the GridFS to slice files bigger than max size"""
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)
    """ RabbitMQ Connections """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))  # Use the MQs service Name i.e. rabbitmq to resolve to """"
    """ Host IP thru ServiceName """
    channel = connection.channel()
    """ Callback func to get executed whenever a msg is consumed from the MQ """
    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            """ if error, Negetive acknowledgement will not ack the msg and hence the msg wont be removed from the MQ"""
            ch.basic_nack(delivery_tag=method.delivery_tag)  # delivery_tag uniquely identifies each msg, so MQ will kow whcih msg had not been acked yet
        else:  # if no error
            ch.basic_ack(delivery_tag=method.delivery_tag)   # Ack which msg consumed + processed , so that it can be removed from the MQ


    """ Consume msgs from the MQ """
    channel.basic_consume(queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback)
    print("Waiting for message. To EXIT press CTRL + C")
    channel.start_consuming()

    if __name__ == '__main__':
        try:
            main()
        except KeyboardInterrupt:  # when ctrl + c is pressed by user
            print("Interrupted, Exiting Now")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)  # Graceful shutdown of the service in case of ctrl + C

    
