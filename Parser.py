
class SymbolTable:

    def __init__(self):
        self.table = {}
        self.nextValue = 16;

    def AddVariable(self, name):
        if name in self.table:
            raise Exception("Symbol already exists!");
        self.table[name] = self.FindNewValue();

    def HasSymbol(self, name):
        return name in self.table

    def AddLable(self, name, address):
        if name in self.table:
            raise Exception("Label already exists!");
        self.table[name] = address

    def GetSymbolValue(self, name):
        if not name in self.table:
            raise Exception("Symbol not found!");
        return self.table[name]

    def FindNewValue(self):
        result = self.nextValue;
        self.nextValue += 1;
        return result;

import unittest

class testSymbolTable(unittest.TestCase):

    def setUp(self):
        self.table = SymbolTable();

    def testAdding(self):
        self.table.AddVariable("var1");
        assert(self.table.HasSymbol("var1"));
        assert(self.table.GetSymbolValue("var1") == 16);
        self.table.AddLable("loop1", 5);
        assert(self.table.HasSymbol("loop1"));
        assert(self.table.GetSymbolValue("loop1") == 5);

    def testRepeatedAdd(self):
        self.table.AddVariable("var1");
        assert(self.table.HasSymbol("var1"));
        assert(self.table.GetSymbolValue("var1") == 16);
        self.assertRaises(Exception, self.table.AddVariable, "var1")
