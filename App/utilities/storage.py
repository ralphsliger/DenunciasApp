import datetime
import os
from os import listdir
from os.path import isfile, join 
import six
from flask import current_app
from google.oauth2 import service_account
from google.cloud import storage
import json



### Funcion que almacena las imagenes en google cloud

def upload_image_file(file, folder, content_id):
    if not file:
        return None
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/ralphsliger/DenunciasApp/App/denunciasapp-19-5e2bf659b239.json'
    file.format = 'png'
    date = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')
    filename = '{}-{}.{}'.format(content_id, date, 'png')
    
    #client = storage.Client(project=current_app.config['PROJECT_ID'])
    #bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    storage_client = storage.Client()
    bucket = list(storage_client.list_buckets())
    bucket = storage_client.get_bucket('denuncias-bucket')
    blob = bucket.blob(os.path.join(folder, filename))
    blob.upload_from_string(file.read(),
                           content_type=file.content_type)
    url = blob.public_url
    
    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')
    return url






