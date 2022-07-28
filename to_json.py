import pandas as pd
import ujson

data = pd.read_csv("middle_ware_old/middle_ware_data_separate_new.csv")
name = list(data["name"])
text = list(data["text"])
model = list(data["model"])

middle_ware_data_separate = {"name": name, "text": text, "model":model}

with open('middle_ware_data_separate.json', 'w') as fp:
    ujson.dump(middle_ware_data_separate, fp)
