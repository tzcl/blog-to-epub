import feedparser
import urllib.request
import time
import os.path
import html2text
import unidecode
import regex as re

"""
Download a collection of Paul Graham essays in EPUB & Markdown.
"""

rss = feedparser.parse("http://www.aaronsw.com/2002/feeds/pgessays.rss")
h = html2text.HTML2Text()
h.ignore_images = True
h.ignore_tables = True
h.escape_all = True
h.reference_links = True
h.mark_code = True

art_no = 1

for entry in reversed(rss.entries):
    url = entry['link']

    try:
        with urllib.request.urlopen(url) as website:
            content = website.read().decode("unicode-escape", "utf-8")
            parsed = h.handle(content)
            title = "_".join(entry['title'].split(
                " ")).lower()
            title = re.sub(r'[\W\s]+', '', title)
            with open(f"./essays/{art_no:03}_{title}.md", 'wb+') as file:
                file.write(f"# {art_no:03} {entry['title']}\n\n".encode())
                parsed = parsed.replace("[](index.html)  \n  \n", "")

                lines = parsed.split("\n")
                for i in range(len(lines)):
                    # Fix relative links
                    link = re.search(r"\[(.+)\]\(([^)]+)\)", lines[i])
                    if link and not link.group(2).startswith("http"):
                        lines[i] = lines[i].replace(link.group(0), f"[{link.group(1)}](http://paulgraham.com/{link.group(2)})")

                parsed = [(p.replace("\n", " ")
                          if re.match(r"^[\p{Z}\s]*(?:[^\p{Z}\s][\p{Z}\s]*){5,100}$", p)
                           else "\n"+p+"\n") for p in lines]
                
                file.write(" ".join(parsed).encode())
                print(f"- ✅ {art_no:03} {entry['title']}")

    except Exception as e:
        print(f"❌ {art_no:03} {entry['title']}, ({e})")

    art_no += 1
    time.sleep(0.05)  # half sec/article is ~2min, be nice with servers!
