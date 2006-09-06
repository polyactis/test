pdf_files=math650_hw1.pdf math650_hw2.pdf
all:	$(pdf_files)
.SUFFIXES:	.xml	.pdf	.html	.fo	.dvi	.ps


.tex.dvi:
	latex $<
	latex $<

.dvi.ps:
	dvips $<

.ps.pdf:
	ps2pdf $<

#-refdbib -d ref -S refdbteststyle -t bibtex $@.aux > $@.bib
#-bibtex $@
#-makeindex $@
#-latex $@

clean:
	-rm -f *.out *.log *.aux *.pdf *.ps *.dvi *.html *.fo *.rtf *.err *.xsl *.*~ *.toc *.bbl *.blg *.backup *.idx *.ilg *.ind


clear:
	-rm -f *.out *.log *.aux *.ps  *.html *.fo *.rtf *.err *.xsl *.*~ *.toc *.bbl *.blg *.backup

