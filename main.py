#!/usr/bin/python3
import requests
import argparse
from bs4 import BeautifulSoup

# --- ARGUMENT PARSING ---
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)

def get_arguments():
    parser = argparse.ArgumentParser(description="COVID Statistic Selection", formatter_class=SmartFormatter)
    parser.add_argument("number", type=int, choices=range(0,1),
                    help="R|Statistic options:\n"
                        "0 -> NSW Total Daily Cases")
    return parser.parse_args()

# --- RETRIEVE STATISTICS ---
def retrieve_page():
    URL = "https://www.health.nsw.gov.au/Infectious/covid-19/Pages/stats-nsw.aspx"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def get_nsw_daily(soup):
    results = soup.find(id="case").find_all("span", class_="number")[0].text.strip()
    return results

# --- MAIN ---
def main():
    args = get_arguments()
    soup = retrieve_page()

    if args.number == 0:
        nsw_daily = get_nsw_daily(soup)
        print("Today NSW Daily: " + nsw_daily)
    else:
        # This should already be taken care of by argparse
        print("Invalid option")

if __name__ == "__main__":
    main()


