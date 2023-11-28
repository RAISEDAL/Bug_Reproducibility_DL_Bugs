import requests
import json
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

url = "https://api.stackexchange.com/2.3/questions/{id}?order=desc&sort=activity&site=stackoverflow&key=vc5m5jBpRA2Rw0HanS2XsA(("

with open('tags.json') as f:
    tags = json.load(f)

with open('critical_information.json') as f:
    critical_information = json.load(f)

with open('edit_actions.json') as f:
    edit_actions = json.load(f)

print ('Enter the question ID:')
id = input()

response = requests.get(url.format(id=id))

response_object = response.json()
question_tags = response_object['items'][0]['tags']

type_of_bug = '-'
tag_to_bug_type = {'model': 'model', 'training': 'training', 'api': 'data', 'tensor': 'tensor', 'gpu': 'gpu'}
exact_match_found = True

for tag in question_tags:
    for bug_type, bug_tags in tags.items():
        if tag in bug_tags:
            type_of_bug = tag_to_bug_type[bug_type]
            break

if type_of_bug == '-':
    exact_match_found = False
    tag_embeddings = {
        'model': model.encode(tags['model']),
        'training': model.encode(tags['training']),
        'api': model.encode(tags['api']),
        'tensor': model.encode(tags['tensor']),
        'gpu': model.encode(tags['gpu']),
    }
    scores = {tag: util.pytorch_cos_sim(model.encode(question_tags), embedding) for tag, embedding in tag_embeddings.items()}
    type_of_bug = max(scores, key=lambda x: scores[x].max())

if exact_match_found:
    print ('The type of bug is: ' + type_of_bug.capitalize())
else:
    print ('We cannot determine the exact type of bug, but based on tag analysis, the type of bug might be: ' + type_of_bug.capitalize())

print ('To reproduce the bug, the most critical information needed is:')
for info in critical_information[type_of_bug]:
    print (info)

print ('To reproduce the bug, we can use the following edit actions:')
for action in edit_actions[type_of_bug]:
    print (action)