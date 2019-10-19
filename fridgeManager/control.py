from urllib.request import urlopen
import json
def get_recipes(ingredients):
    server_response = urlopen("https://api.edamam.com/search?q=%s&app_id=24223dfd&app_key=31ccabbde7b6150d99c98d500293a0b3"%("+".join(ingredients))).read()
    loaded_json = json.loads(server_response)
    dict_list = []
    for hit in loaded_json["hits"]:
        try:
            recipe = hit["recipe"]
            
            url = recipe["url"]
            image = recipe["image"]
            ingredients = recipe["ingredients"]
            label = recipe["label"]
            dict_list.append({"url":url,"image":image,"label":label,"ingredients":ingredients})
            
        except:
            continue
    return dict_list
