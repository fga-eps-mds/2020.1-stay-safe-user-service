import os
import json
from controllers import neighborhood as controller


def print_progress_bar(iteration, total):
    """
    Call in a loop to create terminal progress bar
    """
    prefix = 'Progress'
    suffix = 'Complete'
    decimals = 1
    length = 50
    fill = '█'
    print_end = "\r"
    percent =\
        ("{0:." + str(decimals) + "f}").format(100 * (iteration/float(total)))
    filled_length = int(length * iteration // total)
    progress_bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{progress_bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


dir_ = os.path.dirname(__file__)
with open(dir_ + "/neighborhoods.json", "r") as read_file:
    data = json.load(read_file)

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json"
}

errors = []

len_neighborhoods = len(data['DF']) + len(data['SP'])
print_progress_bar(0, len_neighborhoods)

for state in ['DF', 'SP']:
    for i, neigh in enumerate(data[state]):
        r, code = controller.create_neighborhood(neigh)

        if code != 201:
            print(code)
            print(neigh['neighborhood'])
            print()
            errors.append(neigh)
        print_progress_bar(i+1, len_neighborhoods)
