# KnitrSublime

This package provides *very rudimentary* LaTeX support for `knitr` in Sublime Text 2. It comes with:

* A language definition for `knitr` files
* A build system (only works with Skim on OS X; lacks ability to sync with Skim)
* A snippet for inserting a `knitr` chunk (currently bound to ⌥⌘C, but configurable)

## To do

Ideally, for the sake of cross-platformness and robustness, the build system for LaTeX should be handled by the LaTeXTools package, which is far more mature than my simple build-and-force-open-in-Skim system (e.g. you can specify any PDF viewer, change the TeX engine, sync the PDF with the text editor, etc.). However, [I have yet to find a good way](http://stackoverflow.com/questions/14152004/access-a-build-system-from-another-build-system-in-sublime-text-2) to call a build system from inside another build system (that is, call the LaTeXTools build system from this one after running `knitr`). 

This should maybe eventually be merged with other `knitr`-related packages like [knitr_reports](https://github.com/nachocab/knitr_reports) to make a comprehensive Sublime Text plugin that can handle Markdown, LaTeX, and HTML.
