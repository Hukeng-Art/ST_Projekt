import os
import regex as re
import json

texts = os.listdir('raw_data')

for text in texts:
    with open(f'raw_data/{text}') as f:
        contents = f.read()

        contents_dict = json.loads(contents)

        contents_dict['text'] = re.sub('<.*?>', '', contents_dict['text'])

        with open(f'cleaned/{text}', 'w') as output:
            output.write(json.dumps(contents_dict, indent=4))