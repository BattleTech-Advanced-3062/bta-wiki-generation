import os
import sys
import json
from pprint import pp
import genUtilities
from settings import *

def process_pilot_files(directories):
    pilot_dict = {}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.startswith("pilot_") and file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if data.get("IsRonin", False):
                            pilot_entry = parse_pilot_json(file_path)
                            pilot_dict.update(pilot_entry)

    return pilot_dict

def parse_pilot_json(file_path):
    ability_mapping = {
        "AbilityDefG5": "multitarget",
        "AbilityDefG5a": "battlelord",
        "AbilityDefG8": "precisionmaster",
        "AbilityDefG8b": "ballisticmaster",
        "AbilityDefG8a": "energymaster",
        "AbilityDefG8c": "missilemaster",
        "AbilityDefG10a": "stonecold",
        "AbilityDefP5": "surefooting",
        "AbilityDefP5a": "phantom",
        "AbilityDefP10": "acepilot",
        "AbilityDefP8a": "sprinter",
        "AbilityDefGu5": "bulwark",
        "AbilityDefGu5a": "shieldedstance",
        "AbilityDefGu8": "juggernaut",
        "AbilityDefGu8a": "brawler",
        "AbilityDefGu10a": "defensiveformation",
        "AbilityDefT5A": "sensorlock",
        "AbilityDefT5Aa": "targetprediction",
        "AbilityDefT8A": "mastertactician",
        "AbilityDefT8Aa": "knifefighter",
        "AbilityDefT10Aa": "eagleeye",
        "AbilityDefG5T": "intensifyfirepower",
        "AbilityDefG8T": "perfecttargeting",
        "AbilityDefG10T": "overwhelmingaggression",
        "AbilityDefP5T": "sideslip",
        "AbilityDefGu8T": "streetracer",
        "AbilityDefP10T": "spotter",
        "AbilityDefGu5T": "redundantcomponents",
        "AbilityDefP8T": "bruteforce",
        "AbilityDefGu10T": "hulldown",
        "AbilityDefT8T": "sensorsweep",
        "AbilityDefT5T": "targetpainting",
        "AbilityDefT10T": "commandandcontrol"
    }

    excluded_pilot_tags = {
        "pilot_kurita",
        "pilot_liao",
        "pilot_davion",
        "pilot_marik",
        "pilot_steiner",
        "pilot_backer",
        "pilot_periphery",
        "pilot_magistracy",
        "pilot_taurian",
        "pilot_comstar",
        "pilot_vehicle_crew",
        "pilot_mechwarrior"
    }

    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract the Description.Callsign as the key
    callsign = data.get("Description", {}).get("Callsign", "Unknown")

    # Map the required fields to their respective values
    pilot_details = {
        "callsign": data.get("Description", {}).get("Callsign"),
        "firstname": data.get("Description", {}).get("FirstName"),
        "lastname": data.get("Description", {}).get("LastName"),
        "age": data.get("Description", {}).get("Age"),
        "gender": data.get("Description", {}).get("Gender"),
        "faction": data.get("Description", {}).get("Faction"),
        "biography": data.get("Description", {}).get("Details"),
        "health": data.get("Health"),
        "gunnery": data.get("BaseGunnery"),
        "piloting": data.get("BasePiloting"),
        "guts": data.get("BaseGuts"),
        "tactics": data.get("BaseTactics"),
    }

    # Check for abilities and add them to pilot details
    ability_def_names = data.get("abilityDefNames", [])
    for ability in ability_def_names:
        if ability in ability_mapping:
            pilot_details[ability_mapping[ability]] = ability_mapping[ability]
    
    # Process pilot tags
    pilot_tags = data.get("PilotTags", {}).get("items", [])
    tag_counter = 1
    for tag in pilot_tags:
        if tag.startswith("pilot_") and tag not in excluded_pilot_tags:
            formatted_tag = tag.replace("pilot_", "").capitalize()
            pilot_details[f"pilottag{tag_counter}"] = formatted_tag
            tag_counter += 1

    return {callsign: pilot_details}

if __name__ == "__main__":
    result = process_pilot_files(pilot_dir_list)
    #result = parse_pilot_json(sys.argv[1])
    pp(result)

