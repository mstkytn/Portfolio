import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('....')
cols = df.columns

print('HEAD::::::::::::::', df.head().to_string(), sep='\n')
print('COLS::::::::::::::', cols, sep='\n')
print('INFO::::::::::::::', df.info, sep='\n')
print('DESC::::::::::::::', df.describe(), sep='\n')
print('NULL::::::::::::::', df.isnull().sum(), sep='\n')
print('NUNI::::::::::::::', df.nunique(), sep='\n')

for col in cols:
    print(col, "variable' s distinct values :", df[col].unique())

# column formattings
df['cause'] = df['cause'].str.replace(" ", "")
df['cause'] = df['cause'].str.replace("vegetable", "VEGETABLES")
df['cause'] = df['cause'].str.upper()
df['claim_amount'] = df['claim_amount'].str.replace("R$ ", "", regex=False)
df.claim_amount = df.claim_amount.astype(float)
df.amount_paid = df.amount_paid.astype(float)

rval = ['error',
        df['time_to_close'].median(),
        df['claim_amount'].median(),
        df['amount_paid'].median(),
        'error',
        0,
        False,
        'UNKNOWN']

fna_rp_val = dict(zip(cols, rval))

for v in fna_rp_val:
    print(v, "-", fna_rp_val[v])

print(fna_rp_val)
df = df.fillna(value=fna_rp_val)

# print("Dataset after the cleansing and formatting \n", df.to_string())
# save the processed CSV
# df.to_csv("....")

column_details = ""
for col in df.columns:
    total_string = col + " column has " + str(len(df[col].unique())) + " unique values" + "\n" + str(df[col].unique())
    column_details = column_details + "\n" + total_string + "\n" + ".........................."

print(column_details)
print("Processed_Data :")
print('INFO::::::::::::::', '\n', df.info, '\n')
print('DESC::::::::::::::', '\n', df.describe().to_string(), '\n')
print('NULL::::::::::::::', '\n', df.isnull().sum(), '\n')
print('NUNI::::::::::::::', '\n', df.nunique(), '\n')

# correlations
correlations = df.corr(numeric_only=True)
print(correlations.to_string())

# /////////////////////////////////DATA VISUALIZATION//////////////////////////////
# LOCATION BAR GRAPH
vis1 = df[['claim_id', 'location']].groupby('location').count()
vis1 = vis1.sort_values(by='claim_id', ascending=False)
vis1['percent'] = vis1['claim_id'] / vis1['claim_id'].sum()
print(vis1)
ax = vis1.plot.bar(rot=0, legend=None)
ax.set_xlabel("Location")
ax.set_ylabel("Count")
plt.show()
# HISTOGRAM
vis3 = df['time_to_close']
ax3 = vis3.plot.hist(bins=80)
ax3.set_xlabel("Completion of Claims in days")
plt.show()
# BOX_PLOT
ax4 = df.plot.box(column="time_to_close", by="location", grid=False)
plt.title("Completion of Claims in days by Location")
print(df.groupby('location')['time_to_close'].median())
print(df.groupby('location')['time_to_close'].describe())
plt.show()
# BOX_PLOT-INNER_Q
ax51 = df.plot.box(column="time_to_close", by="location", ylim=[100, 250], grid=False)
plt.title("Completion of Claims in days by Location - The Inners")
plt.show()
# BOX_PLOT-OUTLIERS
ax5 = df.plot.box(column="time_to_close", by="location", ylim=[280, 600], grid=False)
plt.title("Completion of Claims in days by Location - The Outliers")
plt.show()
# BOX_PLOT_HUED_CAUSE
ax4c = sns.boxplot(data=df, x="location", y="time_to_close", hue="cause")
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.title("Completion of Claims in days by cause")
plt.show()
# SCATTER_CLAIM
sns.scatterplot(data=df, x="time_to_close", y="claim_amount")
plt.show()
# SCATTER_PAID
sns.scatterplot(data=df, x="time_to_close", y="amount_paid")
plt.show()
# SCATTER_CAUSE
sns.relplot(data=df, x="time_to_close", y="claim_amount", hue="individuals_on_claim", col="cause")
plt.show()
# SCATTER_LOCATION
sns.relplot(data=df, x="time_to_close", y="claim_amount", hue="individuals_on_claim", col="location")
plt.show()
