import re
from utils import number_to_int, encode_instruction

class Assembler:
    def __init__(self, input_path, output_path, test_mode=False):
        self.input_path = input_path
        self.output_path = output_path
        self.test_mode = test_mode
        self.instructions = []
        self.opcode_map = {
            'load_const': (63, 15),
            'read_mem': (49, 27),
            'write_mem': (59, 9),
            'neq_mem': (31, 0)
        }
    
    def parse_line(self, line):
        """Parse a single line of assembly code"""
        line = line.strip()
        if not line or line.startswith(';'):
            return None
        
        parts = re.split(r'\s+', line, 1)
        command = parts[0].lower()
        
        if command not in self.opcode_map:
            raise ValueError(f"Unknown command: {command}")
        
        opcode, bit_size = self.opcode_map[command]
        operand = None
        
        if len(parts) > 1 and command != 'neq_mem':
            operand_str = parts[1].split(';')[0].strip()
            operand = number_to_int(operand_str)
            
            # Validate operand range
            max_val = (1 << bit_size) - 1
            if not (0 <= operand <= max_val):
                raise ValueError(
                    f"Operand {operand} out of range for {command} "
                    f"(0-{max_val}, {bit_size} bits)"
                )
        
        return (opcode, operand if operand is not None else 0)
    
    def assemble(self):
        """Assemble the source file"""
        with open(self.input_path, 'r') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            try:
                instruction = self.parse_line(line)
                if instruction:
                    self.instructions.append(instruction)
            except Exception as e:
                raise ValueError(f"Line {i}: {str(e)}") from e
        
        if self.test_mode:
            self._output_test_mode()
        
        self._write_binary()
    
    def _output_test_mode(self):
        """Output intermediate representation in test mode"""
        for opcode, operand in self.instructions:
            print(f"({opcode}, {operand})")
    
    def _write_binary(self):
        """Write binary file"""
        with open(self.output_path, 'wb') as f:
            for opcode, operand in self.instructions:
                binary = encode_instruction(opcode, operand)
                f.write(binary)
