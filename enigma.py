class Rotor:
    
    def __init__(self, wiring, state, ring, notch):
        self.wiring = wiring
        self.iwiring = {}
        for count, i in enumerate(self.wiring):
            self.iwiring[i] = count
        self.state = state
        self.ring = ring
        self.notch = notch
        
    def incrament_state(self):
        self.state = (self.state + 1) % 26
        
    def set_state(self, state):
        self.state = state
        
    def forward_encode(self, char):
        n = ord(char)
        m = (n - ord('A') + self.state - self.ring) % 26
        encode = self.wiring[m]
        encode = chr(ord(encode) - self.state + self.ring)
        return encode
        
    def reverse_encode(self, char):
        n = (ord(char) - ord('A') + self.state - self.ring) % 26 + ord('A')
        m = self.iwiring[chr(n)]
        encode = chr((m - self.state + self.ring) % 26 + ord('A'))
        return encode
    
    
class Reflector:
    
    def __init__(self, wiring):
        self.wiring = wiring
        
    def reflect(self, char):
        n = ord(char)
        m = (n - ord('A')) % 26
        encode = self.wiring[m]
        return encode
    

class Machine:
    
    def __init__(self):
        #                   '01234567890123456789012345'
        #                   'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.rotor1 = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 2, 8, 17)
        self.rotor2 = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 2, 8, 5)
        self.rotor3 = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 2, 8, 22)
        self.reflector = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
        
    def encode(self, text):
        output = ''
        for char in text:
            cap_flag = char.isupper()
            cap = char.upper()
            n = ord(cap)
            if n >= 65 and n <= 90:
                self.rotor3.incrament_state()
                if self.rotor3.state == self.rotor3.notch:
                    self.rotor2.incrament_state()
                if self.rotor2.state == self.rotor2.notch:
                    self.rotor1.incrament_state()
                    
                out = self.rotor3.forward_encode(cap)
                out = self.rotor2.forward_encode(out)
                out = self.rotor1.forward_encode(out)
                out = self.reflector.reflect(out)
                out = self.rotor1.reverse_encode(out)
                out = self.rotor2.reverse_encode(out)
                out = self.rotor3.reverse_encode(out)

                if not cap_flag:
                    out = out.lower()
                output += out
            else:
                output += char
        print(output)
                
                
if __name__ == '__main__':
    machine = Machine()
    machine.encode('aaaaa')
    # machine.encode('Hello World, abcd')
    
    # machine.rotor1.set_state(0)
    # machine.encode('Fgqtj Tguil, fjkg')
    
            

