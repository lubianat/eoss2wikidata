import pickle
from scrape import FundedProject
from pathlib import Path
from dictionaries.all import *
from wdcuration import add_key
import json
from time import gmtime, strftime

HERE = Path(__file__).parent.resolve()
RESULTS = HERE.parent.joinpath("results").resolve()


def main():
    with open(f"{HERE}/../results/projects.pickle", "rb") as handle:
        parsed_projects = pickle.load(handle)
    print(parsed_projects)
    statements = ""
    for project in parsed_projects:
        for software in project.projects:
            s = dicts["software"][software]
            p = "|P8324|"
            o = "Q21623039"
            qp1 = "|P6195|"
            qo1 = "Q113788223"
            rp1 = "|S854|"
            ro1 = '"' + "https://chanzuckerberg.com/eoss/proposals/" + '"'
            rp2 = "|S813|"
            ro2 = strftime("+%Y-%m-%dT00:00:00Z/11", gmtime())

            statements += s + p + o + qp1 + qo1 + rp1 + ro1 + rp2 + ro2 + "\n"

    RESULTS.joinpath("funding.qs").write_text(statements, encoding="UTF-8")


if __name__ == "__main__":
    main()
