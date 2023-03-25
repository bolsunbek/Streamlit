import yfinance as yf
import streamlit as st



st.write("""
## Bioinformatics Project - Computational Drug Discovery [Part 1] Download Bioactivity Data
this we will be building a real-life data science project that you can include in your data science portfolio. Particularly, we will be building a machine learning model using the ChEMBL bioactivity data.

In Part 1, we will be performing Data Collection and Pre-Processing from the ChEMBL Database.

### ChEMBL Database

The ChEMBL Database is a database that contains curated bioactivity data of more than 2 million compounds. It is compiled from more than 76,000 documents, 1.2 million assays and the data spans 13,000 targets and 1,800 cells and 33,000 indications. [Data as of March 25, 2020; ChEMBL version 26].

### Installing libraries

Install the ChEMBL web service package so that we can retrieve bioactivity data from the ChEMBL Database.

""")


st.write("""
### Importing libraries
""")
# Import necessary libraries
import pandas as pd
from chembl_webresource_client.new_client import new_client

st.write("""
 Search for Target protein

Target search for Acetylcholinesterase
""")

# Target search for coronavirus
target = new_client.target
target_query = target.search('acetylcholinesterase')
targets = pd.DataFrame.from_dict(target_query)
targets


selected_target = targets.target_chembl_id[0]
selected_target

st.write("""
Here, we will retrieve only bioactivity data for Human Acetylcholinesterase (CHEMBL220) that are reported as pChEMBL values.


""")

activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")
df = pd.DataFrame.from_dict(res)
df

st.write("""
Finally we will save the resulting bioactivity data to a CSV file bioactivity_data.csv.
""")

df.to_csv('acetylcholinesterase_01_bioactivity_data_raw.csv', index=False)

st.write("""
### Handling missing data
If any compounds has missing value for the standard_value and canonical_smiles column then drop it.
""")


df2 = df[df.standard_value.notna()]
df2 = df2[df.canonical_smiles.notna()]
df2

st.write("""
Apparently, for this dataset there is no missing data. But we can use the above code cell for bioactivity data of other target protein.
""")

st.write("""
### Data pre-processing of the bioactivity data

""")

st.write("""
### Labeling compounds as either being active, inactive or intermediate
""")

st.write("""
The bioactivity data is in the IC50 unit. Compounds having values of less than 1000 nM will be considered to be active while those greater than 10,000 nM will be considered to be inactive. As for those values in between 1,000 and 10,000 nM will be referred to as intermediate.
""")

bioactivity_class = []
for i in df2.standard_value:
  if float(i) >= 10000:
    bioactivity_class.append("inactive")
  elif float(i) <= 1000:
    bioactivity_class.append("active")
  #else:
  #  bioactivity_class.append("intermediate")

st.write("""
### Combine the 3 columns (molecule_chembl_id,canonical_smiles,standard_value) and bioactivity_class into a DataFrame
""")

selection = ['molecule_chembl_id','canonical_smiles','standard_value']
df3 = df2[selection]
df3

bioactivity_class = pd.Series(bioactivity_class, name='bioactivity_class')
df4 = pd.concat([df3, bioactivity_class], axis=1)
df4

st.write("""
## Saves dataframe to CSV file
""")

df4.to_csv('wangli_bioactivity_data_preprocessed.csv', index=False)
     
