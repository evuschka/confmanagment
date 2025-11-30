import argparse
from assembler import Assembler

def main():
    parser = argparse.ArgumentParser(description='Assembler for Educational Virtual Machine')
    parser.add_argument('--input', required=True, help='Path to source assembly file')
    parser.add_argument('--output', required=True, help='Path to output binary file')
    parser.add_argument('--test', action='store_true', help='Test mode: output intermediate representation')
    
    args = parser.parse_args()
    
    assembler = Assembler(args.input, args.output, args.test)
    assembler.assemble()

if __name__ == "__main__":
    main()
