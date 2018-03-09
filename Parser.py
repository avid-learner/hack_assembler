import unittest


class SymbolTable:

    def __init__(self, startingValue=16):
        self.table = {}
        self.nextValue = startingValue

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
