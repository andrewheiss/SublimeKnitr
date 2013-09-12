import sublime
import sublime_plugin
import os
import subprocess
import string
import re

class KnitrSendChunkCommand(sublime_plugin.TextCommand):
    
  def run(self, view): # runs on command
    initial_selection = self.view.sel()[0]

    if self.view.match_selector(0, "text.tex.latex.knitr"):
        for region in self.view.find_all('(?<=>>=\n)((.*\n)+?)(?=@)'):
            if region.contains(initial_selection.a):
                chunk_range = sublime.Region(region.a, region.b-1)
                break
        else:
            chunk_range = None

    elif self.view.match_selector(0, "text.html.markdown.knitr"):
        for region in self.view.find_all('(?<=\}\n)((.*\n)+?)(?=```)'):
            if region.contains(initial_selection.a):
                chunk_range = sublime.Region(region.a, region.b-1)
                break
        else:
            chunk_range = None

    else:
        chunk_range = None

    if not chunk_range:
        return

    # Add selection
    self.view.sel().add(chunk_range)  

    print("send chunk:\n%s" % self.view.substr(chunk_range))  

    # Run command from Enhanced-R
    self.view.run_command('r_send_select') 
    
    # Restore initial selection
    self.view.sel().subtract(chunk_range)
    self.view.sel().add(initial_selection)
    self.view.show(initial_selection.a)


class KnitrNextChunkCommand(sublime_plugin.TextCommand):

    def run(self,edit):
        initial_selection = self.view.sel()[0]

        # Find next chunk
        if self.view.match_selector(0, "text.tex.latex.knitr"):
            for region in self.view.find_all('(?<=>>=\n)((.*\n)+?)(?=@)'):
                if region.b > initial_selection.a < region.a:
                    chunk_range = region
                    break
            else:
                chunk_range = None

        elif self.view.match_selector(0, "text.html.markdown.knitr"):
            for region in self.view.find_all('(?<=\}\n)((.*\n)+?)(?=```)'):
                if region.b > initial_selection.a < region.a:
                    chunk_range = region
                    break
            else:
                chunk_range = None

        else:
            chunk_range = None

        if chunk_range:
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(chunk_range.a))
            self.view.show(chunk_range.a)
        else:
            print("end of file reached with no more chunks")


class KnitrPrevChunkCommand(sublime_plugin.TextCommand):

    def run(self,edit):
        initial_selection = self.view.sel()[0]

        # Find previous chunk
        if self.view.match_selector(0, "text.tex.latex.knitr"):
            for region in self.view.find_all('(?<=>>=\n)((.*\n)+?)(?=@)')[::-1]:
                if region.b < initial_selection.a > region.a:
                    chunk_range = region
                    break
            else:
                chunk_range = None

        elif self.view.match_selector(0, "text.html.markdown.knitr"):
            for region in self.view.find_all('(?<=\}\n)((.*\n)+?)(?=```)')[::-1]:
                if region.b < initial_selection.a > region.a:
                    chunk_range = region
                    break
            else:
                chunk_range = None

        else:
            chunk_range = None
                
        if chunk_range:
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(chunk_range.a))
            self.view.show(chunk_range.a)
        else:
            print("start of file reached with no more chunks")
