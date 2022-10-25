import numpy as np
import pandas as pd
from datetime import date, timedelta

# IMPORT CSV
csv = pd.read_csv('https://raw.githubusercontent.com/yellowslides/charts/main/2022charts.csv')

# GLOBAL VARIABLES
chartNumbers = csv.chart.unique()
startDate = date(2022, 1, 6)

# CREATE DICTIONARY OF 2022 ALBUMS
twentyTwoChartsDict = {elem : pd.DataFrame() for elem in chartNumbers}
for key in twentyTwoChartsDict.keys():
    twentyTwoChartsDict[key] = csv[:][csv.chart == key]

# RETURN CHART BY CHART CODE  
def chartByChartCode(chartCode):
  return twentyTwoChartsDict[chartCode]

# RETURN DATE OF CHART BY CHART CODE AS STRING
def dateByChartCode(chartCode):
  return (startDate + timedelta(weeks=(int((chartCode)-1)%100))).strftime('%m/%d/%Y') 

# RETURN LIST OF DATES OF CHARTS BY CHART CODES
def datesByChartNumbers(listOfCodes):
  listOfDates = []
  for i in listOfCodes:
    listOfDates.append(dateByChartCode(i))
  return listOfDates

# INSERT LIST OF DATES TO A DATAFRAME BY CHART CODES
def insertDateList(df, listOfCodes):
  return df.insert(0, 'date', datesByChartNumbers(listOfCodes))

# RESET INDEX ON A DATAFRAME
def resetIndex(df):
  df.insert(0, '#', np.arange(1, len(df)+1)) 
  df.set_index('#', inplace=True)
  return df


#####

# RETURN DATAFRAME OF #1 SONGS
def numberOnes():
  df = csv[csv.position == 1].filter(['title', 'artist'])
  insertDateList(df, chartNumbers)
  return resetIndex(df)

# RETURN DATAFRAME OF TOP *NUM* SONGS ON CHART IN WEEKS
def mostWeeks(num):
  df = csv[['title','artist']].value_counts()[:num].reset_index()
  df.columns = ['song', 'artist', 'weeks'] # fix rename method?
  return resetIndex(df)

# RETURN LENGTH OF LONGEST SEQUENCE OF ASCENDING NUMBERS IN A LIST
def longestAscendingSequence(list):
  currentSequence = 1
  maxSequence = 1
  currentNumber = 0
  maxNumber = 0
  for i in range(1, len(list)):
    if (list[i-1] == list[i]-1):
      currentSequence += 1
      currentNumber = list[i]      
    else:
      currentSequence = 1
    if (currentSequence > maxSequence):
      maxSequence = currentSequence
      maxNumber = currentNumber
  return (maxSequence, maxNumber)

# RETURN DATAFRAME OF MOST CONSECUTIVE WEEKS ON CHART
def mostConWeeks(num):
  df = mostWeeks(num*2)
  listOfWeeks = []
  for index, row in df.iterrows():
    conWeeks, lastDate = longestAscendingSequence((csv.loc[(csv['title'] == row['song']) 
        & (csv['artist'] == row['artist'])])['chart'].tolist())
    df.iloc[index - 1, 2] = conWeeks
    listOfWeeks.append(dateByChartCode(lastDate-(conWeeks-1)) + " - " + dateByChartCode(lastDate))
  df['dates of run'] = listOfWeeks
  return resetIndex(df.nlargest(num, 'weeks'))
