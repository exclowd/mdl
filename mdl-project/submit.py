from urllib.request import urlopen

import numpy as np
from bs4 import BeautifulSoup

from request import submit
from save import get_from_id

np.set_printoptions(linewidth=np.inf)

url = 'http://10.4.21.156/getusage'


def get_score(vec):
    submit(vec)
    HTML = urlopen(url).read()

    soup = BeautifulSoup(HTML, 'html.parser')

    # the first argument to find tells it what tag to search for
    # the second you can pass a dict of attr->value pairs to filter
    # results that match the first tag
    table = soup.find("table")

    score = np.inf
    rows = []
    for row in table.findAll("tr"):
        rows.append(row)
        cols = row.findAll('td')
        if len(cols) > 0:
            if cols[1].text == 'Drowning in Inefficiency':
                score = float(cols[0].text)

    return score


if __name__ == '__main__':
    IDS = [
        4038,
        4040,
        4117,
        3964,
        3981,
        4069,
        3885,
        3984,
        3775,
        3871,
    ]
    # IDS = sorted(IDS)
    for ID in IDS:
        a, error = get_from_id(ID)

        print(ID, list(a))
        score = get_score(a)
        # print(ID, "Got score:", score)
        with open('temp.txt', 'a') as f:
            f.write(f"{score}:{ID}:{error}:{error[1] / error[0]}:{a}\n")

        with open('ranking.txt', 'a') as f:
            f.write(f"{ID} {score}\n")
