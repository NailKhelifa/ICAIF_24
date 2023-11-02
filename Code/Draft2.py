# %%
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from bs4 import BeautifulSoup
import requests 
from pypfopt.efficient_frontier import EfficientFrontier

# %%
## we make some manipulations to correctly import module1

import os
import sys

# on a obtenu le chemin absolu vers notre répertoire en utilisant
# le terminal (ls, pwd, cd)
module_1_directory = '/Users/khelifanail/Documents/GitHub/Portfolio_clustering_project/code'

# Ajouter le chemin du répertoire 'code' au chemin de recherche Python
sys.path.append(module_1_directory)

# Maintenant, vous pouvez importer module1
import module1

# %%
import csv 

with open('S&P500_symbols.csv', mode='r') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)
    
    # Transform the CSV data into a list
    stock_symbols = []
    for row in csv_reader:
        stock_symbols.append(row[0])

# Close the file
file.close()

stock_symbols.pop(0)

# %%
n_stocks = len(stock_symbols) # number of stocks = 502

start = "2022-01-01" # start date
end = "2022-12-31" # end date

df = pd.DataFrame(yf.download(stock_symbols, start, end)) # data on the 502 assets
data = np.log(df["Close"]/df["Open"]).transpose() # compute the returns of these assets
data = data.dropna()

# %% [markdown]
# Ici on va tester le clustering avec du kmeans, k=5 clusters.

# %%
model = KMeans(n_clusters=5)
model_name = 'kmeans'

Y, C = module1.multiple_clusterings(10, data, model, model_name)



# %%
Y_symbol=module1.cluster_composition(Y)
"pour les 5 clusterings"
clustering_composition=[0,0,0,0,0]
clustering_centroid=[0,0,0,0,0]
for i in range(5):
    clustering_composition[i] = pd.DataFrame(Y_symbol.iloc[:, i])
    clustering_centroid[i] = pd.DataFrame(C.iloc[:, i])

returns=module1.clustering_return(clustering_composition[0], clustering_centroid[0], data)


print(returns.iloc[0, 0])


# %%
# Calcul des rendements moyens journaliers pour chaque cluster
daily_expected_returns = pd.Series(
    [np.mean(returns.iloc[i, 0]) for i in range(len(returns))],
    index=returns.index
)

# Annualiser les rendements moyens journaliers
annual_expected_returns = daily_expected_returns * 251
print(annual_expected_returns)
# Construction d'un nouveau DataFrame pour le calcul de la covariance à partir des rendements journaliers
all_returns = pd.DataFrame(
    [returns.iloc[i, 0] for i in range(len(returns))],
    index=returns.index
).T  # Transpose pour que les rendements soient en colonnes

# Calcul de la matrice de covariance annuelle
daily_cov_matrix = all_returns.cov()
annual_cov_matrix = daily_cov_matrix * 251  # Annualiser la matrice de covariance

# Utilisation des rendements attendus annualisés et de la matrice de covariance annuelle dans la fonction markowitz
optimized_weights = module1.markowitz(annual_expected_returns, annual_cov_matrix)

print(optimized_weights)

# %%

print(Y_symbol)
# %%
