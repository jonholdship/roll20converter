# Roll20 Converter
A quick python script to convert from the output of Giffyglyph's Monster Maker to the Roll20 format.

## Usage
 - Edit main.py so ```input_file``` points to your Monster Maker output and ```output_file``` points to your desired output
 - ```input_type``` should equal custom or quickstart depending on your Monster Maker settings
 - run ```python main.py```


## To Do
 - quickstart is not yet supported.
 - Not all data is output from Monster maker, things like proficiency can be deduced from the monster level but aren't put into the json. As a result, skills and saving throws are incorrect and attacks may be missing data.