import pika
import json

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except  Exception as err:
        return f"Internal Server Error : {err}" , 500
    else:  # This is the Python object created here
        message = {
            "video_fid": str(fid),
            "mp3_fid": None,
            "username": access["username"],
        }
    
    try:  # Publish to RabbitMQ
        channel.basic_publish(
            exchange="", 
            routing_key="video",
            body=json.dumps(message),  # json.dumps takes the Python object ( message) from above and converts it into a json formatted string
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ), # MQ and msgs will be durable so that the msgs not lost during a Pod crash
        )
    except Exception as err:
        fs.delete(fid)
        return f"Internal Server Error : {err}" , 500
