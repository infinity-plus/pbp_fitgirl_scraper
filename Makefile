CC      = nuitka3
PKG     = pip
INTERP  = python3
FL      = fitgirl_scraper.py
OPT     = --onefile --disable-console --output-filename=FitGirl-Scraper.exe

all:
	$(CC) $(OPT) --quiet $(FL)

verbose:
	$(CC) $(OPT) --verbose $(FL)

setup:
	$(PKG) install -r requirements.txt

run:
	$(INTERP) $(FL)
