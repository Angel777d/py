from pathlib import Path


def clearItem(item):
	children = [c for c in item.children.values()]
	for child in children:
		child.destroy()


def writeFile(path: Path, value: str):
	try:
		path.parent.mkdir(exist_ok=True)
		text_file = Path.open(path, "w", encoding="utf-8")
		text_file.write(value)
		text_file.close()
	except IOError as err:
		print("Can't write file: %s." % path, err)
	except TypeError as err:
		print("Can't write file: %s." % path, err)


def readFile(path: Path) -> str:
	token = ""
	try:
		f = Path.open(path, "r", encoding="utf-8")
		if f.mode == 'r':
			token = f.read()
	except IOError as err:
		print("File %s is not accessible:" % path, err)
	except TypeError as err:
		print("File %s is not accessible:" % path, err)

	return token


def emptyHandler(*args, **kwargs):
	print("[---] emptyHandler", args, kwargs)
	pass
