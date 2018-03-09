# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 13:34:40 2018

@author: someone
"""

from pyparsing import Word, alphas
greet = Word( alphas ) + "," + Word( alphas ) + "!" # <-- grammar defined here
hello = "Hello, World!"
print (hello, "->", greet.parseString( hello ))

