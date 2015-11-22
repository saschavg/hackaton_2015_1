PYTHON=`. venv/bin/activate; which python`
PIP=`. venv/bin/activate; which pip`
DEPS:=requirements.txt


.PHONY: clean distclean test shell deps all

all: deps test

clean:
	@find . -name "*.pyc" -delete

distclean: clean
	rm -rf venv

install: clean deps

go: 
	PYTHONPATH=$(CURDIR) $(PYTHON) queens_server.py 

venv:
	virtualenv -p python2.7 venv
	$(PIP) install -U "pip>=7.0"
	$(PIP) install -r $(DEPS)

deps: venv
	$(PIP) install -r $(DEPS) -U

test: venv
	PYTHONPATH=$(CURDIR) $(PYTHON) test_Queens.py

shell: venv
	$(PIP) install ipython
	$(CURDIR)/venv/bin/ipython

run: venv
	PYTHONPATH=$(CURDIR) $(PYTHON) queens.py
