import pandas as pd

df_location = 0
reimbursement_data = pd.DataFrame(columns=['Date Received','Date Processed','Date Disbursed','Method','Employee Name','First Name','Last Name','Team','Business Purpose','Amount','Processed?','Region','Account Code','Trinet Codes','Tax Year Incurred','Notes'])

# Load the Data
df = pd.read_csv('./IK12 Dummy Data - Sunil - Reimbursement (Dummy Data).csv')

# Function to get the unique Business Purpose and corresponding data
def get_purpose(location):
  purposes = {}

  for i in range(1,11):
    if df.loc[location,f'Purpose {i}'] not in purposes:
      purposes[df.loc[location,f'Purpose {i}']] = [df.loc[location,f'Date Received'],\
                                            df.loc[location,f'Date Processed'],\
                                            df.loc[location,f'Date Disbursed'],\
                                            df.loc[location,f'subject_name'],\
                                            df.loc[location,f'Team'],\
                                            df.loc[location,f'Cost {i}'],\
                                            df.loc[location,f'Region'],\
                                            df.loc[location,f'Acct Code {i}'],\
                                            df.loc[location,f'Trinet ID'],\
                                            df.loc[location,f'Tax Year Incurred'],\
                                            df.loc[location,f'Notes']]
    else:
      purposes[df.loc[location,f'Purpose {i}']][5] += df.loc[location,f'Cost {i}']

  return purposes


# Function to populate the Final table
def fill_rows(location, df_location, business_purpose, value):
  reimbursement_data.loc[location, 'Date Received'] = value[0]
  reimbursement_data.loc[location, 'Date Processed'] = value[1]
  reimbursement_data.loc[location, 'Date Disbursed'] = value[2]
  reimbursement_data.loc[location, 'Method'] = 'Payroll'

  f_name = value[3].split(' ')[0]
  l_name = value[3].split(' ')[1]
  emp_name = f'{l_name}, {f_name}'

  reimbursement_data.loc[location, 'Employee Name'] = emp_name
  reimbursement_data.loc[location, 'First Name'] = f_name
  reimbursement_data.loc[location, 'Last Name'] = l_name
  reimbursement_data.loc[location, 'Team'] = value[4]
  reimbursement_data.loc[location, 'Amount'] = value[5]
  reimbursement_data.loc[location, 'Region'] = value[6]
  reimbursement_data.loc[location, 'Account Code'] = value[7]
  reimbursement_data.loc[location, 'Trinet Codes'] = value[8]
  
  reimbursement_data.loc[location, 'Tax Year Incurred'] = value[9]
  reimbursement_data.loc[location, 'Notes'] = value[10]
  reimbursement_data.loc[location, 'Business Purpose'] = business_purpose
  
  return True


# Loop through the data to extract and post
for i in range(len(df)):
  purposes = get_purpose(i)
  for key, value in purposes.items():
    business_purpose = key
    print(key, value, df_location)
    fill_rows(len(reimbursement_data), df_location, key, value)
    df_location += 1

reimbursement_data.to_csv('./Converted Reimbursement.csv', sep=',')