java -jar antlr.jar -o . -fo . MDXLexer.g MDXParser.g MDXTree.g

python MDXTree.py --lexer=MDXLexer --parser=MDXParser --parser-rule=mdx_statement --rule=stuff --encoding=utf8 select.mdx
