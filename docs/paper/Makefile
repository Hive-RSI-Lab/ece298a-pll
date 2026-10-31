# Build the paper. Figures: make figs (needs uv; no EDA tools).
paper.pdf: paper.tex $(wildcard figs/*.pdf)
	pdflatex -interaction=nonstopmode -halt-on-error paper.tex >/dev/null
	pdflatex -interaction=nonstopmode -halt-on-error paper.tex >/dev/null
	@echo built paper.pdf
figs:
	cd ../.. && uv run -q --python 3.12 --no-project --with gdstk --with matplotlib --with numpy python docs/paper/make_figs.py
clean:
	rm -f paper.aux paper.log paper.out
.PHONY: figs clean
