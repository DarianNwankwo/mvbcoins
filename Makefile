build:
	cd src/ && pyinstaller --onefile receiver.py
	mv ./src/dist/receiver ./node

clean:
	rm -rf ./src/dist ./src/build
	rm ./src/receiver.spec ./node
