# KnitrSublime

This package provides basic LaTeX support for `knitr` in Sublime Text 2. It comes with:

* A language definition for `knitr` files
* A snippet for inserting a `knitr` chunk (currently bound to ⌥⌘C, but configurable)
* A disabled-by-default build system that only works with Skim on OS X; lacks ability to sync with Skim (only included for legacy purposes)
* Instructions on how to patch the LaTeXTools package to knit and typeset `.Rnw` files (use instead of the disabled build system)


## Patch for LaTeXTools

Some advantages to using LaTeXTools is that you can specify any PDF viewer, change the TeX engine, and sync the PDF with the text editor. If you want to use the highly robust LaTeXTools plugin, you need to patch two files to make the standard LaTeXTools build system knit and typest the `.Rnw` file.

Make the following changes (*huge* thanks to [Heberto del Rio](http://stackoverflow.com/a/15017303/120898) for this!):

### File 1: `Packages/LaTeXTools/makePDF.py`

Find this:

	if self.tex_ext.upper() != ".TEX":
		sublime.error_message("%s is not a TeX source file: cannot compile." % (os.path.basename(view.file_name()),))
		return

And replace with this:

	if (self.tex_ext.upper() != ".TEX") and (self.tex_ext.upper() != ".RNW"):
		sublime.error_message("%s is not a TeX or Rnw source file: cannot compile." % (os.path.basename(view.file_name()),))
		return

Then find this:

	os.chdir(tex_dir)
	CmdThread(self).start()
	print threading.active_count()

And replace with this:

	os.chdir(tex_dir)
	if self.tex_ext.upper() == ".RNW":
		# Run Rscript -e "library(knitr); knit('" + self.file_name + "')"
		os.system("Rscript -e \"library(knitr); knit('"+ self.file_name +"')\"")
		self.file_name = self.tex_base + ".tex"
		self.tex_ext = ".tex"
	CmdThread(self).start()
	print threading.active_count()

(If you want to use `Sweave` instead of `knitr`, change the `Rscript` command accordingly.)

### File 2: `Packages/LaTeXTools/jumpToPDF.py`

Find this:

	if texExt.upper() != ".TEX":
		sublime.error_message("%s is not a TeX source file: cannot jump." % (os.path.basename(view.fileName()),))
		return

And replace with this:

	if (texExt.upper() != ".TEX") and (texExt.upper() != ".RNW"):
		sublime.error_message("%s is not a TeX or Rnw source file: cannot jump." % (os.path.basename(view.fileName()),))
		return

## To do

This should maybe eventually be merged with other `knitr`-related packages like [knitr_reports](https://github.com/nachocab/knitr_reports) to make a comprehensive Sublime Text plugin that can handle Markdown, LaTeX, and HTML.
