import json
import os, sys
import pandas as pd
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import *


app = QtWidgets.QApplication(sys.argv)
tela = uic.loadUi("telainv.ui")



def BrowseFile():
    fname = QtWidgets.QFileDialog.getExistingDirectory(tela, 'Open File','C:')
    print(fname)
    tela.explorer.setText(fname)


def Carrega():
    path = tela.explorer.text()
    if path =='':
        #print('?')
        tela.msg.setText('INFORME O DIRETORIO DOS LOGS')
    else:
        tela.setEnabled(False)
        tela.msg.setText('CARREGANDO...')
        QApplication.processEvents()
        # print(path)
        lista = []
        datalist =[]
        #word = tela.busca.text()
        #print('oi')
        # iterate through all file
        for file in os.listdir(path):
            # Check whether file is in text format or not
            if file.endswith(".txt"):
                file_path = f"{path}\{file}"
                lista.insert(len(lista) + + 1, file)
                #print(file)
                try:
                    myfile = open(file_path)
                    # print('tentei')
                    data = myfile.read()
                    data = data.upper()
                    data = data.replace(" ","")
                    data_into_list = data.split("\n")
                    datalist = data_into_list + datalist
                    myfile.close()
                    # print('TO NO TRY')


                except:
                    # print('naoleu1')
                    pass

                #data = ' '.join(str(e) for e in datalist)
                #print('ok')
                # print(data)

                '''if word in data:
                    print('Palavra encontrada no arquivo: ' + file)
                    #lista.insert(len(lista) + + 1, file)
                else:
                    # print('NÃO TEM')
                    pass
                # print('fechou')'''

            else:
                pass
        tela.setEnabled(True)
        tela.msg.setText('')

        #print(lista)
        listaDes = '\n'.join(lista)
        #print(datalist)
        tela.textBrowser.setPlainText(listaDes)
        nodupes = list(dict.fromkeys(datalist))

        Carrega.nodupesDes = '\n'.join(nodupes)
        #print(Carrega.nodupesDes)

        #print(Carrega.nodupesDes)
        #tela.textBrowser_2.setPlainText(Carrega.nodupesDes)

Carrega.nodupesDes =''

def carregacsv():
    path = tela.explorer.text()
    if path == '':
        # print('?')
        tela.msg.setText('INFORME O DIRETORIO DOS LOGS')
    else:
        tela.setEnabled(False)
        tela.msg.setText('CARREGANDO...')
        QApplication.processEvents()
        lista = []
        for file in os.listdir(path):
            if file.endswith(".csv"):
                #print(file)
                file_path = f"{path}\{file}"
                lista.append(file)
                #print(file)

        lista = '\n'.join(lista)
        #print(lista)
        tela.textBrowser.setPlainText(lista)
        tela.setEnabled(True)
        tela.msg.setText('')

def convertecsv():
    path = tela.explorer.text()
    if path == '':
        # print('?')
        tela.msg.setText('INFORME O DIRETORIO DOS LOGS')
    else:
        tela.setEnabled(False)
        tela.msg.setText('CARREGANDO...')
        QApplication.processEvents()
        for file in os.listdir(path):
            if file.endswith(".csv"):
                datalist = []
                lista = []
                listcsv0 = []
                skip = ''
                file_path = f"{path}\{file}"
                lista.insert(len(lista) + + 1, file)
                #print(file)
                myfile = open(file_path)
                data = myfile.read()
                data = data.replace("	", "")
                data_into_list = data.split("\n")
                conta = 0
                datalist = data_into_list + datalist
                for linha in datalist:
                    conta = conta + 1
                    # print(conta)
                    if (linha[0:3]) == 'EPC':
                        print(linha)
                        skip = int(conta)
                        print(skip)

                # print('tentei')
                header = ['EPC']
                df = pd.DataFrame(columns=header)
                # print(df.to_string())
                df = pd.read_csv(file_path, na_values=['.'], header=None, skiprows=skip, usecols=[0])

                listcsv = pd.DataFrame(df[0].to_string(index=False).replace("\\t", "").replace(" ", "").split("\n"))

                listcsv = listcsv.values.tolist()
                for junta in listcsv:
                    # print(str(junta[0]))
                    listcsv0.append(junta[0])
                listcsvf = '\n'.join(listcsv0)


                finalfile = file_path + '.txt'
                # print(finalfile)
                f = open(finalfile, 'w')
                f.write(str(listcsvf))
                print('criou')
                tela.setEnabled(True)
                tela.msg.setText('ARQUIVOS CONVERTIDOS COM SUCESSO')

def onefile():
    if Carrega.nodupesDes =='':
        print('?')
        tela.msg.setText('BUSQUE OS DADOS PRIMEIRO')
    else:
        print('eita')
        tela.setEnabled(False)
        tela.msg.setText('CRIANDO ARQUIVO')
        QApplication.processEvents()
        path = tela.explorer.text()
        finalfile = path + '/consolidado.txt'
        #print('quant - ' + len(Carrega.nodupesDes))
        print(finalfile)
        f = open(finalfile, 'w')
        #print(Carrega.nodupesDes)
        print(Carrega.nodupesDes[33748000:33750000])
        f.write(Carrega.nodupesDes[33749000:33750000])
        #f.write(Carrega.nodupesDes)
        f.close()
        print('criou')
        # print(Carrega.nodupesDes)
        tela.setEnabled(True)
        tela.msg.setText('ARQUIVO CRIADO ' + finalfile)


def limpa():

    tela.textBrowser.setText('')
    tela.explorer.setText('')
    tela.msg.setText('')
    Carrega.nodupesDes = ''

#tela.busca.returnPressed.connect(Carrega)
tela.FindButton.clicked.connect(Carrega)
tela.csv.clicked.connect(carregacsv)
tela.convertecsv.clicked.connect(convertecsv)
tela.Merge.clicked.connect(onefile)
tela.ExplorerButton.clicked.connect(BrowseFile)
tela.clear.clicked.connect(limpa)



tela.show()
app.exec()