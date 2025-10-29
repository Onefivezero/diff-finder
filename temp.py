from diff_finder import DiffFinder
from pprint import pp

struct_a = {
    "same": "same",
    "different": "different-0",
    "nested_field": {
        "same_number": 1,
        "different_number": 10,
        "list_of_numbers": [1, 2, 3, 4],
    },
}
struct_b = {
    "same": "same",
    "different": "different-1",  # different-0 != different-1
    "nested_field": {
        "same_number": 1,
        "different_number": 5,  # 10 != 5
        "list_of_numbers": [1, 2, 10, 20],  # 3, 4 != 10, 20
    },
}

diffs = DiffFinder.find_diffs(struct_a, struct_b)
pp(diffs)
