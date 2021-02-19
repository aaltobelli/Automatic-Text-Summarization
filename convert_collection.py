import json
import glob
import string

doc_url = "/Users/aldo/Desktop/Dev/Python/BBC News Summary/"



doc_collection = []
categories = ["business", "entertainment", "politics", "sport", "tech"]
i = 0
for category in categories:
    url = doc_url+"News Articles/"+category+"/*.txt"
    summ_url = doc_url+"Summaries/"+category+"/*.txt"
    file_list = glob.glob(url)
    for file_path in file_list:
        with open(file_path, 'r', encoding='ISO-8859-1') as file_input:
            id = file_path[-7:-4]
            full_text = file_input.read()
        with open(summ_url.replace("*", id)) as summ_input:
            summary = summ_input.read()
        data = {
            "id": i,
            "category": category,
            "full_text": full_text,
            "summary": summary
        }

        doc_collection.append(data)
        i += 1

with open('test.json', 'w') as fout:
    json.dump(doc_collection , fout)

#print(doc_collection[2000]["summary"])
