import io
import pandas as pd

DF_CODES = pd.read_csv(io.StringIO('''
Account Code,Trinet
7100,25
7110,25
7140,
7440,25
7441,25
7530,24
'''), header=0)

DF_CODES['Trinet'] = DF_CODES['Trinet'].astype('Int64')


def get_codes(category):
  my_value = category
  try:
    tri_code = DF_CODES.loc[DF_CODES["Account Code"] == my_value]['Trinet'].values[0]
  except:
    tri_code = 'NaN'
  return tri_code


# Function to get the corresponding fields for each employee based on Category
def mg_get_accounts(df, location):
  accounts = {}

  for i in range(1,9):

    if df.loc[location,f'Account Code {i}'] not in accounts:
      trinet_code = get_codes(df.loc[location,f'Account Code {i}'])
      accounts[df.loc[location,f'Account Code {i}']] = [df.loc[location,f'Date Submitted'],\
                                            df.loc[location,f'Date Processed'],\
                                            df.loc[location,f'Date Disbursed'],\
                                            df.loc[location,f'Employee Name'],\
                                            df.loc[location,f'Team'],\
                                            df.loc[location,f'Due {i}'],\
                                            df.loc[location,f'Region'],\
                                            trinet_code,\
                                            df.loc[location,f'Tax Year Incurred'],\
                                            df.loc[location,f'Notes'],\
                                            df.loc[location,f'Purpose {i}']]
    else:
      accounts[df.loc[location,f'Account Code {i}']][5] += df.loc[location,f'Due {i}']

  return accounts

# Function to fill in the final table
def mg_fill_rows(mileage_data, location, df_location, key, value):
  mileage_data.loc[location, 'Date Received'] = value[0]
  mileage_data.loc[location, 'Date Processed'] = value[1]
  mileage_data.loc[location, 'Date Disbursed'] = value[2]
  mileage_data.loc[location, 'Method'] = 'Payroll'

  # First Last name split
  f_name = value[3].split(',')[1]
  l_name = value[3].split(',')[0]

  mileage_data.loc[location, 'Employee Name'] = value[3]
  mileage_data.loc[location, 'First Name'] = f_name
  mileage_data.loc[location, 'Last Name'] = l_name
  mileage_data.loc[location, 'Team'] = value[4]
  mileage_data.loc[location, 'Amount'] = value[5]
  mileage_data.loc[location, 'Region'] = value[6]
  mileage_data.loc[location, 'Trinet Codes'] = value[7]

  mileage_data.loc[location, 'Tax Year Incurred'] = value[8]
  mileage_data.loc[location, 'Notes'] = value[9]
  mileage_data.loc[location, 'Business Purpose'] = value[10]
  mileage_data.loc[location, 'Account Code'] = key

  return mileage_data
