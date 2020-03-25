import os
import json
import pandas as pd
from tqdm import tqdm
import re
import matplotlib.pyplot as plt
from matplotlib import style

style.use("ggplot")

dirs = ["biorxiv_medrxiv"]

docs = []
for d in dirs:
    print(d)
    for file in tqdm(os.listdir(f"{d}/{d}")):

        file_path = f"{d}/{d}/{file}"
        j = json.load(open(file_path, "rb"))
        title = j['metadata']['title']

        try:
            abstract = j['abstract'][0]
        except:
            abstract = ""

        full_text = ""
        for text in j['body_text']:
            full_text += text['text'] + '\n\n'

        docs.append([title, abstract, full_text])

df = pd.DataFrame(docs, columns=['title', 'abstract', 'full_text'])

incubation = df[df['full_text'].str.contains('incubation')]

texts = incubation['full_text'].values
print(len(texts))

incubation_times = []

for t in texts:
    for sentence in t.split(". "):
        if "incubation" in sentence:
            print(sentence)
            single_day = re.findall(r" \d{1,2} day", sentence)

            if len(single_day) == 1:
                num = single_day[0].split(" ")
                incubation_times.append(float(num[1]))

print(incubation_times)
print(len(incubation_times))

plt.hist(incubation_times, bins=10)
plt.ylabel("bin counts")
plt.xlabel("incubations time (days)")
plt.show()

