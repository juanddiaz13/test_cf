import os
import base64
import json
from googleapiclient import discovery

APP_NAME = os.getenv('GCP_PROJECT')
#APP_NAME2 = os.getenv('GCP_PROJECT2'

#projects = ($(gcloud projects list))

def disable_use_appengine(data,context):
  pubsub_data = base64.b64decode(data['data']).decode('utf-8')
  pubsub_json = json.loads(pubsub_data)
  message = pubsub_json['message']

  if message == 'enable':
    print (f'No action necessary. (message: {message})')
    return (message)

  appengine = discovery.build(
    'appengine',
    'v1',
    cache_discovery=False
  )
  apps = appengine.apps()

  # Get the target app's serving status for the APP_NAME
  target_app = apps.get(appsId=APP_NAME).execute()
  current_status = target_app['servingStatus']

  # Get the target app's serving status for the APP_NAME
  #target_app = apps.get(appsId=APP_NAME2).execute()
  #current_status2 = target_app['servingStatus']
  
  # Disable target app, if necessary
  if current_status == 'SERVING':
      print(f'Attempting to disable app {APP_NAME}...')
      body = {'servingStatus': 'USER_DISABLED'}
      apps.patch(appsId=APP_NAME, updateMask='serving_status', body=body).execute()

  # Disable the app2  engine in the other project
  #if current_status2 == 'SERVING':
  #    print(f'Attempting to disable app {APP_NAME}...')
  #    body = {'servingStatus': 'USER_DISABLED'}
  #    apps.patch(appsId=APP_NAME2, updateMask='serving_status', body=body).execute()