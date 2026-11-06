LATEX ?= xelatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all article example dist clean

all: article example

article:
	python3 scripts/render_article.py
	mkdir -p build
	$(LATEX) $(LATEX_FLAGS) -output-directory=build article.tex
	$(LATEX) $(LATEX_FLAGS) -output-directory=build article.tex

example:
	mkdir -p example/build
	$(LATEX) $(LATEX_FLAGS) -output-directory=example/build example/example.tex
	$(LATEX) $(LATEX_FLAGS) -output-directory=example/build example/example.tex

dist:
	mkdir -p dist/misis-article
	cp misisarticle.cls article.tex README.md LICENSE dist/misis-article/
	cd dist && zip -r misis-article.zip misis-article

clean:
	rm -rf build example/build dist
	rm -f *.aux *.log *.out *.toc *.bbl *.blg *.bcf *.run.xml *.xdv *.synctex.gz *.fls *.fdb_latexmk
