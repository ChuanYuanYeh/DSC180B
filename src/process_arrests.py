# Import libraries/modules
import pandas as pd
import os

# Global constants
RACE_MAP = {'B': 'Black or African American','H': 'Hispanic or Latino','O': 'Other','W': 'White','A': 'Asian','K': 'Asian','F': 'Asian','V': 'Asian','G': 'Native Hawaiian and Other Pacific Islander','C': 'Asian','X': 'Other','P': 'Native Hawaiian and Other Pacific Islander','S': 'Native Hawaiian and Other Pacific Islander','J': 'Asian','I': 'American Indian and Alaska Native','U': 'Native Hawaiian and Other Pacific Islander','L': 'Asian','Z': 'Asian','D': 'Asian'}

TYPE_MAP = {'D': 'Dependent', 'F': 'Felony', 'I': 'Infraction', 'M': 'Misdemeanor', 'O': 'Other'}

PERSONAL = ['Aggravated Assault', 'Prostitution/Allied', 'Sex (except rape/prst)', 'Other Assaults', 'Homicide', 'Weapon (carry/poss)', 'Against Family/Child', 'Non-Criminal Detention', 'Rape', ]

PROPERTY = ['Robbery', 'Burglary', 'Larceny', 'Receive Stolen Property', 'Vehicle Theft', ]

INCHOATE = ['Gambling', 'Pre-Delinquency']

STATUTORY = ['Liquor Laws','Driving Under Influence', 'Miscellaneous Other Violations', 'Disorderly Conduct', 'Drunkeness', 'Narcotic Drug Laws', 'Disturbing the Peace', 'Moving Traffic Violations', 'Federal Offenses']

# Main driver functions
def process_arrests(inpath, outpath, cols, title='arrests', **kwargs):
    print('Processing Arrests data.')
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    print('Reading raw data.')
    try:
        arrests = transform_arrests(pd.read_csv(inpath).drop(columns=['Unnamed: 0']), cols)
    except:
        arrests = transform_arrests(pd.read_csv(inpath), cols)
    name = os.path.join(outpath, '{}-processed.csv'.format(title))
    print('Exporting as csv.')
    arrests.to_csv(name, index=False)
    print('Downloaded: {}'.format(name))
    
# Helper methods
def get_pred(row):
    # check year
    yr = row.loc['Year']
    if yr < 2013:
        return 'No PredPol'
    elif yr >= 2015:
        return 'PredPol'
    else:
        # check area
        ar = row.loc['Area Name']
        areas = ['North Hollywood', 'Southwest', 'Foothill']
        if ar in areas:
            return 'PredPol'
        else:
            return 'No PredPol'
        
def crm_category(x):
    try:
        if any(substring in x for substring in INCHOATE):
            return 'Inchoate'
        elif any(substring in x for substring in PROPERTY):
            return 'Property'
        elif any(substring in x for substring in PERSONAL):
            return 'Personal'
        elif any(substring in x for substring in STATUTORY):
            return 'Statutory'
        return 'Financial/Other'
    except TypeError:
        return 'Financial/Other'

def limit_cols(df, cols):
    return df[cols]

def transform_arrests(df, cols):
    print('Processing Arrests data.')
    df['Arrest Date'] = pd.to_datetime(df['Arrest Date'])
    df['Year'] = df['Arrest Date'].apply(lambda x: x.year)
    df['Descent Code'] = df['Descent Code'].map(RACE_MAP)
    df['Charge Group Description'] = df['Charge Group Description'].apply(crm_category)
    df['Arrest Type Code'] = df['Arrest Type Code'].map(TYPE_MAP)
    df['predPol Deployed'] = df.apply(get_pred, axis=1)
    df['Total'] = pd.Series([1] * df.shape[0])
    return limit_cols(df, cols)
