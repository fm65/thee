#!/usr/bin/env python3

from distutils.core import setup

setup(
	name='thee',
	version='1.0',
	description='THE simple python key bindings  Editor',
    long_description=open('README.md').read(),
	author='Fidel R. Monteiro',
	py_modules= [
		"findwindow",
		"highlighter",
		"linenumbers",
		"textarea",
		"texteditor",
		"syntax",
        "config",
        "terminal",
        "interactiveConsole"
    ],
	entry_points = {
		"console_scripts": ["thee = texteditor:main"]	
	},
    license="",
)
 
