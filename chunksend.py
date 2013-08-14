import sublime
import sublime_plugin
import os
import subprocess
import string
import re
#import Rtools

class KnitrSendChunkCommand(sublime_plugin.TextCommand):
    
  def run(self, view): # runs on command
    initial_selection = self.view.sel()[0]
    # Find all chunks
    for region in self.view.find_all('(?<=>>=\n)((.*\n)+?)(?=@)'):
        if region.contains(initial_selection.a):
            chunk_range = sublime.Region(region.a, region.b-1)
            break
    else:
        chunk_range = None

    # print("cur chunk is", chunk_range)
    # to capture the chunk as a string: 
    # self.view.substr(cur_chunk[0])
    # print(self.view.sel()[0].begin() )

    # the self.view.sel() method returns, essentially a nested list (called an
    # object of class RegionSet -- which is  a collection of regions). So the
    # part that is [0] indexes the first region in the region set (which is, of
    # course, the only region in the region set), and the '.begin()' call gets
    # the starting point for the region.
    
    # print(self.view.sel()[0].a # this line does the same, but uses the (for)
    # our purposes here) synonymous term 'a'

    if not chunk_range:
        return

    # Add selection
    self.view.sel().add(chunk_range)    

    # Run command from Enhanced-R
    self.view.run_command('r_send_select') 
    
    # Restore initial selection
    self.view.sel().subtract(chunk_range)
    self.view.sel().add(initial_selection)
    self.view.show(initial_selection.a)

class KnitrNextChunkCommand(sublime_plugin.TextCommand):

    def run(self,edit):
        init_sel = int(self.view.sel()[0].a)
        mysel=self.view.find_all('(?<=>>=\n)((.*\n)*?)(?=@)')
        cur_chunk = []
        chunk_number = []
        print(range(0,len(mysel),1))
        for sel in range(0,len(mysel),1):
            if mysel[sel].b> self.view.sel()[0].a<mysel[sel].a:
                cur_chunk.append(mysel[sel])
                chunk_number.append(sel)
                break

        if cur_chunk != []:
            self.view.show(cur_chunk[0].a)
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(cur_chunk[0].a))
            print("there are ", len(mysel),"chunks, you are at chunk:" ,chunk_number[0])
        else:
            print("there are ", len(mysel),"chunks, you are at chunk:" ,len(mysel))
            print("end of file reached with no more chunks")

        return

class KnitrPrevChunkCommand(sublime_plugin.TextCommand):

    def run(self,edit):
        init_sel = int(self.view.sel()[0].a)
        mysel=self.view.find_all('(?<=>>=\n)((.*\n)*?)(?=@)')
        cur_chunk = []
        chunk_number = []
        print(range(len(mysel)-1,-1,-1))
        for sel in range(len(mysel)-1,-1,-1):
            if mysel[sel].b< self.view.sel()[0].a>mysel[sel].a:
                cur_chunk.append(mysel[sel])
                chunk_number.append(sel)
                break
                
        if cur_chunk != []:
            self.view.show(cur_chunk[0].a)
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(cur_chunk[0].a))
            print("there are ", len(mysel),"chunks, you are at chunk:" ,chunk_number[0])
        else:
            print("there are ", len(mysel),"chunks, you are at chunk:" , 1)
            print("start of file reached with no more chunks")

            return