import os
import json

# Directory containing the JSON files
directory = '/home/freo/Documents/python_venvs/speech_to_text/amazon/project/transcripts'

# Output transcript file
output_file = os.path.join(directory, 'transcript.txt')

# Iterate over the JSON files
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            data = json.load(file)
            transcripts = data['results']['transcripts']
            if transcripts:
                transcript_text = transcripts[0]['transcript']
                with open(output_file, 'a') as output:
                    output.write(transcript_text + '\n\n')
