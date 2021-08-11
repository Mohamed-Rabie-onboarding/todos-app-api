test:
	DEV=True python3 -m pytest tests/ -s -p no:warnings -q

dev:
	DEV=True poetry run python3.9 main.py

docs:
	pdoc3 app --html --output-dir docs/_build --force

docs-serve:
	python3 -m http.server --directory ./docs/_build/app

docs-clear:
	rm -r docs