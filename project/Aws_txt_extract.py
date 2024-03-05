import boto3
client = boto3.client('comprehend',region_name='ap-south-1',aws_access_key_id='AKIAWPOXM4NEKQDMFWGL',aws_secret_access_key='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')
client

# Function to read text from a file
def read_text_from_file(transcribed_text):
    with open(transcribed_text, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Specify the path to your text file
file_path = 'transcribed_text.txt'

# Read text from the file
txt = read_text_from_file("transcribed_text.txt")

# Perform entity detection
response = client.detect_entities(Text=txt, LanguageCode='en')

# Output the response
# print(response)
response

import pandas as pd

pd.DataFrame(response['Entities'])

response = client.detect_pii_entities(Text=txt, LanguageCode='en')
pd.DataFrame(response['Entities'])

txt 

for entity in response['Entities']:
  entity_type = entity['Type']
  entity_value = txt[int(entity['BeginOffset']):int(entity['EndOffset'])]
  print(f"Entity Type: {entity_type} : {entity_value}")



