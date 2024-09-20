import sys


class TerminalColor:
    @staticmethod
    def yellow():
        sys.stdout.write("\033[93m")  # yellow
        sys.stdout.write("\033[7m")  # reverse

    @staticmethod
    def red():
        sys.stdout.write("\033[0m")  # reset
        sys.stdout.write("\033[91m")  # red

    @staticmethod
    def reverse():
        sys.stdout.write("\033[7m")  # reverse

    @staticmethod
    def cyan():
        sys.stdout.write("\033[96m")  # cyan

    @staticmethod
    def reset():
        sys.stdout.write("\033[0m")  # reset


if __name__ == "__main__":
    print("Don't run this file directly.")
