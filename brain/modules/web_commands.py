"""
=========================================================
Project G-EXO
Web Commands Module
Version : 0.9
Developer : Thatikonda Goutham Teja
=========================================================
"""

import urllib.parse
import webbrowser

from logger import log


WEBSITES = {
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "gmail": "https://mail.google.com",
    "google": "https://www.google.com",
    "linkedin": "https://www.linkedin.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "x": "https://x.com",
    "twitter": "https://x.com",
}


def execute(command):

    command = command.lower().strip()

    # ----------------------------------------
    # OPEN WEBSITE
    # ----------------------------------------

    if command.startswith("open "):

        site = command.replace("open ", "", 1)

        if site in WEBSITES:

            print(f"\nOpening {site.title()}...\n")

            log(f"Website Opened : {site}")

            webbrowser.open(WEBSITES[site])

            return True

    # ----------------------------------------
    # GOOGLE SEARCH
    # ----------------------------------------

    elif command.startswith("search "):

        query = command.replace("search ", "", 1)

        url = (
            "https://www.google.com/search?q="
            + urllib.parse.quote(query)
        )

        print(f"\nSearching Google for: {query}\n")

        log(f"Google Search : {query}")

        webbrowser.open(url)

        return True

    return None