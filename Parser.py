import unittest
import Tables
import Assembler
import pyparsing

class SymbolTable:

    def __init__(self, startingValue=16):
        self.table = {}
        self.nextValue = startingValue

    def AddPreDefVariable(self, name, value):
        self.table[name] = value

    def AddVariable(self, name):
        if name in self.table:
            raise Exception("Symbol already exists!")
        self.table[name] = self.FindNewValue()

    def HasSymbol(self, name):
        return name in self.table

    def AddLabel(self, name, address):
        if name in self.table:
            raise Exception("Label already exists!")
        self.table[name] = address

    def GetSymbolValue(self, name):
        if name not in self.table:
            raise Exception("Symbol not found!")
        return self.table[name]

    def FindNewValue(self):
        result = self.nextValue
        self.nextValue += 1
        return result


class Program:
    def __init__(self):
        self.operations = []
        self.table = SymbolTable()

    def AddOperation(self, op):
        self.content.append(op)

    def AddLabel(self, name):
        # add label pointing to next operation
        self.table.AddLabel(name, len(self.operations))

    # gets called only after whole program has been read
    def FillSymbolTable(self):
        for symbolName in Tables.predef_table:
            self.table.AddPreDefVariable(symbolName, Tables.predef_table[symbolName])
        for op in self.operations:
            if type(op) == Assembler.AddressInstruction:
                if op.IsSymbol():
                    if not self.table.HasSymbol(op.GetAddress()):
                        self.table.AddVariable(op.GetAddress())

    def ReplaceSymbols(self):
        for op in self.operations:
            if type(op) == Assembler.AddressInstruction:
                if op.IsSymbol():
                    if not self.table.HasSymbol(op.GetAddress()):
                        raise Exception("Symbol not found!")
                    op.SetAddress(self.table.GetSymbolValue(op.GetAddress()))


class Parser:
    def __init__(self):
        from pyparsing import Literal, CaselessLiteral, Word, OneOrMore, ZeroOrMore, \
        Forward, NotAny, delimitedList, oneOf, Group, Optional, Combine, alphas, nums, restOfLine, cStyleComment, \
        alphanums, printables, empty, quotedString, ParseException, ParseResults, Keyword
        self.a_line = "@" + (Word(alphas, alphanums) | Word(nums)).setParseAction(lambda s,l,t: self.GotAddress(t))
        self.command = Word("ADM-+10|&!")
        self.c_line = Optional(Word("AMD").setParseAction(lambda s,l,t: self.GotTarget(t)) + "=") \
            + self.command.setParseAction(lambda s,l,t: self.GotCommand(t)) \
            + Optional(";" + Word("JLPNGEQTM").setParseAction(lambda s,l,t: self.GotJump(t)))
        self.cmd = self.a_line | self.c_line
        self.newAddress = None
        self.newTarget = None
        self.newCommand = None
        self.newJump = None

    def GotCommand(self, cmd):
        self.newCommand = cmd
        if self.newCommand not in Tables.comp_table:
            raise Exception("wrong target expression")
        self.newCommand = Assembler.InstructionBits(cmd)


    def GotTarget(self, trg):
        self.newTarget = trg
        if self.newTarget not in Tables.dest_table:
            raise Exception("wrong target expression")
        self.newTarget = Assembler.DestinationBits("A" in trg, "D" in trg, "M" in trg)

    def GotJump(self, jmp):
        self.newJump = jmp
        if self.newJump not in Tables.jump_table:
            raise Exception("wrong jump expression")
        self.newJump = Assembler.JumpBits()

    def GotAddress(self, addr):
        self.newAddress = addr

    def parse(self, line):
        self.newAddress = None
        self.newTarget = None
        self.newCommand = None
        self.newJump = None
        parsed = self.cmd.parseString(line)
        if self.newAddress is not None:
            result = Assembler.AddressInstruction(self.newAddress)
            return result
        if self.newCommand is not None:
            result = Assembler.ControlInstruction(self.newCommand, self.newTarget, self.newJump)
            return result


class testSymbolTable(unittest.TestCase):

    def setUp(self):
        self.table = SymbolTable()

    def testAdding(self):
        self.table.AddVariable("var1")
        assert(self.table.HasSymbol("var1"))
        assert(self.table.GetSymbolValue("var1") == 16)
        self.table.AddLabel("loop1", 5)
        assert(self.table.HasSymbol("loop1"))
        assert(self.table.GetSymbolValue("loop1") == 5)

    def testRepeatedAdd(self):
        self.table.AddVariable("var1")
        assert(self.table.HasSymbol("var1"))
        assert(self.table.GetSymbolValue("var1") == 16)
        self.assertRaises(Exception, self.table.AddVariable, "var1")

    def TestValueIncrement(self):
        self.table.AddVariable("var1")
        assert(self.table.HasSymbol("var1"))
        assert(self.table.GetSymbolValue("var1") == 16)
        self.table.AddVariable("var2")
        assert(self.table.HasSymbol("var2"))
        assert(self.table.GetSymbolValue("var2") == 17)
        self.table.AddVariable("var3")
        assert(self.table.HasSymbol("var3"))
        assert(self.table.GetSymbolValue("var3") == 18)
