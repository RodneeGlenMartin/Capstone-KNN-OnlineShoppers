import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

df = pd.read_csv('online_shoppers_intention.csv')

print("=" * 70)
print("DATASET OVERVIEW")
print("=" * 70)
print(f"Total sessions: {len(df)}")
print(f"Total features: {df.shape[1] - 1}")
print(f"Memory used: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")

print("\n" + "=" * 70)
print("1. CLASS DISTRIBUTION (Revenue)")
print("=" * 70)
class_counts = df['Revenue'].value_counts()
class_pct = df['Revenue'].value_counts(normalize=True) * 100
for label in [False, True]:
    print(f"  {str(label):>5} (purchase={label}): {class_counts[label]:>6} sessions  ({class_pct[label]:.2f}%)")
print(f"  Imbalance ratio: {class_counts[False] / class_counts[True]:.2f} : 1")

print("\n" + "=" * 70)
print("2. STRONGEST CORRELATIONS BETWEEN NUMERIC FEATURES")
print("=" * 70)
numeric_df = df.select_dtypes(include='number')
corr = numeric_df.corr().abs()

upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
top_corr = upper.unstack().dropna().sort_values(ascending=False).head(10)
print("Top 10 correlated feature pairs:")
for (a, b), v in top_corr.items():
    sign = "+" if numeric_df.corr().loc[a, b] > 0 else "-"
    print(f"  {sign}{v:.3f}  |  {a}  <->  {b}")

print("\n" + "=" * 70)
print("3. PAGE VALUES BY PURCHASE OUTCOME")
print("=" * 70)
for outcome in [False, True]:
    subset = df[df['Revenue'] == outcome]['PageValues']
    print(f"  Revenue = {outcome}:")
    print(f"    count  : {len(subset)}")
    print(f"    mean   : {subset.mean():.2f}")
    print(f"    median : {subset.median():.2f}")
    print(f"    max    : {subset.max():.2f}")

print("\n" + "=" * 70)
print("4. BOUNCE RATES BY PURCHASE OUTCOME")
print("=" * 70)
for outcome in [False, True]:
    subset = df[df['Revenue'] == outcome]['BounceRates']
    print(f"  Revenue = {outcome}:")
    print(f"    mean   : {subset.mean():.4f}")
    print(f"    median : {subset.median():.4f}")
    print(f"    max    : {subset.max():.4f}")

print("\n" + "=" * 70)
print("5. SESSIONS AND CONVERSION RATE BY MONTH")
print("=" * 70)
month_order = ['Feb', 'Mar', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_table = df.groupby('Month').agg(
    total_sessions=('Revenue', 'size'),
    purchases=('Revenue', 'sum')
).reindex(month_order)
month_table['conversion_rate_%'] = (month_table['purchases'] / month_table['total_sessions'] * 100).round(2)
print(month_table.to_string())

print("\n" + "=" * 70)
print("6. SESSIONS AND CONVERSION RATE BY VISITOR TYPE")
print("=" * 70)
vt_table = df.groupby('VisitorType').agg(
    total_sessions=('Revenue', 'size'),
    purchases=('Revenue', 'sum')
)
vt_table['conversion_rate_%'] = (vt_table['purchases'] / vt_table['total_sessions'] * 100).round(2)
print(vt_table.to_string())

print("\n" + "=" * 70)
print("7. WEEKEND vs WEEKDAY")
print("=" * 70)
wknd_table = df.groupby('Weekend').agg(
    total_sessions=('Revenue', 'size'),
    purchases=('Revenue', 'sum')
)
wknd_table['conversion_rate_%'] = (wknd_table['purchases'] / wknd_table['total_sessions'] * 100).round(2)
print(wknd_table.to_string())

print("\n" + "=" * 70)
print("ALL OUTPUTS PRINTED. CHARTS WILL OPEN ONE AT A TIME.")
print("=" * 70)

plt.figure(figsize=(7, 5))
ax = sns.countplot(x='Revenue', data=df, palette=['#4C72B0', '#DD8452'])
total = len(df)
for p in ax.patches:
    count = int(p.get_height())
    pct = 100 * count / total
    ax.annotate(f'{count}\n({pct:.1f}%)',
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.title('Class Distribution: Did the Visitor Make a Purchase?', fontsize=13)
plt.xlabel('Revenue (Purchase Made)')
plt.ylabel('Number of Sessions')
plt.ylim(0, max(class_counts) * 1.15)
plt.tight_layout()
plt.savefig('fig1_class_distribution.png', dpi=150, bbox_inches='tight')
plt.show()

plt.figure(figsize=(13, 10))
mask = np.triu(np.ones_like(numeric_df.corr(), dtype=bool))
sns.heatmap(numeric_df.corr(), annot=True, fmt='.2f', cmap='coolwarm',
            center=0, vmin=-1, vmax=1, mask=mask, square=True,
            linewidths=0.5, cbar_kws={'shrink': 0.8})
plt.title('Correlation Heatmap of Numeric Features', fontsize=13)
plt.tight_layout()
plt.savefig('fig2_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.boxplot(x='Revenue', y='PageValues', data=df, ax=axes[0],
            palette=['#4C72B0', '#DD8452'])
axes[0].set_title('Page Values by Purchase Outcome (Full View)', fontsize=12)
axes[0].set_xlabel('Revenue')
axes[0].set_ylabel('Page Values')

sns.boxplot(x='Revenue', y='PageValues', data=df, ax=axes[1],
            palette=['#4C72B0', '#DD8452'], showfliers=False)
axes[1].set_title('Page Values by Purchase Outcome (Zoomed, no outliers)', fontsize=12)
axes[1].set_xlabel('Revenue')
axes[1].set_ylabel('Page Values')

plt.tight_layout()
plt.savefig('fig3_pagevalues_boxplot.png', dpi=150, bbox_inches='tight')
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.boxplot(x='Revenue', y='BounceRates', data=df, ax=axes[0],
            palette=['#4C72B0', '#DD8452'])
axes[0].set_title('Bounce Rates by Purchase Outcome (Full View)', fontsize=12)
axes[0].set_xlabel('Revenue')
axes[0].set_ylabel('Bounce Rates')

sns.boxplot(x='Revenue', y='BounceRates', data=df, ax=axes[1],
            palette=['#4C72B0', '#DD8452'], showfliers=False)
axes[1].set_title('Bounce Rates by Purchase Outcome (Zoomed, no outliers)', fontsize=12)
axes[1].set_xlabel('Revenue')
axes[1].set_ylabel('Bounce Rates')

plt.tight_layout()
plt.savefig('fig4_bouncerates_boxplot.png', dpi=150, bbox_inches='tight')
plt.show()

fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(x='Month', hue='Revenue', data=df, order=month_order,
              palette=['#4C72B0', '#DD8452'], ax=ax)

for i, month in enumerate(month_order):
    if month in month_table.index and not pd.isna(month_table.loc[month, 'conversion_rate_%']):
        rate = month_table.loc[month, 'conversion_rate_%']
        total_m = month_table.loc[month, 'total_sessions']
        ax.text(i, total_m + 80, f'{rate}%',
                ha='center', fontsize=10, fontweight='bold', color='#333')

plt.title('Sessions and Purchases by Month  (% = conversion rate)', fontsize=13)
plt.xlabel('Month')
plt.ylabel('Number of Sessions')
plt.legend(title='Revenue', loc='upper right')
plt.tight_layout()
plt.savefig('fig5_purchases_by_month.png', dpi=150, bbox_inches='tight')
plt.show()

fig, ax = plt.subplots(figsize=(9, 5.5))
sns.countplot(x='VisitorType', hue='Revenue', data=df,
              palette=['#4C72B0', '#DD8452'], ax=ax)

for i, vt in enumerate(df['VisitorType'].value_counts().index):
    if vt in vt_table.index:
        rate = vt_table.loc[vt, 'conversion_rate_%']
        total_v = vt_table.loc[vt, 'total_sessions']
        ax.text(i, total_v + 80, f'{rate}%',
                ha='center', fontsize=11, fontweight='bold', color='#333')

plt.title('Sessions and Purchases by Visitor Type  (% = conversion rate)', fontsize=13)
plt.xlabel('Visitor Type')
plt.ylabel('Number of Sessions')
plt.legend(title='Revenue', loc='upper right')
plt.tight_layout()
plt.savefig('fig6_visitor_type.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nAll charts saved as PNG files in your project folder.")
