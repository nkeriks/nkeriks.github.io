all:
	cd cv && python build_cv.py && pdflatex cv.tex && cp -f cv.pdf ../source/pdf/eriksson-cv.pdf && cd -
	quarto render source

