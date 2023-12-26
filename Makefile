-include $(shell curl -sSL -o .build-harness "https://cloudposse.tools/build-harness"; echo .build-harness)

build:
	@exit 0 # for python projects, we don't need to build anything, for other languages, we might need to build something

%.png:
	@python diagramming.py


readme: 
	README_TEMPLATE_FILE=docs/README.md.gotmpl make readme/build
	@exit 0

docs: readme publis_lambda.png
	@exit 0
