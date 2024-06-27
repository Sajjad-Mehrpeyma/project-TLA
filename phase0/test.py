from FA_class import *
import os
test_directory = r"../data/module2Test"
json_fa_file = r"json_fa.json"
with open(os.path.join(test_directory, json_fa_file), 'r') as file:
    json_fa = file.read()

dfa = DFA.deserialize_json(json_fa)

print(dfa.serialize_json())