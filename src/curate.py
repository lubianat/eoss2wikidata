import pickle
from scrape import FundedProject
from pathlib import Path
from dictionaries.all import *
from wdcuration import add_key
import json

HERE = Path(__file__).parent.resolve()


def main():
    # A pickle object with the classes described in scrape.py
    with open(f"{HERE}/../results/projects.pickle", "rb") as handle:
        parsed_projects = pickle.load(handle)
    print(parsed_projects)
    for project in parsed_projects:
        for software in project.projects:
            if software not in dicts["software"]:
                try:
                    dicts["software"] = add_key(dicts["software"], software)
                    with open(f"{HERE}/dictionaries/software.json", "w+") as f:
                        f.write(json.dumps(dicts["software"], indent=4, sort_keys=True))

                except Exception:
                    pass


if __name__ == "__main__":
    main()
