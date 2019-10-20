DEBUG		:=	1
ENVIRON		:=	development
FLASK		:=	application.py

_HOST		:=	::1
_PORT		:=	5000

CMD_VENV	:=	virtualenv
DIR_VENV	:=	venv
VER_PY		:=	3.7
CMD_PIP		:=	$(DIR_VENV)/bin/pip$(VER_PY)
CMD_PY		:=	$(DIR_VENV)/bin/python$(VER_PY)
CMD_PYTEST	:=	$(DIR_VENV)/bin/pytest
CMD_PYREV	:=	$(DIR_VENV)/bin/pyreverse
CMD_PYLINT	:=	$(DIR_VENV)/bin/pylint
CMD_ISORT	:=	$(DIR_VENV)/bin/isort
CMD_FLASK	:=	$(DIR_VENV)/bin/flask

CMD_CURL	:=	curl
CMD_MKDIR	:=	mkdir
CMD_RM		:=	rm
CMD_UNZIP	:=	unzip

DIR_SHORTER	:=	shorter
DIR_TESTS	:=	tests
DIR_TEMP	:=	temp

DIR_THEMES	:=	themes
DIR_DTHEME	:=	$(DIR_THEMES)/default
DIR_DTSTAT	:=	$(DIR_DTHEME)/static

VER_BULMA	:=	0.7.5
URL_BULMA	:=	https://github.com/jgthms/bulma/releases/download/$(VER_BULMA)/bulma-$(VER_BULMA).zip
TMP_BULMA	:=	$(DIR_TEMP)/bulma-$(VER_BULMA).zip
NME_BULMA	:=	bulma.min.css
ZPT_BULMA	:=	bulma-$(VER_BULMA)/css/$(NME_BULMA)
TGT_BULMA	:=	$(DIR_DTSTAT)/$(NME_BULMA)


.PHONY: help
help:
	@echo "make shorter"
	@echo "————————————"
	@echo
	@echo "venv             install virtualenv"
	@echo "requirements     install requirements into venv"
	@echo
	@echo "lint             run pylint"
	@echo "plot             run pyreverse"
	@echo "sort             run isort"
	@echo "test             run pytest"
	@echo "tslow            run pytest (including slow tests)"
	@echo "tcov, tcovh      run test coverage (html)"
	@echo
	@echo "clean            show files to clean"
	@echo "cleanup          clean files unknown to git"
	@echo
	@echo "run              run application"
	@echo "shell            launch a shell"
	@echo
	@echo "                 🦑"
	@echo


###
# plumbing

$(DIR_VENV):
	$(CMD_VENV) -p "python$(VER_PY)" "$(DIR_VENV)"

.PHONY: requirements requirements-dev requirements-mysql
requirements: $(CMD_FLASK)
requirements-dev: $(CMD_ISORT) $(CMD_PYLINT) $(CMD_PYREV) $(CMD_PYTEST)
requirements-mysql: $(DIR_VENV)
	$(CMD_PIP) install -r "requirements-mysql.txt"
$(CMD_FLASK): $(DIR_VENV)
	$(CMD_PIP) install -r "requirements.txt"
$(CMD_ISORT) $(CMD_PYLINT) $(CMD_PYREV) $(CMD_PYTEST): $(DIR_VENV)
	$(CMD_PIP) install -r "requirements-dev.txt"


###
# service

define PYLINT_MESSAGE_TEMPLATE
{C} {path}:{line}:{column} - {msg}
  ↪  {category} {module}.{obj} ({symbol} {msg_id})
endef
export PYLINT_MESSAGE_TEMPLATE

define _lint
	$(CMD_PYLINT) \
		--disable "C0111" \
		--msg-template="$$PYLINT_MESSAGE_TEMPLATE" \
		--output-format="colorized" \
			$(1)
endef

.PHONY: lint lintt
lint: $(CMD_PYLINT)
	$(call _lint,"$(DIR_SHORTER)")
lintt: $(CMD_PYLINT)
	$(call _lint,"$(DIR_TESTS)")


define _reverse
	$(CMD_PYREV) \
		--all-ancestors \
		--filter-mode="ALL" \
		--module-names="yes" \
		--output png \
		--project="$(1)$(2)" \
			$(1)
endef

.PHONY: plot plott
plot: $(CMD_PYREV)
	$(call _reverse,$(DIR_SHORTER))
plott: $(CMD_PYREV)
	$(call _reverse,$(DIR_TESTS),_$(DIR_SHORTER))


define _sort
	$(CMD_ISORT) -cs -fss -m=5 -y -rc $(1)
endef

.PHONY: sort sortt
sort: $(CMD_ISORT)
	$(call _sort,"$(DIR_SHORTER)")
sortt: $(CMD_ISORT)
	$(call _sort,"$(DIR_TESTS)")


define _test
	$(CMD_PYTEST) $(1) "$(DIR_TESTS)" -vv
endef
define _tcov
	$(call _test,$(1) --cov="$(DIR_SHORTER)")
endef

HTMLCOV		:=	htmlcov

.PHONY: test tcov tcovh
test: $(CMD_PYTEST)
	$(call _test,--durations=5)
tslow: $(CMD_PYTEST)
	$(call _test,--durations=5 --runslow)
tcov: $(CMD_PYTEST)
	$(call _tcov,)
tcovh: $(CMD_PYTEST)
	$(call _tcov,--cov-report="html:$(HTMLCOV)")

tcovh-open: tcovh
	$(CMD_PY) -m webbrowser -t "$(HTMLCOV)/index.html"

###
# cleanup

define _gitclean
	git clean \
		-e "*.py" \
		-e "*.sqlite" \
		-e ".env" \
		-e "secret.key" \
		-e "$(DIR_LOGS)/" \
		-e "$(DIR_THEMES)/*_dev" \
		-e "$(DIR_VENV)/" \
		$(1)
endef

.PHONY: clean cleanup
clean:
	$(call _gitclean,-ndx)
cleanup:
	$(call _gitclean,-fdx)


###
# flask

define _flask
	FLASK_DEBUG="$(DEBUG)" \
	FLASK_ENV="$(ENVIRON)" \
	FLASK_APP="$(FLASK)" \
	LOG_LVL="debug" \
	$(CMD_FLASK) $(1)
endef

.PHONY: shell run
run: $(CMD_FLASK) $(TGT_BULMA)
	$(call _flask,run --host "$(_HOST)" --port "$(_PORT)")
shell: $(CMD_FLASK)
	$(call _flask,shell)


###
# database

.PHONY: dbinit dbmig dbup dbdown
dbinit: $(CMD_FLASK)
	$(call _flask,db init)
dbmig: $(CMD_FLASK)
	$(call _flask,db migrate)
dbup: $(CMD_FLASK)
	$(call _flask,db upgrade)
dbdown: $(CMD_FLASK)
	$(call _flask,db downgrade)


###
# assets

$(TGT_BULMA):
	$(CMD_RM) -rfv "$(DIR_TEMP)" || true
	$(CMD_MKDIR) -v "$(DIR_TEMP)"
	$(CMD_CURL) -Lo "$(TMP_BULMA)" "$(URL_BULMA)"
	$(CMD_UNZIP) -d "$(DIR_DTSTAT)" -j "$(TMP_BULMA)" "$(ZPT_BULMA)"
	$(CMD_RM) -rfv "$(DIR_TEMP)"

.PHONY: assets
assets: $(TGT_BULMA)


###
# continuous integration

.PHONY: travis
travis: $(CMD_PYTEST)
	$(call _tcov,--durations=10 --runslow)
