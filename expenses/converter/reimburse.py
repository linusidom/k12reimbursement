import io
import pandas as pd

DF_CODES = pd.read_csv(io.StringIO('''
Category,Account Code,Trinet Code
Travel and Entertainment,7100,25
Travel and Entertainment:Travel,7110,25
Travel and Entertainment:Meals - Internal,7120,25
Travel and Entertainment:Travel Meals - Clients,7130,25
Facility and Office Expense:Shipping and Delivery Expense,7380,23
Facility and Office Expense:Charitable Contributions,7395,24
Team Morale,7400,24
Team Morale:Team Events,7420,24
Team Morale: Company Events,7421,24
Team Morale: Regional Ambassadors,7422,24
Team Morale: Social Committees,7423,24
Team Morale:Gifts,7430,24
Team Morale:Meetings Travel,7440,25
Team Morale: Regional Event Travel,7441,25
Team Morale: Employee Appreciation,7451,24
Team Morale:Employee Perks,7460,24
Team Morale:Remote Work Supplies,7480,23
Marketing & Sales Expense:Advertising,7520,24
Marketing & Sales Expense:Conference/Event Fees,7530,24
Marketing & Sales Expense:Client Relations,7580,24
Marketing & Sales Expense:Client collateral,7581,23
'''), header=0)

DF_CODES['Trinet Code'] = DF_CODES['Trinet Code'].astype('Int64')

def GET_CODES(category):
  my_value = category

  try:
    act_code = DF_CODES.loc[DF_CODES["Category"] == my_value]['Account Code'].values[0]
    tri_code = DF_CODES.loc[DF_CODES["Category"] == my_value]['Trinet Code'].values[0]

  except:
    act_code = 'NaN'
    tri_code = 'NaN'
  return act_code, tri_code


# Function to get the corresponding fields for each employee based on Category

def rb_get_category(df, location):
  categories = {}

  for i in range(1,11):

    if df.loc[location,f'Category {i}'] not in categories:
      codes = GET_CODES(df.loc[location,f'Category {i}'])
      categories[df.loc[location,f'Category {i}']] = [df.loc[location,f'Date Received'],\
                                            df.loc[location,f'Date Processed'],\
                                            df.loc[location,f'Date Disbursed'],\
                                            df.loc[location,f'Employee Name'],\
                                            df.loc[location,f'Team'],\
                                            df.loc[location,f'Cost {i}'],\
                                            df.loc[location,f'Region'],\
                                            codes[0],\
                                            codes[1],\
                                            df.loc[location,f'Tax Year Incurred'],\
                                            df.loc[location,f'Notes'],\
                                            df.loc[location,f'Purpose {i}']]
    else:
      categories[df.loc[location,f'Category {i}']][5] += df.loc[location,f'Cost {i}']

  return categories

  
# Function to fill in the final table
def rb_fill_rows(reimbursement_data, location, df_location, business_purpose, value):
  reimbursement_data.loc[location, 'Date Received'] = value[0]
  reimbursement_data.loc[location, 'Date Processed'] = value[1]
  reimbursement_data.loc[location, 'Date Disbursed'] = value[2]
  reimbursement_data.loc[location, 'Method'] = 'Payroll'

  # First Last name split
  f_name = value[3].split(',')[1]
  l_name = value[3].split(',')[0]

  reimbursement_data.loc[location, 'Employee Name'] = value[3]
  reimbursement_data.loc[location, 'First Name'] = f_name
  reimbursement_data.loc[location, 'Last Name'] = l_name
  reimbursement_data.loc[location, 'Team'] = value[4]
  reimbursement_data.loc[location, 'Amount'] = value[5]
  reimbursement_data.loc[location, 'Region'] = value[6]
  reimbursement_data.loc[location, 'Account Code'] = value[7]
  reimbursement_data.loc[location, 'Trinet Codes'] = value[8]

  reimbursement_data.loc[location, 'Tax Year Incurred'] = value[9]
  reimbursement_data.loc[location, 'Notes'] = value[10]
  reimbursement_data.loc[location, 'Business Purpose'] = value[11]

  return reimbursement_data