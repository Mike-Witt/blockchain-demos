#
# blockchain parsing classes for experimentation
#

import sys

def ERROR(msg):
    print('Couldn\'t continue because:')
    print(msg)
    exit(0)

def DBG(msg):
    #print(msg)
    return

def prt(msg):
    import sys
    sys.stdout.write(msg)

def prthex(hexstr, indent='', nchars=72):
    length = len(hexstr)
    start = 0
    while(start < length):
        end = min( start + nchars, length)
        prt(indent + hexstr[start:end] + '\n')
        start = end 

class BC_Obj(object):
    def __init__(self, hexstr, ptr):
        self.ptr = ptr
        self.len = 0
        self.hex = ''

    def display(self, indent=''):
        prt(indent + 'Obj: ' + self.hex)

class BC_Int32(BC_Obj):
    def __init__(self, hexstr, ptr):
        self.ptr = ptr
        self.len = 8 # 4 bytes long (8 hex digits)
        self.hex = hexstr[ptr:ptr+self.len]
        # I believe it's in little endian byte order
        vb = bytearray.fromhex(self.hex)
        self.int = vb[0] + vb[1]*256 + vb[2]*256*256 + vb[3]*256*256*256
        # NOTE: The documentation has some int32_t == signed int.
        # But I'm handiling all integers as unsinged.

    def display(self, indent=''):
        import locale
        locale.setlocale(locale.LC_ALL, '')
        number = locale.format("%d", self.int, grouping=True)
        prt(indent + '32 bit integer: ' + self.hex + ' = %s'%number + '\n')

class BC_Int64(BC_Obj):
    def __init__(self, hexstr, ptr):
        self.ptr = ptr
        self.len = 16 # 8 bytes long (16 hex digits)
        self.hex = hexstr[ptr:ptr+self.len]
        # I believe it's in little endian byte order
        vb = bytearray.fromhex(self.hex)
        self.int = vb[0] + vb[1]*256 + vb[2]*256*256 + vb[3]*256*256*256\
            + vb[4]*256*256*256*256\
            + vb[5]*256*256*256*256*256\
            + vb[6]*256*256*256*256*256*256\
            + vb[7]*256*256*256*256*256*256*256
        # NOTE: The documentation has some int64_t == signed int.
        # But I'm handiling all integers as unsinged.

    def display(self, indent=''):
        import locale
        locale.setlocale(locale.LC_ALL, '')
        number = locale.format("%d", self.int, grouping=True)
        prt(indent + '64 bit integer: ' + self.hex + ' = %s'%number + '\n')

class BC_Varint(BC_Obj):
    def __init__(self, hexstr, ptr):
        # Parse the varint in the hex string at location ptr.
        # Return the integer and the length of the varint.
        self.ptr = ptr

        # en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer
        first_byte = int( hexstr[ptr:ptr+2], base=16 )
        if first_byte < 0xFD:
            # This one byte contains the number of transactions
            self.int = first_byte
            self.len = 2
        else:
            # The next line of the spec says "<=" 0xFFFF. Is that right?
            ERROR('Haven\'t implemented varint > 1 yet!')

        self.hex = hexstr[ptr : ptr + self.len]

    def display(self, indent=''):
        prt(indent + 'Varint: ' + self.hex + ' = %s'%self.int + '\n')

class BC_Input(BC_Obj):
    # A single transaction input. We create one by giving it the
    # transaction hex string and the position to start parsing.
    # The 'len' field can be used to get to the next thing in the tx.
    def __init__(self, hexstr, ptr):
        DBG('  Input at: %d'%ptr)
        self.ptr = ptr
        # Previous output is a fixed 36 byte field. 72 hex digits.
        prev_out_hex_len = 72
        self.previous_output = hexstr[ptr:ptr+prev_out_hex_len]
        DBG('    previous_output: %s'%self.previous_output)
        ptr += prev_out_hex_len
        self.script_len_varint = BC_Varint(hexstr, ptr)
        self.script_hex_len = self.script_len_varint.int * 2
        ptr += self.script_len_varint.len
        self.script = hexstr[ptr:ptr + self.script_hex_len]
        ptr += self.script_hex_len
        DBG('    script: %s'%self.script)
        self.sequence = hexstr[ptr:ptr+8]
        DBG('    sequence: %s'%self.sequence)
        self.len = prev_out_hex_len + self.script_len_varint.len\
            + self.script_hex_len + 8
        self.hex = hexstr[ptr:ptr+self.len]

    def display(self, indent=''):
        prt(indent + 'Input: length = %s hex characters'%self.len + '\n')
        indent += '  ' 
        prt(indent + 'Previous output:\n')
        prthex(self.previous_output, indent + '  ')
        prt(indent + 'Script length:\n')
        self.script_len_varint.display(indent + '  ')
        prt(indent + 'Script:\n')
        prthex(self.script, indent + '  ')
        prt(indent + 'Sequence: %s'%self.sequence + '\n')

class BC_Output(BC_Obj):
    # A single transaction ouput.
    def __init__(self, hexstr, ptr):
        self.ptr = ptr
        self.value = BC_Int64(hexstr, ptr)
        self.len = self.value.len
        ptr += self.value.len

        self.script_len_varint = BC_Varint(hexstr, ptr)
        self.len += self.script_len_varint.len
        ptr += self.script_len_varint.len
        self.pk_script_hex_length = self.script_len_varint.int * 2

        self.pk_script = hexstr[ptr:ptr+self.pk_script_hex_length]
        self.len += self.pk_script_hex_length
        ptr += self.pk_script_hex_length

        self.hex = hexstr[self.ptr:ptr]

    def display(self, indent=''):
        prt(indent + 'Output: length = %s hex characters'%self.len + '\n')
        indent += '  ' 
        prthex(self.hex, indent)
        prt(indent + 'value:\n')
        self.value.display(indent + '  ')
        prt(indent + 'pk_script length:\n')
        self.script_len_varint.display(indent + '  ')
        prt(indent + 'pk_script:\n')
        prthex(self.pk_script, indent + '  ')

class BC_Transaction(BC_Obj):
    def __init__(self, hexstr, ptr):
        self.version = BC_Int32(hexstr, 0)
        self.len = self.version.len
        self.n_inputs = BC_Varint(hexstr, self.len)
        self.len += self.n_inputs.len
        DBG('%d inputs'%self.n_inputs.int)

        self.inputs = []
        for i in range(self.n_inputs.int):
            input = BC_Input(hexstr, self.len)
            self.inputs.append(input)
            self.len += input.len
            DBG('  Input %s: %s'%(i, input.hex))

        self.n_outputs = BC_Varint(hexstr, self.len)
        self.len += self.n_outputs.len

        self.outputs = []
        for i in range(self.n_outputs.int):
            output = BC_Output(hexstr, self.len)
            self.outputs.append(output)
            self.len += output.len

        self.locktime = BC_Int32(hexstr, self.len)
        self.len += self.locktime.len

        self.hex = hexstr[ptr:ptr+self.len]

    def display(self, indent=''):

        # First find the lengths of all the fields and display the
        # field-delimited hex string.
        lengths = [] # Lengths of fields in the hex string
        lengths.append(self.version.len)
        lengths.append(self.n_inputs.len)
        for input in self.inputs:
            lengths.append(input.len) 
        lengths.append(self.n_outputs.len)
        for output in self.outputs:
            lengths.append(output.len) 
        # (Display the entire transaction with breaks between fields)
        pointer = 0
        dispstr = ''
        for length in lengths:
            dispstr += self.hex[pointer:pointer+length]
            dispstr += '|'
            pointer += length
        prthex(dispstr, indent)

        # Now display the individual fields
        prt('version:\n')
        self.version.display(indent)
        prt('tx_in:\n')
        self.n_inputs.display(indent)
        prt('Inputs:\n')
        for input in self.inputs:
            input.display(indent)
        prt('tx_out:\n')
        self.n_outputs.display(indent)
        prt('Outputs:\n')
        for output in self.outputs:
            output.display(indent)
        prt(indent + 'locktime: %s\n'%self.locktime.hex)

