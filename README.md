#yate
Yet Another Text Extrator: a small, simple command-line python tool for extracting data from raw text. Goal is to feed that data to search engines and graph databases.

It outputs a simple key/value list.

##How to use##
Yate receives text input, and according to the data points defined in the config file, extracts them and outputs them as key/value, in different formats.

The data point definitions are regexes (match, extract or multi-extract) or lambda functions that extract value(s) from the raw text.

##Tester##
**Yate** also includes a tester, which scans outgoing key/value pairs for missing or invalid values, which is meant for singling out documents which have parsing problems.

##Differ & Patcher##
These two tools make it possible to generate patches to do on-the-fly correction of texts with minor errors which make data points extraction troublesome. It works extactly like GNU diff & patch, although Google's diff-match-patch library is used, so it's entirely done in Python.


#TODO#

* Include more config examples in config\_default
* Review code to match common Python code conventions (I'm not that much of a Python programmer, yet)
* Include a working example and use case (Content I'm currently working on is not public)
* Reorganize code, external lib directory, executable scripts in root directory
* Better error handling, more options, ...
