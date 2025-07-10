# {
#     "input": {
#       "sentences": [
        
#       ]
#     }
#   }
  


from sklearn.datasets import fetch_20newsgroups
import json
newsgroups = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))
docs = newsgroups.data

with open('test_input.json', 'w') as f:
    json.dump({'input':{'sentences':docs[:100]}}, f)



