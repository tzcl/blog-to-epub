import regex as re

# index.html can be retrieved manually by scrolling through stopa.io until all
# posts are loaded and then saving the <html> element in Chrome devtools

base_url = "https://stopa.io"
pattern = re.compile(r"(/post/\d{1,3}).json")
posts = []

with open("index.html", "r") as index:
    for line in index:
        match = pattern.search(line)
        if match:
            posts.append(f"{base_url}{match.group(1)}\n")


# Get the posts in chronological order
posts.reverse()

with open("posts.txt", "w") as output:
    for post in posts:
        output.write(post)
