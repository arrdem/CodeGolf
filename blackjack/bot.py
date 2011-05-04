#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       bot.py
#
#   LICENSE       
#       Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#   
#   ABOUT   
#       This software was developed for codegolf.stackexchange.com as 
#       part of a standard package for running the KOTH style AI 
#       challenges which I have enjoyed participating in.
#
#   DOCUMENTATION
#       class bot
#           Serves as a container which allows other code to more easily
#           run specific files as subprocesses with arguments.
#           Does some fancy footwork to build java, lisp and python code
#           into "compiled" form for improved runtime.
#           TODO:
#             - add support for c/c++ and java INSIDE OF bot instead of
#               using a seperate compiler routine.
#
#       buildBots(dir)
#           takes a string dir and returns a list of valid bots in that
#           directory.

class basic_bot:
    def __init__(self, filename):
        print "[!] CREATED BOT -", filename, "\t",
        self.filename = filename
        self.exec_code = self.__build__(os.path.splitext(filename))
        
    def __build__(self, a):
        base, ext = a
        if ext == '.py':
            py_compile.compile(self.filename)
            print 'compiled python '# + self.filename
            return ('%s %sc' %( PYTHON_PATH, self.filename))
        
        elif ext =='.lsp':
            # we mess with stdout/err here to suprress
            # the noisy output of clisp
            if subprocess.call([CLISP_PATH, '-c --silent', self.filename],stdout=subprocess.PIPE,stderr=subprocess.PIPE) == 0:
                print 'compiled lisp '# + self.filename
                return CLISP_PATH + " " + self.filename
          
        elif ext == '.java':
            if subprocess.call([JAVAC_PATH, self.filename]) == 0:
                print 'compiled java '# + self.filename
                classname = re.sub('\.java$', '', self.filename)
                classname = re.sub('/', '.', classname);
                return JAVA_PATH + " " + classname
        
        elif ext == '.class':
            # We assume further down in compilation and here that Java classes are in the default package
            classname = re.sub('.*[/\\\\]', '', self.filename)
            dir = self.filename[0:(len(self.filename)-len(classname))]
            if (len(dir) > 0):
                dir = "-cp " + dir + " "
            classname = re.sub('\\.class$', '', classname);
            print ""
            return JAVA_PATH + " " + dir + classname
        
        else:
            print ""
            return self.filename
        
    def run(self, history):
        process = subprocess.Popen(self.exec_code+" "+history,stdout=subprocess.PIPE,shell=True)
        return process.communicate()[0].strip().lower()
        
    def nicename(self, pad = True, padlen = 16):
        if pad:
            return string.center(os.path.splitext(os.path.split(self.filename)[1])[0], padlen)
        else:
            return os.path.splitext(os.path.split(self.filename)[1])[0]
