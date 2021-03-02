import os
from flask import Flask, render_template, request, current_app
from flask_pager import Pager
app = Flask(__name__)
app.secret_key = os.urandom(42)
app.config['PAGE_SIZE'] = 1
app.config['VISIBLE_PAGE_COUNT'] = 20

# -*- coding: utf-8 -*-
path = './data.csv'
import pandas as pd
data=pd.read_csv(path)

data=data[['sub_index','sent','prediction']]
big=[]
small=[]
new={}
for i in range(len(data)):
    j=i+1
    if j==len(data): break
    elif data["sub_index"][j]!=1:
        new['index']=data["sub_index"][i]
        new["sent"]=data["sent"][i]
        new["pred"]=data["prediction"][i]
        small.append(new)
        new={}
    else:
        new['index']=data["sub_index"][i]
        new["sent"]=data["sent"][i]
        new["pred"]=data["prediction"][i]
        small.append(new)
        new={}
        big.append(small)
        small=[]

print(len(big[0]))

@app.route("/")
def index():
    page = int(request.args.get('page', 1))
    count = len(big)
    pager = Pager(page, count)
    pages = pager.get_pages()
    skip = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show=big[skip: skip + limit]
    return render_template('index.html', pages=pages, data_to_show=data_to_show,length=len(data_to_show[0]))


if __name__ == '__main__':
    app.run(debug=True)

