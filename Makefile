RM        		= rm -f
GENERATED_MOD	= breathe/_parser.py

.PHONY: all
all: html pdf

.PHONY: html
html: data
	$(MAKE) -C documentation html

.PHONY: pdf
pdf: data
	$(MAKE) -C documentation latexpdf
	
.PHONY: data
data:
	$(MAKE) -C examples/doxygen all
	$(MAKE) -C examples/tinyxml all
	$(MAKE) -C examples/specific all

$(GENERATED_MOD): \
		xml_parser_generator/schema.json \
		xml_parser_generator/module_template.py.in \
		xml_parser_generator/make_parser.py
	python3 xml_parser_generator/setuptools_builder.py

.PHONY: distclean
distclean: clean
	$(MAKE) -C documentation clean
	$(RM) $(GENERATED_MOD)

.PHONY: clean
clean:
	$(MAKE) -C examples/doxygen $@
	$(MAKE) -C examples/tinyxml $@
	$(MAKE) -C examples/specific $@

.PHONY: test
test:
	cd tests && python3 -m pytest -v

.PHONY: dev-test
dev-test: $(GENERATED_MOD)
	cd tests && PYTHONPATH=../:$(PYTHONPATH) python3 -m pytest -v

.PHONY: flake8
flake8:
	flake8 breathe

.PHONY: black
black:
	black --check .

.PHONY: type-check
type-check: $(GENERATED_MOD)
	mypy --warn-redundant-casts --warn-unused-ignores breathe tests

.PHONY: version-check
version-check:
	 PYTHONPATH=../:$(PYTHONPATH) python3 scripts/version-check.py
