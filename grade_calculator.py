import pandas as pd

# Read the CSV file
final_student_grades = pd.DataFrame()
df = pd.read_csv('student_grades.csv')
# Combine "FIRST" and "LAST" columns into a single "FULL NAME" column
df['FULL_NAME'] = df['FIRST'] + ' ' + df['LAST']

# Drop the "FIRST" and "LAST" columns if you no longer need them
df = df.drop(['FIRST', 'LAST'], axis=1)

# Reorder the columns with the last column as the first column
df = df[['FULL_NAME'] + [col for col in df.columns if col != 'FULL_NAME']]

# Create a new column with class average
df['CLASS_AVERAGE'] = df[['EXAM_1_GRADE','EXAM_2_GRADE','EXAM_3_GRADE','EXAM_4_GRADE']].mean(axis=1)

#Create a new column to calculate GPA
df['GPA'] = df[['FULL_NAME', 'CLASS_AVERAGE']].groupby(['FULL_NAME']).transform('mean')
# print(df)

#Create filter out the common names and create the classes are columns with the values in the rows
df = df.pivot(index=['FULL_NAME', 'GPA'], columns='CLASS', values='CLASS_AVERAGE').reset_index().rename_axis(None)
print(df)
# print(s.unstack(level=0))
# print(df)

# Save the updated DataFrame to a new CSV file
# df.to_csv('final_student_grades.csv', index=False)
# print(df.pivot_table(index='FULL NAME', columns='CLASS', values='CLASS_AVERAGE'))


