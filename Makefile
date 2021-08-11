app-serve:
	DEV=True poetry run python3.9 app/main.py

docs:
	pdoc3 app --html --output-dir docs/_build --force --skip-errors

docs-serve:
	python3 -m http.server --directory ./docs/_build/app