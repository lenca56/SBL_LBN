#importing packages
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def int_to_str(number):
    """
    function that converts integer of at most 3 digits to str of exactly 3 digits

    params:
    -------
    number: int
        3 digit number between (001 and 115)
    returns
    -------
    string: str
        3 digit string converted
    """
    if (number < 1 or number >999):
        raise Exception('number is outside 3 digit range or is 0')

    string = str(number)
    while len(string) != 3:
        string = '0' + string
    return string

# will require Path object
def check_exist(dyad, subject, path=None):
    """
    constructing function that creates path name based on inputs while also checking if the file already exists

    params:
    -------
    dyad: int
        number between 1 and 115 inclusively (possible dyad numbers)
    subject: str
        'Demo' or 'Observer'
    returns
    -------
    
    """
    # path to work in
    path = Path("/Users/lencacuturela/Desktop/Research/github/SBL_LBN/data") if path is None else path

    # checking that particular dyad is a valid option
    if (dyad<1 or dyad>115):
        raise Exception('Dyad number not within range (1,115) inclusively')

    # checking that particular object is a valid option
    if (subject != "Demo" and subject!= "Observer"):
        raise Exception('subject can only be "Demo" or "Observer"')

   
    # create a string of the file name to look for
    fname = f"DLC-Output_Dyad_{int_to_str(dyad)}_{subject}.csv"
    # determine what directory to look for the file in 
    full_path = path / fname

    # return if it exists or not
    return full_path.exists(), full_path

def load_and_wrangle(dyad, subject, path=None, overwrite=False):

    """
    Function for loading & cleaning DLC output .csv file

    params:
    -------
    dyad: int
        number between 1 and 115 inclusively (possible dyad numbers)
    subject: str
        'Demo' or 'Observer'
    overwrite : bool, default=True
        whether to save out and overwrite previous filtered .csv

    returns
    -------
    df : pandas dataframe
    """
            
    # path to work in
    path = Path("/Users/lencacuturela/Desktop/Research/github/SBL_LBN/data") if path is None else path
    
    exists, full_path = check_exist(dyad=dyad, subject=subject, path=path)
    
    if exists and overwrite==False:
        print("loading from previously created file")
        df = pd.read_csv(full_path)
        return df
    
    else:
        print("loading from DLC output")
    
        # hyperparameter column names from dLC 
        col_names = ["Nose.x","Nose.y","Nose.p","Right_before_eye.x","Right_before_eye.y","Right_before_eye.p","Right_before_ear.x",
        "Right_before_ear.y","Right_before_ear.p","Right_after_ear.x","Right_after_ear.y","Right_after_ear.p","Left_before_eye.x","Left_before_eye.y",
        "Left_before_eye.p","Left_before_ear.x","Left_before_ear.y","Left_before_ear.p","Left_after_ear.x","Left_after_ear.y","Left_after_ear.p",
        "Skeleton_1.x","Skeleton_1.y","Skeleton_1.p","Skeleton_2.x","Skeleton_2.y","Skeleton_2.p","SKeleton_3.x","SKeleton_3.y","SKeleton_3.p",
        "Tail.x","Tail.y","Tail.p", "Right_side_3.x","Right_side_3.y","Right_side_3.p","Right_side_tail.x","Right_side_tail.y","Right_side_tail.p",
        "Left_side_3.x","Left_side_3.y","Left_side_3.p","Left_side_tail.x","Left_side_tail.y","Left_side_tail.p"]
        
        # taking not filtered??!
        array = np.genfromtxt(path / f"Dyad_{int_to_str(dyad)}_Emotional_Contagion_{subject}DLC_resnet_101_Emotional_Contagion_NetworkJun10shuffle3_1030000_filtered.csv", delimiter=',', skip_header = 3, skip_footer=1)
        print(array.shape)
        df = pd.DataFrame(array[:,1:], columns=col_names)

        # save out
        df.to_csv(full_path, index = False)
        
        return df
