from django.shortcuts import render
import requests
import pandas as pd
# Create your views here.


def home(request):
    data = get_data()
    return render(request, 'index.html',{'output':data})


def get_data():
    response = requests.get("https://api.dexlab.space/v1/trades")
    df = pd.DataFrame(response.json()['data'])
    df[["coin1", "coin2"]] = df["market"].str.split(pat="/", expand=True)
    df['price_1'] = df['price'].astype('float') / df['size'].astype('float')
    new_df = df[['coin1', 'coin2', 'price_1', 'createdAt']]
    new_df['createdAt'] = pd.to_datetime(new_df['createdAt']).dt.tz_convert('Australia/Sydney')
    new_df['price_1'] = new_df['price_1'].round(4)
    new_df = new_df[new_df.price_1 > 0.0000]
    data = new_df.to_dict('records')
    return data
