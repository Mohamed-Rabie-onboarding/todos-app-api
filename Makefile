serve:
	DEV=True poetry run python3.9 app/__init__.py

docs:
	pdoc3 app --html --output-dir docs/api --force
