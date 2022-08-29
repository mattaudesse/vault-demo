.DEFAULT_GOAL := config

P=$${P:-$$(command -v python3.9 || command -v python3)}
V=$${V:-$$(command -v vault     || echo "$$(pwd)/vault")}
I=./venv/bin/python

deps:
	@if [ ! -x "$(P)" ]; then echo "Please pass python path like so: $(MAKE) P=/a/b/c/python3 <targets>"; exit 1; fi
	@if [ ! -x "$(V)" ]; then echo "Please pass vault path like so: $(MAKE) V=/a/b/c/vault <targets>";    exit 1; fi
	@if [ ! -d ./venv ] \
	  ; then echo 'Creating isolated Python "venv"...' \
	  ; $(P) -m venv ./venv \
	 && . ./venv/bin/activate \
	 && pip install -U pip \
	 && pip install -r reqs.txt \
	  ; fi

vault: deps
	@$(V) server -dev | tee vout

config: deps
	@$(I) config.py

a: deps
	@$(I) script.py a

b: deps
	@$(I) script.py b

clean:
	@([ -d ./venv   ] && rm -r ./venv)   || :
	@([ -f ./vout   ] && rm    ./vout)   || :
	@([ -f ./cred/a ] && rm    ./cred/a) || :
	@([ -f ./cred/b ] && rm    ./cred/b) || :
