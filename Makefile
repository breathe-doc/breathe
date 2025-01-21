
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

.PHONY: distclean
distclean: clean
	$(MAKE) -C documentation clean

.PHONY: clean
clean:
	$(MAKE) -C examples/doxygen $@
	$(MAKE) -C examples/tinyxml $@
	$(MAKE) -C examples/specific $@

.PHONY: test
test:
	cd tests && python3 -m pytest -v

.PHONY: dev-test
dev-test:
	cd tests && PYTHONPATH=../:$(PYTHONPATH) python3 -m pytest -v

.PHONY: ruff
ruff:
	ruff check
	ruff format

.PHONY: type-check
type-check:
	mypy
