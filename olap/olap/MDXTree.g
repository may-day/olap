tree grammar MDXTree;

options {
  // We're going to process an AST whose nodes are of type CommonTree.
  ASTLabelType = CommonTree;
    language = Python;

  // We're going to use the tokens defined in
  // both our MathLexer and MathParser grammars.
  // The MathParser grammar already includes
  // the tokens defined in the MathLexer grammar.
  tokenVocab = MDXParser;
}

/*
@members {
	#cids = []
}
*/

@main{

def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    import antlr3
    import antlr3.constants
    FileStream = antlr3.ANTLRFileStream
    class CaseInsensitiveFileStream(FileStream):
        def LA(self, i):
            if i==0:
                return 0 # undefined
        
            if i<0 :
                i+=1 # e.g., translate LA(-1) to use offset 0
        
 
 	    try:
                return ord(unichr(self.data[self.p+i-1]).upper())
            except IndexError:
                return antlr3.constants.EOF
    
    from antlr3.main import WalkerMain
    class MyWalker(WalkerMain):
        def execute(self, argv):
   	    antlr3.ANTLRFileStream = CaseInsensitiveFileStream
   	    super(MyWalker, self).execute(argv)
   	    
    main = MyWalker(MDXTree)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)

}

stuff
	:	 ^(SELECTSTMT x=axis_specification_list? y=cube_specification ) { print $x.text, $y.text ; }
	;

axis_specification_list
	:	^(AXESPEC .*) ;
cube_specification
	:	^(CUBESPEC .*);
	
