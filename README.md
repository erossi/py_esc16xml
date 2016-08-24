# py_esc16xml
Simple converter ESC 2016 events from php-json to xml-pentabarf compatibile calendar (almost).

### Json can be obtained from
https://www.endsummercamp.org/API/ls_sched_talk.php

Please do:

	curl https://www.endsummercamp.org/API/ls_sched_talk.php > esc16.json
	python3 escjsontoxlm.py

and see the output.xml generated.

You can use [ConfClerk](http://www.toastfreeware.priv.at/confclerk/)
or [Giggity](https://wilmer.gaa.st/main.php/giggity.html).
