import sys

def main():
    print("Hello from liteview!")


if __name__ == "__main__":
    num_args = len(sys.argv)
    ## user passed in argument
    if(num_args == 2):
        ##bring up TUI
        print(sys.argv)
    else:
        print("Please pass in SQLITE db path")
