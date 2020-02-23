def printSomeWinPath():
	import ctypes
	from ctypes import wintypes, windll, create_unicode_buffer

	CSIDL_COMMON_APPDATA = 35

	_SHGetFolderPath = windll.shell32.SHGetFolderPathW
	_SHGetFolderPath.argtypes = [wintypes.HWND,
	                             ctypes.c_int,
	                             wintypes.HANDLE,
	                             wintypes.DWORD, wintypes.LPCWSTR]

	path_buf = create_unicode_buffer(wintypes.MAX_PATH)
	for i in range(100):
		result = _SHGetFolderPath(0, i, 0, 0, path_buf)
		print(i, path_buf.value)


print("All done")
