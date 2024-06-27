import json
class State:
    __counter = 0

    def __init__(self, id: None) -> None:
        if id is None:
            self.id = State._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, 'State'] = {}

    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class DFA:

    def __init__(self) -> None:
        self.state_ids: dict[int, 'State'] = {}
        self.init_state = None
        self.states: list['State'] = []
        self.alphabet: set['str'] = {}
        # self.initial_states: list['State'] = []
        self.final_states: set['State'] = set()

    @staticmethod
    def deserialize_json(json_str: str) -> 'DFA':
        fa = DFA()
        json_fa = json.loads(json_str)

        fa.alphabet = set(json_fa["alphabet"])

        for state_str in json_fa["states"]:
            fa.add_state(int(state_str[2:]))

        fa.init_state = fa.get_state_by_id(int(json_fa["initial_state"][2:]))

        for final_str in json_fa["final_states"]:
            fa.add_final_state(fa.get_state_by_id(int(final_str[2:])))

        for state_str in json_fa["states"]:
            for symbol in fa.alphabet:
                fa.add_transition(fa.get_state_by_id(int(state_str[2:])), fa.get_state_by_id(int(json_fa[state_str][symbol][2:])),
                                  symbol)

        return fa

    def serialize_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", list(self.final_states))),
            "alphabet": list(self.alphabet)
        }

        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                fa[f"q_{state.id}"][symbol] = f"q_{state.transitions[symbol].id}"

        return json.dumps(fa)

    def add_state(self, id: int | None = None) -> State:
        new_state = State(id if id else None)
        self.states.append(new_state)
        self.state_ids[new_state.id] = new_state
        return new_state

    def add_transition(self, from_state: State, to_state: State, input_symbol: str) -> None:
        from_state.add_transition(input_symbol, to_state)

    # def assign_initial_state(self, state: State) -> None:
    #     self.initial_states.add(state)
        

    def add_final_state(self, state: State) -> None:
        self.final_states.add(state)

    def get_state_by_id(self, id) -> State | None:
        return self.state_ids[id]

    def is_final(self, state: State) -> bool:
        return state in self.final_states



class NFAState:
    __counter = 0

    def __init__(self, id: None) -> None:
        if id is None:
            self.id = State._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, 'State'] = {}

    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class NFA:
    def __init__(self) -> None:
        self.init_state: 'NFAState' = None
        self.states: list['NFAState'] = []
        self.alphabet: set['str'] = []
        # self.final_states: list['State'] = []
        self.final_states: set['NFAState'] = []
        self.state_ids: dict[int, 'NFAState'] = {}

    @staticmethod
    def convert_DFA_instance_to_NFA_instance(dfa_machine: 'DFA') -> 'NFA':
        nfa = NFA()
        nfa.alphabet = dfa_machine.alphabet.union('λ')
        
        for id in dfa_machine.state_ids.keys():
            nfa.add_state(id)

        nfa.init_state = nfa.state_ids[dfa_machine.init_state.id]
        nfa.final_states = [nfa.state_ids[state.id] for state in dfa_machine.final_states]
        for state in dfa_machine.states:
            for key in state.transitions.keys():
                to_state = state.transitions[key]
                nfa.state_ids[state.id].add_transition(key, nfa.state_ids[to_state.id])
        return nfa
    
    @staticmethod
    def union(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        machine1.alphabet = machine1.alphabet.union(machine2.alphabet)
        offset = len(machine1.state_ids)
        for id in machine2.state_ids.keys():
            machine1.state_ids[id + offset] = machine2.state_ids[id]
            machine2.state_ids[id].id += offset
        machine1.init_state.add_transition('λ', machine2.init_state)
        return machine1

    @staticmethod
    def concat(machine1: 'NFA', machine2: 'NFA') -> 'NFA':

        machine1.alphabet = machine1.alphabet.union(machine2.alphabet)
        offset = len(machine1.state_ids)

        for id in machine2.state_ids.keys():
            machine1.state_ids[id + offset] = machine2.state_ids[id]
            machine2.state_ids[id].id += offset

        for state in machine1.final_states:
            state.add_transition('λ', machine2.init_state)

        machine1.final_states = machine2.final_states
        return machine1
    
    @staticmethod
    def star(machine: 'NFA') -> 'NFA':
        machine.final_states.add(machine.init_state)
        for state in machine.final_states:
            state.add_transition('λ',machine.init_state)

    def add_state(self, id: int) -> NFAState:
        new_state = NFAState(id)
        self.states.append(new_state)
        self.state_ids[new_state.id] = new_state
        return new_state
    
    def serialize_to_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", list(self.final_states))),
            "alphabet": list(self.alphabet)
        }

        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                if symbol in state.transitions:
                    fa[f"q_{state.id}"][symbol] = f"q_{state.transitions[symbol].id}"

        return json.dumps(fa)
