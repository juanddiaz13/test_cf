import os
import base64
import json
from googleapiclient import discovery
from google.cloud import resourcemanager_v3

#Bring the env variables that contains the project ID where are the apps 
APP_NAME = os.getenv('GCP_PROJECT') 
#APP_NAME2 = os.getenv('GCP_PROJECT2')

def enable_use_appengine(data,context):
  client = resourcemanager_v3.ProjectsClient()
  request = resourcemanager_v3.ListProjectsRequest(parent="organizations/795761523920",)
  page_result = client.list_projects(request=request)
  for response in page_result:
    print(response)
  pubsub_data = base64.b64decode(data['data']).decode('utf-8')
  pubsub_json = json.loads(pubsub_data)
  message = pubsub_json['message']

  if message == 'disable':
    print (f'No action necessary. (message: {message})')
    return (message)

  appengine = discovery.build(
    'appengine',
    'v1',
    cache_discovery=False
  )
  apps = appengine.apps()

  # Get the target app's serving status
  target_app = apps.get(appsId=APP_NAME).execute()
  current_status = target_app['servingStatus']

  # Get the target app's serving status
  #target_app = apps.get(appsId=APP_NAME2).execute()
  #current_status2 = target_app['servingStatus']

  # Enable target app, if necessary
  if current_status == 'USER_DISABLED':
    print(f'Attempting to enable app {APP_NAME}...')
    body = {'servingStatus': 'SERVING'}
    apps.patch(appsId=APP_NAME, updateMask='serving_status', body=body).execute()

  # Enable target app in the other project, if necessary
  #if current_status2 == 'USER_DISABLED':
  #  print(f'Attempting to enable app {APP_NAME}...')
  #  body = {'servingStatus': 'SERVING'}
  #  apps.patch(appsId=APP_NAME2, updateMask='serving_status', body=body).execute()
