# From https://colab.research.google.com/github/nestauk/im-tutorials/blob/3-ysi-tutorial/notebooks/Web-Scraping/Web%20Scraping%20Tutorial.ipynb#scrollTo=knTVDbU7JeAC

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pickle
from dataclasses import dataclass, field
from pathlib import Path
from selenium import webdriver

HERE = Path(__file__).parent.resolve()


@dataclass
class FundedProject:
    """Class for keeping track of each CZI funded projects."""

    href: str = ""
    projects: list = field(default_factory=list)
    leads: list = field(default_factory=list)
    cycle: str = ""


def main():
    url = "https://chanzuckerberg.com/eoss/proposals/"

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    driver.close()

    projects = soup.find_all(("a", {"class": "list__row is-active"}), href=True)

    def clean_up(string):
        return [txt.strip().replace("and ", "") for txt in string.text.split(",")]

    parsed_projects = []
    for proj in projects:
        if proj.has_attr("data-cycle"):
            project_now = FundedProject()
            project_now.href = proj.get("href")
            labels = proj.find_all("span")
            for j, label in enumerate(labels):
                if "Project" in labels[j - 1].text:
                    project_now.projects = clean_up(labels[j])
                if "Lead" in labels[j - 1].text:
                    project_now.leads = clean_up(labels[j])
                if "Cycle" in labels[j - 1].text:
                    project_now.cycle = clean_up(labels[j])
            parsed_projects.append(project_now)

    print(parsed_projects)
    with open(f"{HERE}/../results/projects.pickle", "wb") as handle:
        pickle.dump(parsed_projects, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
