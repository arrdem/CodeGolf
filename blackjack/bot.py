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
#       buildBots(dir, dir)
#           takes as arguments the paths of the source and binary
#           folders. Itterates through /source building bots to /binary.
#           Then itterates through /binary, testing each file for sanity
#           and returning a list of all bots.
#           TODO
#             - A SINGLE INSANE BOT TAKES DOWN THE ENTIRE INTERPRETER.
#               Now. That may be by design, but the system should still
#               be improved to provide a way for class bot to commit 
#               suicide if the target binary isn't sane.

####    CONFIG
PYTHON_PATH     = '/usr/bin/python' # path to python executable
CLISP_PATH      = '/usr/bin/clisp'  # path to clisp executable
JAVAC_PATH      = '/usr/bin/javac'  # path to java compiler
JAVA_PATH       = '/usr/bin/java'   # path to java vm

####    DEPENDS
import subprocess 
import os
import sys
import random
import py_compile
import itertools
import multiprocessing
import string
import re

#### CLASSES
class bot:
    def __init__(self, filename):
        print "[!] CREATED WARRIOR -", filename, "\t",
        self.filename = filename
        self.exec_code = self.__build__(os.path.splitext(filename))
        self.__test__()
        #print "\t", self.exec_code
        
    def __build__(self, a):
        base, ext = a
        if ext == '.py':
            py_compile.compile(self.filename)
            print 'compiled python '
            return ('%s %sc' %( PYTHON_PATH, self.filename))
        
        elif (ext in ('.lsp', '.lisp')):
            if subprocess.call([CLISP_PATH, '-c --silent', self.filename],stdout=subprocess.PIPE,stderr=subprocess.PIPE) == 0:
                print 'compiled lisp '
                return CLISP_PATH + " " + self.filename
            else:
                self.__die__()
          
        elif ext == '.java':
            if subprocess.call([JAVAC_PATH, self.filename]) == 0:
                print 'compiled java '
                classname = re.sub('\.java$', '', self.filename)
                classname = re.sub('/', '.', classname);
                return JAVA_PATH + " " + classname
            else:
                self.__die__()
        
        elif ext == '.class':
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
            
    def __call__(self):
        self.__test__()
    
    def __test__(self):
        process = subprocess.Popen(self.exec_code+" ",stdout=subprocess.PIPE,shell=True)
        
    def __die__(self):
        print "\n[!] FATAL ERROR IN (", self.nicename(pad = False), ") - ABORTING CONTEST"
        exit(1)
        
    def run(self, history):
        process = subprocess.Popen(self.exec_code+" "+history,stdout=subprocess.PIPE,shell=True)
        return process.communicate()[0].strip().lower()
        
    def nicename(self, pad = True):
        if pad:
            return string.center(os.path.splitext(os.path.split(self.filename)[1])[0], 20)
        else:
            return os.path.splitext(os.path.split(self.filename)[1])[0]

####    FUNCTIONS

def buildBots(bots_dir, src_dir, botType = bot):
    if (os.path.isdir(bots_dir) and os.path.isdir(src_dir)):
            for foo in os.listdir(src_dir):
                filename = os.path.split(foo)[-1]
                base, ext = os.path.splitext(filename)
                
                if ext in ('.c','.cpp'):
                    print "[!] COMPILING ", foo, 
                    subprocess.call(["gcc", "-o", bots_dir + "/" + base, "./src/" + foo])
                    print ", DONE!"
                
                elif (ext == '.java'):
                    print "[!] COMPILING ", foo,
                    subprocess.call([JAVAC_PATH, "-d ."+bots_dir, "./src/" + foo])
                    print ", [DONE]"
                
                else:
                    print "No compiler registered for ", foo
                
            print "\nFinding bots in " + bots_dir
            players = [bots_dir+"/"+exe for exe in os.listdir(bots_dir) if (os.access(bots_dir+"/"+exe,os.X_OK) or os.path.splitext(exe)[-1] == '.class')]
            
            for i,p in enumerate(players):
                players[i] = botType(p)
    else:
        print "[!] ERROR - FILESYSTEM IS WRONG - FIX SOURCE OR MOVE TARGETS"
        exit(1)
        
    print "\n"
    return players
