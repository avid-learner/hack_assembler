import unittest
import Tables


def BoolToBit(value):
    return str(int(value))


def testBoolToBit():
    assert(BoolToBit(True) == "1")
    assert(BoolToBit(False) == "0")


def BoolsToBits(values):
    result = ""
    for v in values:
        result += BoolToBit(v)
    return result


def testBoolsToBits():
    assert(BoolsToBits((True, False, True)) == "101")


def IntToBits(value):
    return "{0:015b}".format(value)


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


class TestAddressInstruction(unittest.TestCase):
    def testToBits(self):
        a = AddressInstruction(56)
        assert(a.ToBitString() == "0000000000111000")

    def testSymbolToBits(self):
        a = AddressInstruction("variable")
        self.assertRaises(Exception, a.ToBitString)


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
        return BoolsToBits((self.A, self.D, self.M))

    def ToPlainStr(self):
        if self.A:
            return "A"
        if self.D:
            return "D"
        if self.M:
            return "M"


class testDestBits(unittest.TestCase):
    def test(self):
        bits = DestinationBits()
        assert(bits.ToBitString() == "000")
        bits.AddA()
        assert(bits.HasA())
        assert(bits.ToBitString() == "100")
        bits.AddM()
        assert(bits.HasM())
        assert(bits.ToBitString() == "101")
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

    def RemoveJ1(self):
        self.J1 = False

    def RemoveJ2(self):
        self.J2 = False

    def RemoveJ3(self):
        self.J3 = False

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

    def ToBitString(self):
        return "111"+self.instruction.ToBitString() + self.destination.ToBitString() + self.jumps.ToBitString()


class testInstructionBits:
    def test(self):
        bits = InstructionBits("M+1")
        assert(bits.ToBitString() == "1110111")
        for instr in Tables.comp_table:
            bits = InstructionBits(instr)
            assert(bits.ToBitString() == Tables.comp_table[instr])


class Label:
    def __init__(self, name):
        self.name = name
