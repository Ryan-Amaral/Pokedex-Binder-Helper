"""
Made some changes/improvements in this version, building off of chat-gpt's code.

1. Cache API results into a local file, not that important here, but didn't want to spam the API
with unnecessary traffic.
2. Fixed the total Pokemon count and gen 9 limit.
3. Made output less verbose per line by marking pages and generations separately, and made location
more clear.
4. Included whether the given page is a front or back.
5. Print rather than save to string as saving to a string wasn't necessary (though could be in 
another use-case).
6. Reset page count per generation (that's just my preference), with each generation starting on a
front page.
"""

import requests
import json
import os
import logging

POKEDEX_FILE_NAME = "pokedex.json"
POKEMON_API_BASE="https://pokeapi.co/api/v2/pokemon?limit="

# Function to fetch Pokemon data from an open API (i.e., PokeAPI) or cached file.
def fetch_pokemon_list(limit=1025):
    if os.path.isfile(POKEDEX_FILE_NAME):
        logging.info("Reading pokemon from saved file.")
        with open(POKEDEX_FILE_NAME, "r") as f:
            pokemon_json = json.load(f)
    else:
        logging.info("Downloading pokemon from API")
        url = f"{POKEMON_API_BASE}{limit}"
        response = requests.get(url)
        if response.status_code == 200:
            pokemon_json = response.json()
            with open(POKEDEX_FILE_NAME, "w") as f:
                json.dump(pokemon_json, f, indent=4)
        else:
            raise Exception('Failed to fetch data from PokeAPI')
    
    return [pokemon['name'].capitalize() for pokemon in pokemon_json['results']]

# Function to create the binder location list.
def generate_binder_guide(pokemon_list):
    generation_limits = [151, 100, 135, 107, 156, 72, 88, 96, 120]  # Number of Pokemon per generation
    pokemon_index = 0
    for gen, gen_limit in enumerate(generation_limits, start=0):  # Start at 0 for zero-based generation count
        generation_number = gen + 1  # Adjust to use 1-based display for generation
        page_number = 0
        isFront = True
        print(f"~~~~~~~~~~\nGeneration {generation_number}\n~~~~~~~~~~")
        for i in range(gen_limit):
            pocket_number = (i % 9) + 1
            if pocket_number == 1:
                page_number += 1
                if page_number == 1 or isFront == True:
                    front_back_text = "Front"
                else:
                    front_back_text = "Back"
                isFront = not isFront
                print(f"\nPage: {page_number} ({front_back_text})")
            pokemon_name = pokemon_list[pokemon_index]
            print(f"#{pokemon_index + 1:04} - {pokemon_name}: {pocket_number}")
            pokemon_index += 1
        print("")

# Main script
try:
    pokemon_list = fetch_pokemon_list()
    generate_binder_guide(pokemon_list)
except Exception as e:
    print(str(e))