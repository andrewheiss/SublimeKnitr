# KnitrSublime

This package provides basic LaTeX support for `knitr` in Sublime Text 2. It comes with:

* A language definition for `knitr` files
* The following snippets (configurable in `sublime-keymap` file):
	* Insert `knitr` chunk: `⌥⌘C`
	* Send current chunk to R GUI: `⌘⇧^R` *(requires [R Tools](https://github.com/karthikram/Rtools); R 3.0 includes a single binary, so there is no need to call R64.app. Modify `Rtools.py` to run R instead of R64)*
	* Move between chunks: `⌘⇧,` and `⌘⇧.`
* A disabled-by-default build system that only works with Skim on OS X; lacks ability to sync with Skim (only included for legacy purposes)
* Instructions on how to patch the LaTeXTools package to knit and typeset `.Rnw` files (use instead of the disabled build system)


## Patch for LaTeXTools

Some advantages to using LaTeXTools is that you can specify any PDF viewer, change the TeX engine, and sync the PDF with the text editor. If you want to use the highly robust LaTeXTools plugin, you need to patch two files to make the standard LaTeXTools build system knit and typest the `.Rnw` file.

Make these three changes (*huge* thanks to [Heberto del Rio](http://stackoverflow.com/a/15017303/120898) for this!):

**Important:** *Copying and pasting code from GitHub can do unexpected things to indentation and can temporarily break LaTeXTools. Make sure the indentation is correct after pasting.*

### File 1: `Packages/LaTeX/LaTeX.tmLanguage`

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

### File 2: `Packages/LaTeXTools/makePDF.py`

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

### File 3: `Packages/LaTeXTools/jumpToPDF.py`

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
