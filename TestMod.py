import Parser
import Assembler
import Tables

def testLabels():
        p = Parser.Program()
        p.AddLabel("loop")
        p.AddOperation(Assembler.AddressInstruction(56))
        assert(p.table.HasSymbol("loop"))
        assert(p.table.GetSymbolValue("loop") == 0)
        p.AddOperation(Assembler.AddressInstruction("loop"))
        p.ReplaceSymbols()
        text = p.ToBinary()
        print(text)

def testFile(fileName, outFileName):
    p = Parser.Parser()
    program = p.ParseFile(fileName)
    print(program.ToBinary())
    print(program.table.table)
    outf = open(outFileName, "w")
    outf.write(program.ToBinary())

if __name__ == "__main__":
    #testFile("test.asm", "test.hack")
    #testFile("add\Add.asm", "Add.hack")
    testFile("max\MaxL.asm", "MaxL.hack")
    testFile("pong\Pong.asm", "PongN.hack")
    testFile("max\Max.asm", "Max.hack")
    #testFile("pong\PongL.asm", "PongL.hack")
    testFile("rect\Rect.asm", "Rect.hack")
    #testLabels()
