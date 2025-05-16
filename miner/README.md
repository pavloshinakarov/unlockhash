# Requirements
```
	pip install -r requirements.txt
```

# How to run on windows or linux
```
	python3 run.py
```

# How to generate/build an .exe on windows
```
	python -m PyInstaller --onefile --console --add-data "C:\Python312\Lib\site-packages\pyfiglet\fonts;pyfiglet/fonts" run.py
```

# TODO:
```
	Future versions will have options for "collaborative pools" and "auto-claim".
```