import os
import json
from recipe import Recipe
import recipe

import asyncio
from nicegui import ui

from material import Material

# Create Basic Materials:
water = Material(name="WATER", emoji="💧")
fire = Material(name="FIRE", emoji="🔥")
earth = Material(name="EARTH", emoji="🪱")
air = Material(name="AIR", emoji="💨")
dna = Material(name="DNA", emoji="🧬")

discovered_materials = [water, fire, earth, air, dna]
material_list = []

def updateDiscoveredMaterialsList(ui_list, crafting_area):
    ui_list.clear()
    for material in discovered_materials:
        with ui_list:
            with ui.item(on_click=lambda m=material: addToCrafingArea(m, crafting_area)):
                with ui.item_section():
                    ui.item_label(f"{material.emoji} {material.name}")

def removeFromCrafingArea(material, crafting_area, item):
    material_list.remove(material)
    crafting_area.remove(item)

def addToCrafingArea(material, crafting_area):
    if len(material_list) < 2:
        material_list.append(material)

        ui.notify(f"Added {material.emoji} {material.name} to the crafting area!")

        with crafting_area:
            item = ui.item()
            item.on_click(lambda: removeFromCrafingArea(material, crafting_area, item))
            with item:
                with ui.item_section():
                    ui.item_label(f"{material.emoji} {material.name}")


async def onCraftButtonClick(materials, spinner, ui_list, crafting_area):
    spinner.set_visibility(visible=True)
    await asyncio.sleep(0.1)  # Let the UI update to show the spinner
    await craft(materials)
    spinner.set_visibility(visible=False)
    updateDiscoveredMaterialsList(ui_list, crafting_area)

async def craft(materials):
    if len(materials) < 2:
        ui.notify("You need two materiuals to craft something!", type= 'warning')
        return
    
    input1_found = any(material.name == materials[0] for material in discovered_materials)
    input2_found = any(material.name == materials[1] for material in discovered_materials)

    if input1_found is False or input2_found is False:
        ui.notify("You haven't discovered some of these materials", type= 'warning')
        return

    with open(os.path.join(script_dir, filename), 'r') as file:
        data = json.load(file)
        recipies = [Recipe(r["material_list"], Material(**r["output"])) for r in data]


        foundRecipe = False
        for m_recipe in recipies:
            if materials[0] in m_recipe.material_list and materials[1] in m_recipe.material_list:
                if(m_recipe.output not in discovered_materials):
                    discovered_materials.append(m_recipe.output)
                    ui.notify(f"Added {m_recipe.output.emoji} {m_recipe.output.name} to discovered materials!")
                foundRecipe = True
                break
            
        if foundRecipe == False:
            new_material = recipe.createRecipe(materials[0], materials[1])
            ui.notify("Discovered new recipe!", type= 'positive')
            if(new_material not in discovered_materials):
                discovered_materials.append(new_material)
                ui.notify(f"Added {new_material.emoji} {new_material.name} to discovered materials!")



script_dir = os.path.dirname(__file__)
filename = "recipies.json"

with ui.row():
    with ui.column():
        crafting_area = ui.list().classes('bg-blue-100 rounded-lg shadow-md')

        with ui.row():
            spinner = ui.spinner(size='lg')
            spinner.set_visibility(visible=False)

            craft_button = ui.button('Craft')

    discoveredMaterials_list = ui.list().classes('bg-blue-100 rounded-lg shadow-md')
    updateDiscoveredMaterialsList(discoveredMaterials_list, crafting_area)

    @craft_button.on_click
    async def craft_button_click():

        materials = []

        for material in material_list:
            materials.append(material.name.strip().upper())

        await onCraftButtonClick(materials, spinner, discoveredMaterials_list,crafting_area)
  
ui.run()
