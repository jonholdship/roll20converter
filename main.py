import Monster
import json


#this is a MM output json for a single monster
input_file="test_data/complex_monster_MM_custom.json"
#currently we can only do custom monsters not quickstarts
input_type="custom"

output_file="roll20_test.json"



monster=open(input_file)
monster=json.load(monster)
monster=monster["blueprint"]

monster=Monster.Monster(monster)

r20_json=monster.to_r20_json(output_file)
