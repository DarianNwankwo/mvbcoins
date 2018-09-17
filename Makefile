build:
	echo '#!/usr/bin/env python3' | cat - src/main.py > src/main.py.tmp
	mv src/main.py.tmp src/main.py

clean:
	tail src/main.py -n +2 > src/temp.py
	mv src/temp.py src/main.py