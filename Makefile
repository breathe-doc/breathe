
all: html pdf

html: data
	$(MAKE) -C documentation html

pdf: data
	$(MAKE) -C documentation latexpdf
	
data:
	$(MAKE) -C examples/doxygen all
	$(MAKE) -C examples/tinyxml all
	$(MAKE) -C examples/specific all

distclean: clean
	$(MAKE) -C documentation clean

clean:
	$(MAKE) -C examples/doxygen $@
	$(MAKE) -C examples/tinyxml $@
	$(MAKE) -C examples/specific $@

test:
	cd tests && pytest -v

dev-test:
	cd tests && PYTHONPATH=../:$(PYTHONPATH) pytest -v

flake8:
	flake8 breathe/*.py \
		breathe/directive/*.py \
		breathe/finder/*.py \
		breathe/renderer/sphinxrenderer.py \
		breathe/renderer/filter.py \
		breathe/parser/compound.py
