import pandas as pd
import numpy as np
from itertools import combinations
from collections import defaultdict
import requests

# Membaca file CSV dari URL
def hitung_eclatku(file_csv, min_support=0.001):
    data = pd.read_csv(file_csv, index_col=None)    
    grouped_data = data.groupby('Transaction')['Item'].apply(set).reset_index()
# Menghitung jumlah transaksi total
    total_transactions = len(grouped_data)
# Inisialisasi dictionary untuk menyimpan itemset dan transaksi yang mengandung itemset
    itemsets = defaultdict(list)
# Membuat itemset untuk setiap transaksi
    for index, row in grouped_data.iterrows():
        transaction_id = row['Transaction']
        items = row['Item']
        for item in items:
            itemsets[item].append(transaction_id)
    # Inisialisasi list untuk menyimpan pasangan item, support, dan confidence
    rules = []
    supports = []
    confidences = []
    # Menentukan nilai minimum support
    # min_support = 0.001  # Ubah sesuai kebutuhan
    # Menentukan pasangan item dan menghitung support serta confidence
    for item1, item2 in combinations(itemsets.keys(), 2):
        transactions_item1 = set(itemsets[item1])
        transactions_item2 = set(itemsets[item2])
        intersection = transactions_item1.intersection(transactions_item2)
        
        support = len(intersection) / total_transactions
        confidence_item1_to_item2 = len(intersection) / len(transactions_item1)
        confidence_item2_to_item1 = len(intersection) / len(transactions_item2)
        
        # Menambahkan kondisi untuk minimum support
        if support >= min_support:
            rules.append(f"jika beli {item1}, maka beli {item2}")
            rules.append(f"jika beli {item2}, maka beli {item1}")
            supports.extend([support, support])
            confidences.extend([confidence_item1_to_item2, confidence_item2_to_item1])

    # Membuat DataFrame dari hasil
    df_results = pd.DataFrame({
        'Rules': rules,
        'Support': supports,
        'Confidence': confidences
    })

    # Mengurutkan DataFrame berdasarkan nilai Support dan Confidence
    sorted_df = df_results.sort_values(by=['Support', 'Confidence'], ascending=False, ignore_index=True)
    # Menampilkan hasil
    sorted_df = sorted_df.reset_index(drop=True)
    return sorted_df
