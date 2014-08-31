#wikitodict

This little script takes a Wikipedia article title and returns a
Python dictionary based on that article's infobox.

##Usage
Simply place the wikitodict module in your project directory and
use like so:

```python
import wikitodict
cheers = wikitodict.search('Cheers')
cheers['genre']
u'Sitcom'
cheers['num_seasons']
u'11'
cheers['opentheme']
u'"Where Everybody Knows Your Name" <br />Performed by Gary Portnoy'
```

##Issues
This is about as quick and dirty as it gets. 

* No error handling to speak of.
* Results are still a little 'dirty' with html elements and user
comments present in many dictionary values.
* Not all key value pairs make sense. For example, the dictionary
for 'Barack Obama' contains the key 'blank1' with the value
'Awards' and the key 'data1' with the value 'Nobel Peace Prize'.
A much better result would be an entry with the key 'Awards' and
the value 'Nobel Peace Prize'.
