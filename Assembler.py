import unittest
import Tables


def BoolToBit(value):
    return str(int(value))


def BoolsToBits(values):
    result = ""
    for v in values:
        result += BoolToBit(v)
    return result


def IntToBits(value):
    return "{0:b}".format(value)


class AddressInstruction:
    def __init__(self, address):
        self.address = address

    def GetAddress(self):
        return self.address

    def IsSymbol(self):
        return type(self.address) == str

    def IsAddress(self):
        return type(self.address) == int

    def SetAddress(self, value):
        self.address = value

    def ToBitString(self):
        if self.IsSymbol():
            raise Exception("Symbol wasn't replaced yet!")
        return "0"+IntToBits(self.address)


class DestinationBits:
    def __init__(self, ABit=False, DBit=False, MBit=False):
        self.A = ABit
        self.D = DBit
        self.M = MBit

    def HasA(self):
        return self.A

    def HasD(self):
        return self.D

    def HasM(self):
        return self.M

    def AddA(self):
        self.A = True

    def AddD(self):
        self.D = True

    def AddM(self):
        self.M = True

    def ToBitString(self):
        return BoolsToBits((self.A, self.M, self.D))


class testDestBits(unittest.TestCase):
    def test(self):
        bits = DestinationBits()
        assert(bits.ToBitString() == "000")
        bits.AddA()
        assert(bits.HasA())
        assert(bits.ToBitString() == "100")
        bits.AddM()
        assert(bits.HasM())
        assert(bits.ToBitString() == "110")
        bits.AddD()
        assert(bits.HasD())
        assert(bits.ToBitString() == "111")


class JumpBits:
    def __init__(self, J1=False, J2=False, J3=False):
        self.J1 = J1
        self.J2 = J2
        self.J3 = J3

    def AddJ1(self):
        self.J1 = True

    def AddJ2(self):
        self.J2 = True

    def AddJ3(self):
        self.J3 = True

    def ToBitString(self):
        return BoolsToBits((self.J1, self.J2, self.J3))


class testJumpBits(unittest.TestCase):
    def test(self):
        bits = JumpBits()
        assert(bits.ToBitString() == "000")
        bits.AddJ1()
        assert(bits.ToBitString() == "100")
        bits.AddJ2()
        assert(bits.ToBitString() == "110")
        bits.AddJ3()
        assert(bits.ToBitString() == "111")


class InstructionBits:
    def __init__(self, Expression):
        self.Expression = Expression

    def ToBitString(self):
        return Tables.comp_table[self.Expression]


class ControlInstruction:
    def __init__(self, instruction, destination, jumps):
        self.instruction = instruction
        self.destination = destination
        self.jumps = jumps


class testInstructionBits:
    def test(self):
        bits = InstructionBits("M+1")
        assert(bits.ToBitString() == "110111")
