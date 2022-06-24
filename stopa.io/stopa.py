import time
from urllib.request import Request, urlopen

import html2text
import regex as re
from bs4 import BeautifulSoup

"""
Collate the complete collection of Stepan Parunshvili's essays.
"""

h = html2text.HTML2Text()
h.ignore_tables = True
h.escape_snob = False
h.mark_code = True

headers = { "User-Agent": "Mozilla/6.0" } # urllib user agent gets 403'd
number = 1

with open("posts.txt", "r") as posts:
    for post in posts:
        req = Request(post, headers=headers)
        try:
            with urlopen(req) as data:
                html = data.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")

                title = soup.head.title.string

                content = soup.find("div", class_="layout").div.div.div

                content.h1.a.replaceWithChildren()
                for img in soup.findAll("img", src=re.compile(r"^/api/")):
                    img['src'] = f"https://stopa.io{img['src']}"

                body = h.handle(str(content.span))

                with open(f"./articles/{number:03}_{title}.md", "wb+") as article:
                    article.write(f"# {title}\n".encode())

                    lines = body.split("\n")
                    for i in range(len(lines)):
                        match = re.match("(#+)(.+)$", lines[i])
                        if match:
                            lines[i] = f"{(1 + len(match.group(1))) * '#'}{match.group(2)}"

                    article.write("\n".join(lines).encode())

                print(f"- ✅ {number:03} {title}")

        except Exception as e:
            print(f"❌ {number:03} title, ({e})")

        number += 1
        time.sleep(0.05)
