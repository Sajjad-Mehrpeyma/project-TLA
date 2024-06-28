import sys
sys.path.append(r'..\project-template')
from utils.utils import imageType
from phase0.FA_class import DFA
from phase2 import module2


def solve(json_fa_list: list[str], images: list[imageType]) -> list[int]:
    res: list[int] = [0 for _ in range(len(images))]
    max_sim = [0 for _ in range(len(images))]
    for i, image in enumerate(images):
        for j, json_fa in enumerate(json_fa_list):
            similarity = module2.solve(json_fa, image)[1]
            if similarity > max_sim[i]:
                max_sim[i] = similarity
                res[i] = j
    return res

if __name__ == "__main__":
    ...
