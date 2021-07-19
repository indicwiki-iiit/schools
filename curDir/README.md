This directory contains the codebase for the new model, converting knowledge base to intermediate structured article (dataframe of labeled article sentences) which can be modified and updated by users and then converting this data to XML page which can be imported in mediawiki.

###Files:
-**write.py**
	Generates an article and its title by rendering the jinja templates given a school's data !

-**zeroMain.py** 
	constructs an article(s) for a given list of school code(s) and then segments and structures each article, then this structured data is stored in a dataframe which is pickled as **articleParts.pkl** in the data folder. Also, it constructs an xml file for the give school code(s).

Rest of the files are auxilary files.

###To Run:
1. Modify the oneMakeDataframe file to include the udise school's codes you want articles for and run the following command to generate a dataframe with the school's sentences you want to show in the interface
>python oneMakeDataframe.py

2. To generate a XML file, which can be directly imported into tewiki. Run the following command
>python twoGenXML.py
