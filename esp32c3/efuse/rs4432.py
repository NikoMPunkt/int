#Galois field arithmetic functions for GF(2^8) with primitive polynomial 0x11D
# RS(n,k): n is the total length of the codeword; k is the length of the original message.
# Length of original message is 32 bytes
# Return message length is 44 bytes

class RS:
    def __init__(self, polynom= 0x11D):
        self.polynom = 0x11d # x8 + x4 + x3 + x2 + x0
        self.nsym =12 # The number of parity symbols 44 - 32
        self.field_size = 256 # max term is x8 --> 2^8 field_size


    def __gf_mult(self, x, y):
        r = 0
        while y:
            if y & 1:
                r ^= x
            y >>= 1
            x <<= 1
            if x & self.field_size:
                x ^= self.polynom
        return r

    def __gf_pow(self, x, power):
        r = 1
        for _ in range(power):
            r = self.__gf_mult(r, x)
        return r

    def __gf_poly_mult(self, p, q):
        r = [0] * (len(p) + len(q) - 1)
        for j in range(len(q)):
            for i in range(len(p)):
                r[i + j] ^= self.__gf_mult(p[i], q[j])
        return r

    # RS encoding and decoding functions
    def __rs_generator_poly(self):
        g = [1]
        for i in range(self.nsym):
            g = self.__gf_poly_mult(g, [1, self.__gf_pow(2, i)])
        return g

    def Encode_msg(self, msg_in):
        gen = self.__rs_generator_poly()
        msg_out = [0] * (len(msg_in) + len(gen) - 1)
        msg_out[:len(msg_in)] = msg_in
        for i in range(len(msg_in)):
            coef = msg_out[i]
            if coef != 0:
                for j in range(1, len(gen)):
                    msg_out[i + j] ^= self.__gf_mult(gen[j], coef)
        msg_out[:len(msg_in)] = msg_in
        return msg_out








