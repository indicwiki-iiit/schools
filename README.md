This directory contains two python notebooks which are mainly used for visualising the data while testing some features and a "src" directory which is the main codebase for writing articles ! 

##'curDir' Directory

This directory contains the codebase for the new model, converting knowledge base to intermediate structured article (dataframe of labeled article sentences) which can be modified and updated by users and then converting this data to XML page which can be imported in mediawiki.

###Files:
-**write.py**
	Generates an article and its title by rendering the jinja templates given a school's data !

-**oneMakeDataframe.py** 
	constructs an article(s) for a given list of school code(s) and then segments and structures each article, then this structured data is stored in a dataframe which is pickled as **articleParts.pkl** in the data folder. 

-**twoGenXML.py** 
	generates the XML file from the previously constructed dataframe !

Rest of the files are auxilary files.