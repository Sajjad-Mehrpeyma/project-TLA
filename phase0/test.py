from FA_class import *
import os

if __name__ == '__main__':
    
    test_directory = r".\data\module2Test"
    json_fa_file = r"json_fa.json"
    with open(os.path.join(test_directory, json_fa_file), 'r') as file:
        json_fa = file.read()

    dfa = DFA.deserialize_json(json_fa)
    nfa = NFA.convert_DFA_instance_to_NFA_instance(dfa)
    print(nfa.serialize_to_json())
    print(dfa.serialize_json())