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

script_dir = os.path.dirname(__file__)
filename = "recipes.json"

def initDiscoveredMaterials():
    with open(os.path.join(script_dir, filename), 'r') as file:
        data = json.load(file)
        recipes = [Recipe(r["material_list"], Material(**r["output"])) for r in data]

    # Init discovered materials
    for recipe in recipes:
        if recipe.output not in discovered_materials:
            discovered_materials.append(recipe.output)

def clearRecipes(ui_list, crafting_area):
    recipe.clearRecipes()
    discovered_materials.clear()
    discovered_materials.extend([water, fire, earth, air, dna])
    updateDiscoveredMaterialsList(ui_list, crafting_area)
    material_list.clear()
    crafting_area.clear()

def updateDiscoveredMaterialsList(ui_list, crafting_area):
    ui_list.clear()
    for material in discovered_materials:
        with ui_list:
            with ui.item(on_click=lambda m=material: addToCraftingArea(m, crafting_area)):
                with ui.item_section():
                    ui.item_label(f"{material.emoji} {material.name}")

def removeFromCraftingArea(material, crafting_area, item):
    material_list.remove(material)
    crafting_area.remove(item)

def addToCraftingArea(material, crafting_area):
    if len(material_list) < 2:
        material_list.append(material)

        ui.notify(f"Added {material.emoji} {material.name} to the crafting area!")

        with crafting_area:
            item = ui.item()
            item.on_click(lambda: removeFromCraftingArea(material, crafting_area, item))
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
    
    with open(os.path.join(script_dir, filename), 'r') as file:
        data = json.load(file)
        recipes = [Recipe(r["material_list"], Material(**r["output"])) for r in data]

    for m_recipe in recipes:
        if materials[0] in m_recipe.material_list and materials[1] in m_recipe.material_list:
            ui.notify(f"You already discovered {m_recipe.output.emoji} {m_recipe.output.name}!", type= 'warning')
            return
            

    new_material = recipe.createRecipe(materials[0], materials[1])
    discovered_materials.append(new_material)

    ui.notify("Discovered new recipe!", type= 'positive')
    ui.notify(f"Added {new_material.emoji} {new_material.name} to discovered materials!")


initDiscoveredMaterials()
ui.query('body').style('font-family: monospace;')

ui.header().classes('bg-transparent')
with ui.column().classes('w-full items-center'):
    ui.label("Open Source Alchemy 🧪").style('color: black; font-size: 200%').classes('justify-center ')


with ui.row().classes('justify-center w-full'):
    with ui.column().classes():
        crafting_area = ui.list().classes('bg-neutral-100 rounded-lg shadow-md')

        with ui.row():
            spinner = ui.spinner(size='lg')
            spinner.set_visibility(visible=False)

            craft_button = ui.button('🛠️', color= 'transparent').props('round').style('font-size: 150%')
            craft_button.tooltip('Craft')

    with ui.column().classes('items-center'):
        discoveredMaterials_list = ui.scroll_area().classes('bg-neutral-100 rounded-lg shadow-md max-h-96 min-w-[200px]')
        with ui.row():
            reset_button = ui.button('Reset 🔄️', color='transparent', on_click=lambda: clearRecipes(discoveredMaterials_list, crafting_area))
            reset_button.style('font-size: 115%').classes('rounded-lg')
            reset_button.tooltip('Reset discovered materials')
        
        
updateDiscoveredMaterialsList(discoveredMaterials_list, crafting_area)

@craft_button.on_click
async def craft_button_click():

    materials = []

    for material in material_list:
        materials.append(material.name.strip().upper())

    await onCraftButtonClick(materials, spinner, discoveredMaterials_list,crafting_area)
    material_list.clear()
    crafting_area.clear()
    
  
ui.run()
