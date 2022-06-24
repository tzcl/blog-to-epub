all: clean fetch merge bind

clean:
	@echo "🗑  Cleaning up..."
	rm -rf articles posts stopa.md stopa.epub

fetch:
	@echo "🧠 Downloading articles from stopa.io..."
	pipenv install
	pipenv run python posts.py
	mkdir articles
	pipenv run python stopa.py

merge:
	@echo "🌪  Merging articles..."
	pandoc articles/*.md -o stopa.md -f markdown_strict

bind:
	@echo "📒 Binding the EPUB... "
	pandoc articles/*.md -o stopa.epub -f markdown_strict --metadata-file=metadata.yaml --toc --toc-depth=1
	@echo "🎉 EPUB file created."
