#yate
Yet Another Text Extrator: a small, simple command-line python tool for extracting data from raw text. Goal is to feed that data to search engines and graph databases.

It outputs a simple key/value list.

##How to use##
Yate receives text input, and according to the data points defined in the config file, extracts them and outputs them as key/value, in different formats.

The data point definitions are regexes (match, extract or multi-extract) or lambda functions that extract value(s) from the raw text.


##Tester##
**Yate** also includes a tester, which scans outgoing key/value pairs for missing or invalid values, which is meant for singling out documents which have parsing problems.

