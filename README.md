# infinite-craft-gemini
This is an open-source project inspired by the game _Infinite Craft_ using Google's Gemini API.\
It is programmed in Python and uses the [NiceGUI](https://nicegui.io/) Python Library for the UI.

## Getting Started
In order to play, you need a Gemini API key. You can get one from [Google AI Studio](https://aistudio.google.com/).\
Once you have an API key, you can either set it as an enviroment variable on your local machine, or you can go into the `recipe.py` file and add your api key where it says `client = genai.Client()`
  * Ex: `client = genai.Client(api_key= 'GEMINI_API_KEY')`
<br />
Now you can run and play!

## Game Customization
Right now, the system prompt (found in the `recipe.py` file) is as follows:
```
'''Create a new material based on two given materials output your answer like:    
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
                ```, make sure that the materials created are common items, things, people, foods, places, buildings'''
```
You can edit this if you like!

## Showcase
[![SHOWCASE_VIDEO](https://img.youtube.com/vi/K45yoS99AYQ/0.jpg)](https://youtu.be/K45yoS99AYQ?si=3cyhoWllvxRIn7lz)
