quick :
	pdflatex Report.tex

all : Report.aux
	echo "pdf with references"
	bibtex Report.aux
	pdflatex Report.tex
	pdflatex Report.tex

full : Report.aux
	echo "pdf with references and index"
	bibtex Report.aux
	makeindex Report
	pdflatex Report.tex
	pdflatex Report.tex

Report.aux :
	pdflatex Report.tex
	
clean :
	rm -f q*.aux *.toc *.blg *.bbl *.out *.log *.ilg *.ind *.idx

	
