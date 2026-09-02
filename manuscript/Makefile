# Makefile for LaTeX Manuscript Compilation

MAIN = main
LATEX = pdflatex -interaction=nonstopmode -halt-on-error
BIBTEX = bibtex

.PHONY: all pdf clean distclean

all: pdf

pdf: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex references.bib sections/*.tex tables/*.tex
	$(LATEX) $(MAIN).tex
	$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN).tex
	$(LATEX) $(MAIN).tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.nav *.snm *.fls *.fdb_latexmk sections/*.aux tables/*.aux

distclean: clean
	rm -f $(MAIN).pdf
