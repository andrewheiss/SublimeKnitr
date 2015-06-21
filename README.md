# Sublime knitr

* Version: 1.2.2
* Date: January 30, 2015

This package provides [**knitr**](http://yihui.name/knitr/) Markdown and LaTeX support in Sublime Text 2 and 3. It comes with:

* Language definitions for **knitr** LaTeX and Markdown files
* A build system for R Markdown files.
* The following commands (available via the command palette and with keyboard shortcuts):
	* Insert **knitr** chunk snippet: `super+alt+c`
	* Move between chunks: `super+alt+,` and `super+alt+.`
	* Send chunk to R GUI: `super+b` *(requires [Enhanced-R](https://github.com/randy3k/Enhanced-R))*
	
By default, `ctrl` is used in place of `super` on Windows and Linux.


## Dependencies

In order to use all the features of this package, you'll need to install two other packages. Both are easily installable via Package Control:

* [Enhanced-R](https://github.com/randy3k/Enhanced-R)
* [LaTeXing](http://www.latexing.com/) or [LaTeXTools](https://github.com/SublimeText/LaTeXTools) (see patch below for LaTeXTools)

The easiest way to use this plugin is to use [LaTeXing](http://www.latexing.com/), especially since development on LaTeXTools has slowed significantly. Simply enable the `knitr` setting and adjust the command in `knitr_command` if required. 

Alternatively, you can use this plugin with [LaTeXTools](https://github.com/SublimeText/LaTeXTools), with three manual patches, listed below. 


## Building R Markdown files

Building an `.Rmd` file creates an `.md` file in the same directory. It's up to you to use that file elsewhere (i.e. use Pandoc to convert it `.html`, `.docx`, `.rtf`, or even `.tex` if you feel like being extra circuitous).

There is also a build variant that will create an HTML file from the knitted Markdown file. Use this with `super + shift + b`. 

I typically build the `.Rmd` file once, open the resulting `.md` file in [Marked](http://markedapp.com/), and then leave it open in Marked as I make further changes and newer builds. 

Alternatively, you can force the build system to open the resulting `.md` file in the default program for Markdown files by changing the `"cmd":` line in `knitr-Markdown.sublime-build` to:

		"cmd": [ "Rscript -e \"library(knitr); knit('$file_name')\"; open $file_base_name.md" ],


## Unicode and other encoding issues

Working with non-ASCII characters in plots is a little tricky because of how LaTeX and R differently support Unicode. Here's are some general guidelines for fixing character encoding issues:

1. Add `LANG=en_US.UTF-8` to `~/.Renviron` (create this file if needed). This will ensure that R runs with Unicode support whenver it opens.
2. Add a separate chunk near the beginning of your document with this: `pdf.options(encoding = '<encoding>')`, where `encoding` is any of those listed in the output of this command: `list.files(system.file('enc', package = 'grDevices'))`. Choose an encoding that encompasses all the characters you're using in your plots.
3. If using `.Rnw` and LaTeX, ensure that `\usepackage[utf8]{inputenc}` is in your preamble.


## Roadmap and wish list

* Better Markdown syntax highlighting, including Multimarkdown and Pandoc extras like footnotes, tables, and citations.
* Create commands for Pandoc conversion from R Markdown to other formats? (or maybe just use actual Pandoc packages for that). 

------------

### Manual patch for LaTeXTools

If you want to use the LaTeXTools plugin, you need to patch three files to make the standard LaTeXTools build system knit and typest the `.Rnw` file. Make these three changes (*huge* thanks to [Heberto del Rio](http://stackoverflow.com/a/15017303/120898) for this!):

**Important:** *Copying and pasting code from GitHub can do unexpected things to indentation (replacing tabs with spaces) and can temporarily break LaTeXTools. Make sure the indentation is correct after pasting.*

#### File 1: `Packages/LaTeX/LaTeX.tmLanguage`

Add `Rnw` to the list of accepted LaTeX file types, like so:

	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
		<key>fileTypes</key>
		<array>
			<string>tex</string>
			<string>Rnw</string>
		</array>

**Instructions for Sublime Text 3**: In ST3, default packages are hidden deep within ST itself and are difficult to access, let alone edit. However, you can still get to `LaTeX.tmLanguage` relatively easily if you install the [PackageResourceViewer plugin](https://github.com/skuroda/PackageResourceViewer). After installing it, run the "PackageResourceViewer: Open Resource:" command through the command pallete (command/ctrl + shift + p) and navigate to LaTeX.tmLanguage. After making changes, ST will save a copy of the file in a more accessible location (`Packages/LaTeX/LaTeX.tmLanguage`), overriding the default built-in file. 

#### File 2: `Packages/LaTeXTools/makePDF.py`

Find this:

	if self.tex_ext.upper() != ".TEX":
		sublime.error_message("%s is not a TeX source file: cannot compile." % (os.path.basename(view.file_name()),))
		return

And replace with this:

	if (self.tex_ext.upper() != ".TEX") and (self.tex_ext.upper() != ".RNW"):
		sublime.error_message("%s is not a TeX or Rnw source file: cannot compile." % (os.path.basename(view.file_name()),))
		return

Then find this:

	# We should now be able to construct the builder object
	self.builder = builder_class(self.file_name, self.output, builder_settings, platform_settings)

And replace with this:

	if self.tex_ext.upper() == ".RNW":
		# Run Rscript -e "library(knitr); knit('" + self.file_name + "')"
		os.system("Rscript -e \"library(knitr); knit('"+ self.file_name +"')\"")
		self.file_name = self.tex_base + ".tex"
		self.tex_ext = ".tex"

	# We should now be able to construct the builder object
	self.builder = builder_class(self.file_name, self.output, builder_settings, platform_settings)

(If you want to use `Sweave` instead of `knitr`, change the `Rscript` command accordingly.)

#### File 3: `Packages/LaTeXTools/jumpToPDF.py`

Find this:

	if texExt.upper() != ".TEX":
		sublime.error_message("%s is not a TeX source file: cannot jump." % (os.path.basename(view.fileName()),))
		return

And replace with this:

	if (texExt.upper() != ".TEX") and (texExt.upper() != ".RNW"):
		sublime.error_message("%s is not a TeX or Rnw source file: cannot jump." % (os.path.basename(view.fileName()),))
		return

#### File 4: `Packages/LaTeXTools/viewPDF.py`

Find this:

	if texExt.upper() != ".TEX":
		sublime.error_message("%s is not a TeX source file: cannot view." % (os.path.basename(view.fileName()),))
		return

And replace with this:

	if (texExt.upper() != ".TEX") and (texExt.upper() != ".RNW"):
		sublime.error_message("%s is not a TeX or Rnw source file: cannot view." % (os.path.basename(view.fileName()),))
		return


If you want to be able to use multiple files and to find your bib file, you'll also need to change the following files:
#### File 5: `Packages/LaTeXTools/getTeXRoot.py`

Find this:

	mroot = re.match(r"%\s*!TEX\s+root *= *(.*(tex|TEX))\s*$",line)

And replace with this:

	mroot = re.match(r"%\s*!TEX\s+root *= *(.*(tex|rnw))\s*$",line, flags=re.IGNORECASE)

#### File 6: `Packages/LaTeXTools/latex_cite_completions.py`

Find this:

	if src[-4:].lower() != ".tex":

And replace with this:

	if src[-4:].lower() not in [".tex",".rnw"]:

    
