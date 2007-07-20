pastg=hello
borland_pas_tg=MIHDEEP2

all:	$(pastg) $(borland_pas_tg)


$(pastg):	%:	%.pas
	-gpc $(PFLAGS) -Wall  $< -o $@

$(borland_pas_tg):	%:	%.pas
	-gpc $(PFLAGS) -Wall --borland-pascal -o $@ $<

clean:
	-rm -f $(pastg) $(borland_pas_tg)
