from src.garcon import Garcon
from src.recorder import Recorder

gc = Garcon()

def main():
	gc.enter_func()
	recorder = Recorder()
	recorder.record()

if __name__=='__main__':
	main()