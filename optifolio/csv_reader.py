import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
'''
df = pd.read_csv('przykładowe_dane.csv', sep=';')
df.dropna(axis=1, inplace=True)
print(df)



# liczenie obecnej wartości portfela
def transaction_val(row):
    if row['buy_sell'] == 'K':
        return row['liczba akcji']*row['course']+row['fare']
    elif row['buy_sell'] == 'S':
        return -1*(row['liczba akcji']*row['course']+row['fare'])
    
wallet_value = df.apply(transaction_val, axis=1).sum()
print(wallet_value)


# jak odfiltrować część danych - np. tylko kupno akcji
df[df['buy_sell']=='K'].head()


# przykładowa tabela z firmami i sektorami
firmy = pd.DataFrame(data={'firma': ['Adobe','Makita','21 st Century Fox','Starbucks','Facebook','BlackBerry','EBay','Netflix','Moderna','AstraZeneca','Apple','NASDAQ','Garmin'], 'sektor': ['informatyczny', 'elektryczny', 'rozrywkowy', 'gastronomiczny', 'informatyczny', 'elektroniczny', 'informatyczny', 'rozrywkowy', 'medyczny', 'medyczny', 'elektroniczny', 'ekonomiczny', 'elektroniczny']})
print(firmy)


# liczę ile akcji każdej firmy kupiono oraz sprzedano
kupione_akcje = df[df['buy_sell']=='K'].groupby(['nazwa']).sum()['liczba akcji']
sprzedane_akcje = df[df['buy_sell']=='S'].groupby(['nazwa']).sum()['liczba akcji']

# tworzę osobną tabelę przefstawiającą obecny stan portfela
portfel = pd.DataFrame(kupione_akcje)
portfel.rename(columns={"liczba akcji": "kupione"}, inplace=True)
portfel['sprzedane'] = sprzedane_akcje
portfel.fillna(0, inplace=True)
portfel['balans'] = portfel['kupione'] - portfel['sprzedane']
print(portfel)

# biorę do wykresu tylko firmy których akcje użytkownik posiada (jest ich więcej niż 0)
pie_data = portfel['balans'][portfel['balans'] > 0].sort_values(ascending=False)
print(pie_data)

# jest brzydki, wiem
labels = list(pie_data.index.values)
plt.pie(pie_data, labels=labels)
plt.show()

# nad tym siedziałam długo XD
sektory = pie_data.to_frame().join(firmy.set_index('firma'))
sektory

pie_data2 = sektory.groupby(by=['sektor']).sum()
pie_data2 = pie_data2['balans'].sort_values(ascending=False)
pie_data2


labels = list(pie_data2.index.values)
plt.pie(pie_data2, labels=labels)
plt.show()

sektory.sort_values(by='sektor')

# zbieram w grupy dane do wykresu zagnieżdżonego
nested_data_out = sektory.sort_values(by='sektor').groupby(by=['sektor']).sum()['balans']
labels_out = sektory.sort_values(by='sektor').groupby(by=['sektor']).sum().index.values
nested_data_in = sektory.sort_values(by='sektor')['balans']
labels_in = sektory.sort_values(by='sektor').index.values


fig, ax = plt.subplots()

size = 0.3

cmap = plt.get_cmap("tab20c")
outer_colors = cmap(np.arange(3)*4)
inner_colors = cmap([1, 2, 5, 6, 9, 10])

ax.pie(nested_data_out, radius=1, colors=outer_colors, startangle=0, normalize=True,
       labels=labels_out, wedgeprops=dict(width=size, edgecolor='w'))

ax.pie(nested_data_in, radius=1-size, colors=inner_colors, startangle=0, normalize=True,
       wedgeprops=dict(width=size, edgecolor='w'))

ax.set(aspect="equal", title='podział portfela na sektory i firmy')
plt.show()


