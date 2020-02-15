INPUT_FILE = interns.csv
GENERATED_MATCHES_FILE = matches.json
GROUP_SIZE = 4

GENERATOR_SCRIPT = src/intern_social_matcher.py

.PHONY: all generate render clean

all: generate render

clean:
	rm $(GENERATED_MATCHES_FILE)

generate: $(INPUT_FILE) $(GENERATOR_SCRIPT)
	python3 $(GENERATOR_SCRIPT) $(INPUT_FILE) $(GROUP_SIZE) $(GENERATED_MATCHES_FILE)

run:
	./run.sh

format:
	black --exclude "venv/" .