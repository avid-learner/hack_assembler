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
        self.operations.append(op)

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
                    #print(op.address)
                    if not self.table.HasSymbol(op.GetAddress()):
                        raise Exception("Symbol not found!")
                    op.SetAddress(self.table.GetSymbolValue(op.GetAddress()))

    def ToBinary(self):
        text = ""
        for instr in self.operations:
            text += (instr.ToBitString()+"\n")
        return text

class testProgram():
    def testLabels(self):
        p = Program()
        p.AddLabel("loop")
        p.AddOperation(Assembler.AddressInstruction(56))
        assert(p.table.HasSymbol("loop"))
        assert(p.table.GetSymbolValue("loop") == 0)
        p.AddOperation(Assembler.AddressInstruction("loop"))
        p.ReplaceSymbols()
        text = p.ToBinary()
        print(text)


class Parser:
    def __init__(self):
        from pyparsing import Literal, CaselessLiteral, Word, OneOrMore, ZeroOrMore, \
        Forward, NotAny, delimitedList, oneOf, Group, Optional, Combine, alphas, nums, restOfLine, cStyleComment, \
        alphanums, printables, empty, quotedString, ParseException, ParseResults, Keyword, cppStyleComment, FollowedBy
        self.a_line = "@" + (Word(alphas+"_.$", alphanums+"_.$") | Word(nums)).setParseAction(lambda s,l,t: self.GotAddress(t))
        self.command = Word("ADM-+10|&!").setParseAction(lambda s,l,t: self.GotCommand(t))
        self.dest_clause = Optional(";" + Word("JLPNGEQTM").setParseAction(lambda s,l,t: self.GotJump(t)))
        self.target_clause = (Optional(Word("AMD") + "=").setParseAction(lambda s,l,t: self.GotTarget(t)))
        self.c_line_t = self.target_clause + self.command + self.dest_clause
        self.c_line_nt = self.command + self.dest_clause
        self.c_line = self.c_line_t | self.c_line_nt
        self.label = "(" + Word(alphas+"_.$", alphanums+"_.$").setParseAction(lambda s,l,t: self.GotLabel(t)) + ")"
        self.comment = cppStyleComment
        self.cmd = self.a_line | self.c_line | self.label
        self.oneline = (self.cmd + Optional(self.comment)) | self.comment
        self.newAddress = None
        self.newTarget = None
        self.newCommand = None
        self.newJump = None
        self.newLabel = None

    def GotCommand(self, cmd):
        self.newCommand = cmd[0]
        #print(cmd)
        if self.newCommand not in Tables.comp_table:
            raise Exception("wrong compute expression")
        self.newCommand = Assembler.InstructionBits(self.newCommand)


    def GotLabel(self, trg):
        #print(trg)
        l = Assembler.Label("".join(trg))
        self.newLabel = l

    def GotTarget(self, trg):
        self.newTarget = trg[0]
        #print(trg)
        if self.newTarget not in Tables.dest_table:
            raise Exception("wrong target expression")
        self.newTarget = Assembler.DestinationBits("A" in trg[0], "D" in trg[0], "M" in trg[0])

    def GotJump(self, jmp):
        self.newJump = jmp[0]
        #print(jmp)
        if self.newJump not in Tables.jump_table:
            raise Exception("wrong jump expression")
        self.newJump = Assembler.JumpBits()
        if "G" in jmp[0]:
            self.newJump.AddJ3()
        if "E" in jmp[0]:
            self.newJump.AddJ2()
        if "N" in jmp[0]:
            self.newJump.RemoveJ2()
        if "L" in jmp[0]:
            self.newJump.AddJ1()
        if "P" in jmp[0]:
            self.newJump.AddJ1()
            self.newJump.AddJ2()
            self.newJump.AddJ3()

    def GotAddress(self, addr):
        self.newAddress = "".join(addr)
        if self.newAddress.isdigit():
            self.newAddress = int(self.newAddress)

    def Parse(self, line):
        self.newAddress = None
        self.newTarget = None
        self.newCommand = None
        self.newJump = None
        self.newLabel = None
        parsed = self.oneline.parseString(line)
        if self.newAddress is not None:
            result = Assembler.AddressInstruction(self.newAddress)
            return result
        elif self.newCommand is not None:
            #print(self.newCommand.Expression)
            if self.newTarget is None:
                self.newTarget = Assembler.DestinationBits()
            if self.newJump is None:
                self.newJump = Assembler.JumpBits()
            result = Assembler.ControlInstruction(self.newCommand, self.newTarget, self.newJump)
            return result
        elif self.newTarget is not None:
            cmd = self.newTarget.ToPlainStr()
            self.newCommand = Assembler.InstructionBits(cmd)
            self.newTarget = Assembler.DestinationBits()
            if self.newJump is None:
                self.newJump = Assembler.JumpBits()
            result = Assembler.ControlInstruction(self.newCommand, self.newTarget, self.newJump)
        elif self.newLabel is not None:
            result = self.newLabel
            return result
        else:
            return None

    def ParseFile(self, fileName):
        inFile = open(fileName, "r")
        p = Program()
        for line in inFile:
            r = self.Parse(line)
            if type(r) is Assembler.Label:
                p.AddLabel(r.name)
            elif r is not None:
                p.AddOperation(r)
        p.FillSymbolTable()
        p.ReplaceSymbols()
        inFile.close()
        return p


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
