build:
	pyinstaller --onefile src/receiver.py
	mv ./dist/receiver ./node

clean:
	rm -rf ./dist ./build
	rm receiver.spec ./node



