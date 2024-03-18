import win32process
import win32gui
from ctypes import windll, c_int, byref  # , c_ulong

user32 = windll.user32
kernel32 = windll.kernel32
# psapi = windll.psapi
ReadProcessMemory = kernel32.ReadProcessMemory
WriteProcessMemory = kernel32.WriteProcessMemory

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
# VIRTUAL_MEM = (0x1000 | 0x2000)
# PAGE_EXECUTE_READWRITE = 0x00000040

PROCESS_NAME = "Tiberian Sun"
PLAYER_BASE = 0x3E2284  # player base
MONEY_OFFSET = 0x1A4  # money offset


def GetProcess():  # 获取游戏进程
	window = win32gui.FindWindow(PROCESS_NAME, PROCESS_NAME)  # 查找游戏窗体
	hid, pid = win32process.GetWindowThreadProcessId(window)  # 根据窗体得到进程编号
	process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)  # 用最高权限打开进程
	return process  # 返回的是进程地址


def GetValue(process, base, offset):
	data = c_int(0)
	# When amd64 is compatible with 32-bit programs, 
	# an offset of 0x400000 must be added to the starting address.
	ReadProcessMemory(int(process), base + 0x400000, byref(data), 4, None)
	ReadProcessMemory(int(process), data.value + offset, byref(data), 4, None)
	return data.value


def SetValue(process, base, offset, value):
	data = c_int(0)
	# When amd64 is compatible with 32-bit programs, 
	# an offset of 0x400000 must be added to the starting address.
	ReadProcessMemory(int(process), base + 0x400000, byref(data), 4, None)
	address = data.value
	data = c_int(value)
	WriteProcessMemory(int(process), address + offset, byref(data), 4, None)


def main():
	p = GetProcess()
	if p == 0:
		print(f"no {PROCESS_NAME} process found!")
		return
	money = GetValue(p, PLAYER_BASE, MONEY_OFFSET)
	print(f"money was {money}")
	SetValue(p, PLAYER_BASE, MONEY_OFFSET, money + 200000)
	print(f"money is modded to {money}")


if __name__ == '__main__':
	main()
