import pandas as pd
import numpy as np
import math as mt
import os
from io import StringIO

#https://cahyadsn.phpindonesia.id/extra/topsis.php#top_07
#https://studyshut.blogspot.com/2018/11/contoh-perhitungan-manual-penyelesaian.html

def topsis(file,filew,isUpload):

    #Read untuk HTML
    if(isUpload):
        df = file
        wgt = filew
    else:
        df = pd.read_csv(file)
        wgt = pd.read_csv(filew)

    #untuk perhitungan
    df2 = pd.read_csv(StringIO(u""+df.to_csv(index=False)), header=None, index_col= 0, skiprows=1 )
    wgt2 = pd.read_csv(StringIO(u""+wgt.to_csv(index=False)), header=None, index_col= 0, skiprows=1 )
    
    #Membuat matriks
    matrix = df2.values
    rmat = len(matrix[:,0]) # 6
    cmat = len(matrix[0,:]) # 4
    #WEIGHT
    weight = wgt2.values 

    # X untuk R
    x = []
    for i in matrix.T:
        temp = 0
        for j in i:
            temp += pow(i[j],2)
        temp = mt.sqrt(temp)
        x.append(temp)

    # MATRIX NORMALISASI (R)
    R = np.copy(matrix)
    R = np.asfarray(R,float)

    for i in range(rmat):
        for j in range(cmat):
            R[i][j] = matrix[i][j] / x[j]

    #print("R\n",R)

    # MATRIX NORMALISASI TERBOBOT (Y)
    Y = np.copy(R)
    Y = np.asfarray(R,float)

    for i in range(rmat):
        for j in range(cmat):
            Y[i][j] = R[i][j] * weight[j]

    #print("Y\n",Y)

    # MENENTUKAN A+ dan A-
    A = np.arange((2*cmat)).reshape(2,cmat)
    A = np.asfarray(A,float)

    for i in range(len(A[0,:])):
        A[0,i] = max(Y[:,i])
        A[1,i] = min(Y[:,i])

    #print("A\n",A)

    # MENENTUKAN D+ dan D-
    D = np.arange((2*rmat)).reshape(rmat,2)
    D = np.asfarray(D,float)
    
    for i in range(rmat):
        temp = 0
        for j in range(cmat):
            temp += pow((A[0][j] - Y[i][j]),2)
        temp = mt.sqrt(temp)
        D[i][0] = temp
    
    for i in range(rmat):
        temp = 0
        for j in range(cmat):
            temp += pow((A[1][j] - Y[i][j]),2)
        temp = mt.sqrt(temp)
        D[i][1] = temp

    #print("D\n",D)

    #Menghitung Nilai Preferensi
    V = np.arange((rmat*2)).reshape(rmat,2)
    V = np.asfarray(V,float)

    temp = 0
    for i in range(len(V[:,0])):
        V[i][0] = temp
        temp = temp + 1

    for i in range(rmat):
        V[i][1] = D[i][1] / (D[i][1] + D[i][0])

    #print("V\n",V)

    #RANKING 
    Kreditor = df
    ValuedKreditor = Kreditor.assign(Value = V[:,1])

    Sorted = ValuedKreditor.sort_values(by='Value', ascending=False)
    #print("Sorted\n",Sorted)
    
    #OUTPUT
    data = {
        "datakreditor": df,
        "weight": wgt,
        "sortedkreditor": Sorted
    } 
    return data

#print(topsis())
#topsis()