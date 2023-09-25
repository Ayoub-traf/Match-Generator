# How to run


## Steps

- Make sure the python is installed
- Install requirements in the folder Test_models using "pip install -r requirements.txt"

##  Test models

To test models, we can run this example of commands : 
![382717240_1771902153243726_6030898185192001056_n](https://github.com/Ayoub-traf/Match-Generator/assets/76260962/e172cfcf-ec5b-48bd-8a3b-722f1aef1401)

The match duration (time) must be greater than 0 and less than or equal to 120.

- python main.py --time 15 --style defending
- python main.py --time 90 --style attacking
- python main.py --time 30 --style balanced --output ./your-folder/your-file.json

If --output not specified, the result will be saved in generated_match.json in the Test_models folder.

## Notebook

Here is the link of the notebook used for data analytics and model training :

https://colab.research.google.com/drive/1m8Ic4T-q62RKHLM5UlAngsnfr4_CATLD
