build:
	cd src/ && pyinstaller --onefile main.py
	mv ./src/dist/main ./node

clean:
	rm -rf ./src/dist ./src/build
	rm ./src/main.spec ./node
