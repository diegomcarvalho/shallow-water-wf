
build: source-download
	$(MAKE) -C kfs2d_rna_mirror
	$(MAKE) -C mpca-ann clean
	$(MAKE) -C mpca-ann

source-download:
	git clone https://github.com/robertopsouto/kfs2d_rna_mirror.git
	git clone https://github.com/scsr-inpe/mpca-ann.git
	cd mpca-ann; git checkout a52ad36
	cd ..
	touch source-download

clean:
	rm -fr kfs2d_rna_mirror mpca-ann source-download __pycache__ runinfo ann1.best
