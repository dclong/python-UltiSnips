## python-UltiSnips

python-UltiSnips is a tool written in Python 
for automatically generating UltiSnips snippets 
by parsing help documentation of programming languages.
It focus on the auto-complete functionality.


## Examples

### Scala
seq.txt is a text file by copying and pasting the help page of Seq. 
Please refer to snippets/scala/seq.txt for example.
```
./ui.py -p 'def |val ' -t '' -f seq.txt
```
