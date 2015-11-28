PYTHON=`. venv/bin/activate; which python`
PIP=`. venv/bin/activate; which pip`
DEPS:=requirements.txt


.PHONY: clean distclean test shell deps all build

all: deps test

clean:
	@pwd
	@rm -f *.pyc *.so *.c 
	@rm -rf ./bulid

distclean: clean
	rm -rf venv

install: clean distclean deps build

go: 
	PYTHONPATH=$(CURDIR) $(PYTHON) queens_server.py 

build:
	python setup.py build_ext --inplace

venv:
	virtualenv -p python2.7 venv
	$(PIP) install -U "pip>=7.0"
	$(PIP) install -r $(DEPS)

deps: venv
	$(PIP) install -r $(DEPS) -U

test: venv
	#PYTHONPATH=$(CURDIR) $(PYTHON) test_Queens.py TestQueensGame.test_position_needs_lock_1
	python test_Queens.py

shell: venv
	$(PIP) install ipython
	$(CURDIR)/venv/bin/ipython

run: venv 
	PYTHONPATH=$(CURDIR) $(PYTHON) queens_runner.py
