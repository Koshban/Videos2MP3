import pika
import json
import tempfile
import os
from bson.objectid import ObjectId
import moviepy.editor

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)  # Deserialize a JSON document to a Python Object 
    """ Empty Temp file to put splittted video files """
    tf = tempfile.NamedTemporaryFile()
    """" Video contents from GridFS"""
    out = fs_videos.get(ObjectId(message["video_fid"]))  # The file id of the mongoDB msg when the Video was uploaded there (In the Util module)

    """ Add Video contents to the empty tf file ( tf variable above )"""
    tf.write(out.read())

    """ Video to MP3 """
    audio = moviepy.editor.VideoFileClip(tf.name).audio  # tf.name is the path of the temp file
    tf.close()  # after closing tf will get deleted automatically

    """ Write Audio to file, named videofilename.mp3 """
    tf_path = tempfile.gettempdir() + f"/{message["video_fid"]}.mp3"
    audio.write_audiofile(tf_path)

    """ Save the audio file to MongoDB """
    with open(file=tf_path, mode="rb") as fw:
        data = fw.read()
        fid = fs_mp3s.put(data)  # Storing the file inot GridFS
    
    os.remove(tf_path)
    message["mp3_fid"] = str(fid)

    """ Put it onto the MQ on different Topic tha the incoming Video topic"""
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs_mp3s.delete(fid)  # if we cant put msg onto MQ, delete the mp3 uploaded to MongoDB, it will get retried from consumer.callback()
        return " Failed to Publish message"



