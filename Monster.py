import json

class Monster:
	def __init__(self,monster_dict,type="monster_maker_custom"):
		if type=="monster_maker_custom":
			self.monster_from_MM_custom_json(monster_dict)

	def monster_from_MM_custom_json(self,monster_dict):
		monster=monster_dict.copy()
		self.name=monster["description"]["name"]
		self.size=monster["description"]["size"]
		self.monster_type=monster["description"]["type"]
		self.alignment=monster["description"]["alignment"]
		self.hp=f"{monster['hp']['average']} ({monster['hp']['roll']})"
		self.challenge=monster["challenge"]["rating"]

		#how do I get this?
		self.proficiency=1

		#get AC from base+mod then make a string with the AC type
		if monster["ac"]["modifier"]==None:
			self.ac=0.0
		else:
			self.ac=float(monster["ac"]["modifier"])
		self.ac=monster["ac"]["base"]+self.ac
		self.ac=f"{self.ac} ({monster['ac']['type']})"


		#speed and senses are dictionaries of type:distance
		#so we combine to a comma separated list of type and distance
		self.speed=monster["speed"]
		self.speed=", ".join([f"{x.capitalize()} {y}" for x,y in self.speed.items()])

		self.senses=monster["senses"]
		self.senses=", ".join([f"{x.capitalize()} {y}" for x,y in self.senses.items() if y is not None])

		#similar for languages
		self.languages=", ".join([x["name"].capitalize() for x in monster["languages"]])

		#abilities is a dictionary, may as well keep it but get rid of quickstart 
		monster["abilities"].pop("quickstart",None)
		self.abilities=monster["abilities"]

		#Saving throws are broken.
		self.savingThrows=""

		#Skills is a list of dictionaries but we want a single string with modifiers
		self.skills=[]
		for skill in monster["skills"]:
			skill_name=skill["name"].capitalize()
			skill_mod=self.abilities[skill["custom"]["ability"]]+self.proficiency
			self.skills.append(f"{skill_name} +{skill_mod}")
		self.skills=", ".join(self.skills)

		#Just want a comma separated string of types from what is a rather complex list of dictionaries.
		self.damageResistances=", ".join([f"{x['type'].capitalize()}" for x in monster["resistances"]])
		self.damageImmunities=", ".join([f"{x['type'].capitalize()}" for x in monster["immunities"]])
		self.vulnerabilities=", ".join([f"{x['type'].capitalize()}" for x in monster["vulnerabilities"]])
		self.conditionImmunities=", ".join([f"{x['type'].capitalize()}" for x in monster["conditions"]])

		#traits in both formats are a list of dictionaries with name and description as keys
		#however description has a different name in each format so loop to rename
		self.traits=monster["traits"]
		for i in range(len(self.traits)):
			trait=self.traits[i]
			trait["text"]=trait.pop("detail","")
			self. traits[i]=trait
		
		#Same deal for actions
		self.actions=monster["actions"]
		for i in range(len(self.actions)):
			action=self.actions[i]
			action["text"]=action.pop("detail","")
			self.actions[i]=action
			
		#and reactions
		self.reactions=monster["reactions"]
		for i in range(len(self.reactions)):
			action=self.reactions[i]
			action["text"]=action.pop("detail","")
			self.reactions[i]=action
			
		# finally legendary actions
		# MM has no concept of cost so it will just be in the detail
		self.legendaryActions=monster["legendaryActions"]
		for i in range(len(self.legendaryActions)):
			action=self.legendaryActions[i]
			action["text"]=action.pop("detail","")
			self.legendaryActions[i]=action
			
		self.legendaryPoints=monster['legendaryActionsPerRound']

	def to_r20_json(self,output_file):
		out_dict=vars(self)
		out_dict["type"]=out_dict.pop("monster_type","")

		for key in ["hp","ac"]:
		    out_dict[key.upper()]=out_dict.pop(key,"")
		    
		ability_keys=list(out_dict["abilities"].keys())
		for i,key in enumerate(['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']):
		    out_dict[key]=out_dict["abilities"][ability_keys[i]]
		deleted=out_dict.pop("abilities","")

		output_file=open(output_file,"w")
		json.dump(out_dict,output_file)
		output_file.close()
