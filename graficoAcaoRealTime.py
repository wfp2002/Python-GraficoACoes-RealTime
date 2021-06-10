import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime
import pandas as pd
import requests

fig = plt.figure(figsize=(10,2), facecolor='#FAFAFA')

ax1 = fig.add_subplot(121) #121 = 1 linha, 2 Colunas, indice 1 ou seja primeiro grafico
ax2 = fig.add_subplot(122) #122 = 1 linha, 2 Colunas, indice 2 ou seja segundo grafico
#Criando o DF vazio com as colunas abaixo
df =  pd.DataFrame(columns=['data', 'seed', 'bnb'])

#funcao animate que sera chamada pela funcao animation do matplotlib
def animate(i):
    global df #Definindo global para usar o dataframe criado fora da funcao
    xs = [] #lista do eixo x
    yseed = [] #lista do eixo y seed
    ybnb = [] #lista do eixo y bnb

    r = requests.get('https://bscscan.com/token/0x40b34cc972908060d6d527276e17c105d224559d') #SEED
    r2 = requests.get('https://bscscan.com/token/0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c') #BNB
    
    seed = float(r.text.split('$')[1].split(',')[0])
    bnb = float(r2.text.split('$')[1].split(',')[0])
    data = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    #Colocando a info coletada e a data dentro do DataFrame
    df = df.append({'data': data, 'seed': seed, 'bnb': bnb}, ignore_index=True)

    if len(df) == 16: #Deixando apenas 15 registros no Dataframe para exibit no grafico
        df = df.drop(0) #Deletando registro index(0) o mais antigo
        df = df.reset_index(drop=True) #Refazendo o index

    #Fazendo iteracao no dataframe para gravar nas listas
    for index, _ in df.iterrows():
            xs.append(str(df.data[index]))
            yseed.append(float(df.seed[index]))
            ybnb.append(float(df.bnb[index]))
        
    print(df)        
    
    #Limpando os axes
    ax1.clear()
    ax2.clear()

    #Definindo o fundo do texto (axes.text) que informara o preco da acao dentro do grafico.
    props = dict(boxstyle='round', facecolor='#FFE6C8', alpha=0.5)

    #Dados do grafico 1 SEED
    ax1.text(0.05, 0.95, 'Valor: $'+str(seed), transform=ax1.transAxes, fontsize=14,verticalalignment='top', bbox=props)
    ax1.set_ylim(df.seed.min()-1,df.seed.max()+1)
    ax1.tick_params(axis='x', labelrotation=20, labelsize=7)
    ax1.grid(color = "gainsboro", linestyle='--', linewidth=0.5)
    ax1.set_title('SEED')
    ax1.set_ylabel("VALOR EM DOLAR")
    ax1.plot(xs, yseed)

    #Dados do grafico 2 BNB
    ax2.text(0.05, 0.95, 'Valor: $'+str(bnb), transform=ax2.transAxes, fontsize=14,verticalalignment='top', bbox=props)
    ax2.set_ylim(df.bnb.min()-1,df.bnb.max()+1)
    ax2.tick_params(axis='x', labelrotation=20, labelsize=7)
    ax2.grid(color = "gainsboro", linestyle='--', linewidth=0.5)
    ax2.set_title('BNB')
    ax2.set_ylabel("VALOR EM DOLAR")
    ax2.plot(xs, ybnb)
    
#Chamando a funcao animation 
ani = animation.FuncAnimation(fig, animate, interval=15000) #interval=15000 Atualiza de 15 em 15 segundos

#Inserindo ajustes para melhor visualizacao os valores podem ser obtidos direto na feramenta de ajustes no grafico gerado.
#Faca os ajustes em tempo real usando a ferramenta depois passe os valores para essas variaveis.
plt.subplots_adjust(left=0.05, bottom=0.7, right=0.97, top=0.95, wspace=0.25, hspace=0.2)
plt.show()