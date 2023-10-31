pdf_files=math650_hw1_R_intro_regression.pdf math650_hw2.pdf math650_hw3_1.pdf math650_hw3_2.pdf math650_hw4.pdf math650_hw5.pdf math650_hw6.pdf math650_hw7.pdf math650_hw8.pdf math650_hw9.pdf math650_hw10.pdf math650_hw11.pdf
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

