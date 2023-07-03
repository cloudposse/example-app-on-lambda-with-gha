-include $(shell curl -sSL -o .build-harness "https://cloudposse.tools/build-harness"; echo .build-harness)

%.png:
	@python diagramming.py

docs: readme publis_lambda.png
	@exit 0
