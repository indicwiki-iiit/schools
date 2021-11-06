# Schools

Schools is one of the domains, which is a part of the IndicWiki Project.

## Description

The aim of this domain is to create a large number of articles (about 1 lakh) about schools across the states of Andhra Pradesh and Telangana. This domain has potential because of the importance of relevant information pertaining to schools, which would assist parents in making informed decisions about the education of their children. Hence, we are generating these data-rich articles in telugu for about 1 lakh schools, and uploading them to wikipedia, so that people who can read only in their native language (here, telugu) can benefit from this information.

## Installation and setup

Create virtual environment in the project folder using the following commands.

```bash
$ pip install virtualenv
$ pip install python3.7 
$ virtualenv -p python3.7 schEnv
```
After the successful creation of virtual environment (venv), clone the repository or download the zip folder of the project and extract it. Run the following commands from the schools (root) directory to activate the virtual environment and install all necessary dependencies.

```bash
$ source schEnv/bin/activate
$ pip install -r requirements.txt
```
requirements.txt comes along with the Project Directory. 

## Guide to generate XML dump, articles for different schools

- Clone the repository into the local system.
- Enter the 'curDir' folder inside the cloned repo.
- Execute the file zeroMain.py with the help of command: `python3 zeroMain.py <code_start_index> <code_end_index>`, where `code_start_index` and `code_end_index` correspond to the row numbers of the first and last desired articles (only serial order is possible). For example `python3 zeroMain.py 30 50` would generate xml dump for schools in rows 30-50 (inclusive). By default, dump is generated for all schools (case where no command line arguments are provided, such as `python3 zeroMain.py`).
- On executing the above command, different parts of article are written to an `articleParts.csv` file (as a dataframe), xml dump is obtained in `onePage.xml`, titles of given set of schools is obtained as a dataframe in `title.csv`, any errors encountered are logged in `error.txt`. If command line arguments were passed, names of these files would have the range passed in their filenames (such as `onePage30-50.xml` etc).


## Github Structure

The folder curDir contains the entire implementation corresponding to article generation. This directory contains the codebase for the new model, converting knowledge base to intermediate structured article (dataframe of labeled article sentences) which can be modified and updated by users and then converting this data to XML page which can be imported in mediawiki. 

It can be found [here](https://github.com/indicwiki-iiit/schools/tree/main/curDir). All the below explained files and folders are inside this directory.



### data

> Github folder Link: https://github.com/indicwiki-iiit/schools/tree/main/curDir/data
- This folder contains various datasets (final and intermediate), and the implementations as to how they were obtained. The python scripts in this folder are described as follows:
	- _mergeDuplicates.py_ -> The number of rows were found to be more than the number of unique schools, because of repetitions caused due to a school having multiple instruction mediums. This script removes all duplicate rows with same school codes and replaces the 'Medium' column's value with list of all mediums associated with the respective school code.
	- _unify\_pkls.py_ -> This script unifies all the pickles given in a folder into one pickle file. (Assumes the given folder contains a pickle named DISTRICTS, which is a pickle of a list of all file names in the given folder.)
	- _process\_xlsx.py_ -> This script reads all the excel sheets in scraped_xlsx, filters & normalises them, concatenates them to allScraped.pkl and finally computes intersection of new data with halfDB.pkl and adds this intersection to oneKB.pkl
	- _readFreqTokens.py_ -> This script cleans up frequently occurring english tokens and their corresponding telugu translation, and stores them.
	- _readyCodes.py_ -> This script selects school udise codes which do not have duplicate school names, i.e, it selects codes for which articles can be generated.
- The pickle files and datasets in this folder are described as follows:
	- _halfDF.pkl_ -> This is the pickle file of a dataframe consisting of all records from excel sheet provided by Praveen Sir (the unified version of pickle files in 'excelDB\_pkls folder).
	- _allScraped.pkl_ -> This is the pickle file of a dataframe consisting of all records from excel sheet which was scraped from udise website (these records are in Unified 'scraped_xlsx' folder).
	- _errors.pkl_ -> This pickle file corresponds to the dataframe of all schools which have to be manually checked, because of some discrepancies in their entries.
	- _oneKB.pkl_ -> This pickle file corresponds to the dataframe consisting of all error free records from both halfDB.pkl and allScraped.pkl. Further, it is updated everytime new records are added into allScraped.pkl. 
	- _readyCodes.pkl_ -> This pickle file consists of school udise codes which do not have duplicate school names (articles can be generated for these).
	- _freqTokens.csv_ -> This file consists of the dataframe which comprises of translation and frequency for every english token in the dataset.
	- _freqTokens.pkl_ -> This pickle file consists of the same dataframe mentioned above, in .pkl format for easy loading.
	- _tokens.csv_ -> This file consists of various english tokens (in englisg) and their corresponding frequencies in csv format (for machine generated translation).
- The sub-folders present inside this folder are explained below:
	- _epoch_ -> This folder contains article parts, xml dump and titles for all 21k school articles generated based on oneKB.pkl.
	- _trials_ -> This folder was used just for testing purposes, generating articles for few schools to check functioning of template and xml generation implementation.
	- _excelDB\_pkls_ -> This folder consists of all pickles of dataframes, one per district, extracted from the excel sheet given by Praveen Sir. One pickle file named 'DISTRICTS', which contains list of all districts pertaining to different school records, is also present in the excel sheet.
	- _processed\_xlsx_ -> This folder consists of excel sheets which are already cleaned and concatenated to allScraped.pkl.
	- _scraped\_xlsx_ -> This folder consists of raw scraped data in form of excel sheets (district-wise).
	- _titles\_translation_ -> This folder consists of implementation for creating a proper one-one tokenwise mapping from english to telugu, given a reviewed dataframe of english school titles and their corresponding telugu translation. The code can be found in `create_title_dict.py`, and the english token - telugu token translation can be found in `titleTokens` files. Some edge cases for which one-one mapping cannot be achieved are logged in `edgeCases-titleTokens` files.

### scrape_new_data

> Github folder Link: https://github.com/indicwiki-iiit/schools/tree/main/curDir/scrape_new_data
- This folder contains implementation and datasets corresponding to newly scraped data from schools.org.in. The python scripts in this folder are described as follows:
	- _data\_cleaning.py_ -> This file contains implementation which handles basic data cleaning, such as making missing values uniform, identifying edge cases and removing unwanted attributes.
	- _extract\_info.py_ -> This file contains the actual scraping implementation for scraping the complete data for all schools in Andhra Pradesh and Telangana. Similar to `zeroMain.py`, this file can be provided with command line arguments for scraping data for a particular subsegment of schools. For example `python3 extract_info.py 30 50` would scrape data for schools in rows 30-50 in intermediate dataframe `schools_id_name_url_dataframe.pkl` (inclusive). By default, data is scraped for all schools (case where no command line arguments are provided, such as `python3 extract_info.py`).
	- _extract\_urls.py_ -> This file contains implementation for web crawling and obtaining, storing urls for each school from the two states, so as to minimize overhead while actually scraping content from them.
	- _notability\_check.py_ -> This file filters out non-sparse rows (well populated rows) and stores them separately, as these can be highlighted while generating articles.
- The pickle files and datasets of this folder are described as follows:
	- _school\_urls\_dict.pkl_ -> This file consists of a dictionary, where school UDISE codes are the keys and that school's url in the above website is the corresponding value.
	- _schools\_id\_name\_url\_dataframe.pkl_ -> This pickle file consists of an intermediate dataframe, where each row contains a school's UDISE code, its corresponding name, and its url in schools.org.in. 
	- _schools\_id\_name\_url\_dataframe.xlsx_ -> This excel file consists of the same intermediate dataframe above, in excel format.
	- _schools\_org\_data.xlsx_ -> This excel file contains the complete dataset for all the data scraped from all the schools.
	- _schools\_org\_data\_part\_i.pkl_ -> These 3-part pickle files contain the same information as in excel file above, but have been split to 3 parts due to size constraints.
	- _notable\_schools\_org\_data.pkl_ -> This pickle file consists of data corresponding to notable schools alone (about 14% of the total data collected - for the states Andhra Pradesh and Telangana).
	- _notable\_schools\_org\_data.xlsx_ -> This excel file consists of the same dataframe above, in excel format.
	- _translated\_dataset\_notable\_schools.pkl_ -> This dataset consists of all attributes which require translation while rendering in articles. There are about 15 such attributes and their corresponding english and telugu versions are present here (summing up to 30). Note that these were collected only for notable schools.
	- _translated\_dataset\_notable\_schools.xlsx_ -> This excel file consists of the same dataframe above, in excel format.

### template

> Github folder Link: https://github.com/indicwiki-iiit/schools/tree/main/curDir/template
- This folder .
	- _new\_teluguDFtext.j2_ -> This file consists of the improved template to generate wikitext provided a school's data, corresponding to latest dataset (from schools.org.in)
	- _teluguDFtext.j2_ -> This file consists of the template to generate the wikitext of a given school's data (based on old dataset - oneKB)
	- _teluguTitle.j2_ -> This jinja2 template file generates the title for a given school.

### createMgnt.py

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/createMgnt.py
- This file contains implementation which generates a dataframe where each row contains a school's managament details in english and its corresponding translation in telugu.

### getJsData.py

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/getJsData.py
- This file contains implementation which stores the data for each school (its title, code) in .js format in provided path.

### help.py

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/help.py
- This file contains implementation of pre-processing and more convenient translation for frequently occuring words, phrases and numbers etc.

### onePage.xml

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/onePage.xml
- This file contains how a sample xml dump might look for a particular school.

### schoolXML5k_1.xml

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/schoolXML5k_1.xml
- This file contains how a sample xml dump might look for a multiple school articles in the same xml file.

### template\_functions.py

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/template_functions.py
- This file contains various python functions which are used in edge case handling (different sentences based on attributes available) while rendering the article from template based on data provided.

### trans.py

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/trans.py
- This file contains implementation which deals with translation, transliteration of attributes along with string cleaning (with the help of regular expressions and libraries like anuvaad, deeptranslit) and exception handling.

### transNNP.py

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/transNNP.py
- This file acts a helper file for `trans.py` and assists in translation of english tokens.

### write.py

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/write.py
- This file contains implementation which generates an article and its title by rendering the jinja templates, given a particular school's data.

### create\_translated\_dataset.py

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/create_translated_dataset.py
- This script generates a translated dataset for all notable schools, including all attributes which require translation while rendering in articles (there are about 15 such english attributes).

### merge\_translated\_dataset.py

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/merge_translated_dataset.py
- This script merges the translated dataset (once its reviewed) with the original dataset, to avoid on-the-fly translation.

### zeroMain.py

> Github file Link: https://github.com/indicwiki-iiit/schools/blob/main/curDir/zeroMain.py
- This file constructs article(s) for a given list of school code(s) and then segments and structures each article. It constructs an xml file for the given school code(s). (More details are explained in the section 'Guide to generate XML dump')


### Sample Article

You can find the sample article [here](https://docs.google.com/document/d/1zx1IG2G8MDLfH21ofY1Z8AEoV-bv2KEe8bbjNDWFsxc/edit)

