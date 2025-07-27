from google import genai
from google.genai.types import GenerateContentConfig
import json
import os

from material import Material

class Recipe:
    def __init__(self, material_list, output):
        self.material_list = material_list
        self.output = output



def createRecipe(material_one, material_two):
    client = genai.Client()
    response = client.models.generate_content(
        model= "gemini-2.5-flash",
        config= GenerateContentConfig(
            system_instruction= '''Create a new material based on two given materials output your answer like:    
                {
                    "material_list" : ["FIRE", "EARTH"],
                    "output" : {
                        "name" : "VOLCANO,
                        "emoji" "🌋"
                    }
                },
                
                but make sure it has no extra words, only the curly braces and the contents, DO NOT WRITE IT LIKE:
                ```json
                {
                    "material_list" : ["FIRE", "EARTH"],
                    "output" : {
                        "name" : "VOLCANO,
                        "emoji" : "🌋"
                    }
                }
                ```,
                make sure that the materials created are common items, things, people, foods, places, buildings'''
        ),
        contents= f"material one is {material_one} and material two is {material_two}"
    )

    # print(response.text)
    material_json = json.loads(response.text)

    script_dir = os.path.dirname(__file__)
    filename = "recipies.json"

    with open(os.path.join(script_dir, filename), 'r') as file:
        data = json.load(file)
        data.append(material_json)

    with open(os.path.join(script_dir, filename), 'w') as file:
        json.dump(data, file, indent=4)

    output_material = Material(**material_json["output"])
    return Recipe(material_json["material_list"], output_material).output

