# The PLL paper

[paper.pdf](paper.pdf): the design and its results written up as a paper, with
figures drawn from the results this repository records.

    make figs     # redraw figs/ from the recorded reports and data/ (uv, no EDA tools)
    make          # build paper.pdf (pdflatex)

`data/` holds the two post-layout ngspice results that are not gate reports:
the VCO tuning curves at four corners and the TSPC divider waveform.
`sims/make_decks.py` then `sims/run_sims.sh` re-run them on the extracted
netlist (~40 min, needs the EDA tree via `~/modules/bin/eda-env`).
