PYTHON ?= python3

.PHONY: check render test

check:
	$(PYTHON) scripts/validate_reading_list.py
	$(PYTHON) scripts/render_readme.py --check

render:
	$(PYTHON) scripts/render_readme.py

test:
	$(PYTHON) -m unittest discover -s tests -v
