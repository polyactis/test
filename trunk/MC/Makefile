
.SUFFIXES:	.pdf

latex_files=problems

all:	$(latex_files)

$(latex_files):	%:	%.tex
	latex $@
	-refdbib -d ref -S refdbteststyle -t bibtex $@.aux > $@.bib
	-bibtex $@
	-makeindex $@
	-latex $@
	-latex $@
	-dvipdf $@.dvi

clean:
	-rm -f *.out *.log *.aux *.pdf *.ps *.dvi *.html *.fo *.rtf *.err *.xsl *.*~ *.toc *.bbl *.blg *.backup *.idx *.ilg *.ind


clear:
	-rm -f *.out *.log *.aux *.ps  *.html *.fo *.rtf *.err *.xsl *.*~ *.toc *.bbl *.blg *.backup

