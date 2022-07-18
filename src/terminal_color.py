import sys

def yellow():
    sys.stdout.write("\033[93m") #yellow
    sys.stdout.write("\033[7m") #reverse
def red():
    sys.stdout.write("\033[0m") #reset
    sys.stdout.write("\033[91m") #red
def reverse():
    sys.stdout.write("\033[7m") #reverse
def cyan():
    sys.stdout.write("\033[96m") #cyan
def reset():
    sys.stdout.write("\033[0m") #reset

if __name__=="__main__":
    print("Please call this code from main.py only")