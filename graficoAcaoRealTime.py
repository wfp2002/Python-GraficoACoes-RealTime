import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import pandas as pd
import requests
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import FormatStrFormatter

fig = plt.figure(figsize=(10,2), facecolor='#FAFAFA')
fig.suptitle('GRAFICO DAS ULTIMAS 25 COTACOES', fontsize=16)

#2,2,1
#R,C,I (Row, Column, Index)
ax1 = fig.add_subplot(2,2,1) #2,2,1 = 2 linhas, 2 Colunas, indice 1 ou seja primeiro grafico
ax2 = fig.add_subplot(2,2,2) #2,2,2 = 2 linhas, 2 Colunas, indice 2 ou seja segundo grafico
ax3 = fig.add_subplot(2,2,3) #2,2,2 = 2 linhas, 2 Colunas, indice 3 ou seja terceiro grafico
ax4 = fig.add_subplot(2,2,4) #2,2,2 = 2 linhas, 2 Colunas, indice 4 ou seja quarto grafico

#Criando o DF vazio com as colunas abaixo
df =  pd.DataFrame(columns=['datahora','data','hora', 'seed', 'bnb','btc','ada'])

#funcao animate que sera chamada pela funcao animation do matplotlib
def animate(i):
    global df #Definindo global para usar o dataframe criado fora da funcao
    
    props = dict(boxstyle='round', facecolor='#FFE6C8', alpha=0.5) #Definindo o fundo do texto (axes.text) que informara o preco da acao dentro do grafico.    
    
    datahora = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    data = datahora.split(' ')[0]
    hora = datahora.split(' ')[1]
    labelrotation = 70
    labelsize = 8
    percentualMinMax = 0.05
    AnchoredTextSize = 10
    lineSize = 0.5
    
    reqSEED = requests.get('https://bscscan.com/token/0x40b34cc972908060d6d527276e17c105d224559d') #SEED
    reqBTC = requests.get("https://www.coingecko.com/en/coins/bitcoin")
    reqADA = requests.get("https://www.coingecko.com/en/coins/cardano")
    
    seed = float(reqSEED.text.split('$')[1].split(',')[0])
    bnb = float(reqSEED.text.split('BNB: $')[1].split('<')[0]) #Pegando o valor da BNB da mesma tela da SEED para nao fazer mais uma requisiscao
    btc = float(reqBTC.text.split('price.price">$')[1].split('<')[0].replace(',',''))
    ada = float(reqADA.text.split('price.price">$')[1].split('<')[0].replace(',',''))

    #Colocando a info coletada e a data dentro do DataFrame
    df = df.append({'datahora': datahora, 'data':data, 'hora':hora, 'seed': seed, 'bnb': bnb, 'btc': btc, 'ada': ada}, ignore_index=True)
    
    if len(df) == 26: #Deixando apenas 25 registros no Dataframe para exibit no grafico
        df = df.drop(0) #Deletando registro index(0) o mais antigo
        df = df.reset_index(drop=True) #Refazendo o index
    
    print(df)   
    print('------------------------------------------------------------------------')

    #Definindo os percentuais para gerar a legenda do eixo y, ou seja, o grafico ira compreender de 5% acima a 5% abaixo do preco para gerar a escala do eixo y Min e Max
    seedMin = float(df.seed.min() - (df.seed.min() * percentualMinMax))
    seedMax = float(df.seed.max() + (df.seed.max() * percentualMinMax))
    bnbMin = float(df.bnb.min() - (df.bnb.min() * percentualMinMax))
    bnbMax = float(df.bnb.max() + (df.bnb.max() * percentualMinMax))
    btcMin = float(df.btc.min() - (df.btc.min() * percentualMinMax))
    btcMax = float(df.btc.max() + (df.btc.max() * percentualMinMax))
    adaMin = float(df.ada.min() - (df.ada.min() * percentualMinMax))
    adaMax = float(df.ada.max() + (df.ada.max() * percentualMinMax))
        
    #Limpando os axes
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    
    #Dados do grafico 1 SEED
    ax1.set_ylim(seedMin,seedMax)
    ax1.tick_params(axis='x', labelrotation=labelrotation, labelsize=labelsize)
    ax1.grid(color = "gainsboro", linestyle='--', linewidth=lineSize)
    ax1.set_title('SEED')
    ax1.set_ylabel("VALOR EM DOLAR")
    ax1.plot(df.hora, df.seed)
    ax1.add_artist(AnchoredText('Valor: $'+str(round(seed,2)), loc=2, prop=dict(size=AnchoredTextSize, bbox=props),frameon=False))  
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f')) #Formatando eixo x para 2 casas decimais
    
    #Dados do grafico 2 BNB
    ax2.set_ylim(bnbMin,bnbMax)
    ax2.tick_params(axis='x', labelrotation=labelrotation, labelsize=labelsize)
    ax2.grid(color = "gainsboro", linestyle='--', linewidth=lineSize)
    ax2.set_title('BNB')
    ax2.set_ylabel("VALOR EM DOLAR")
    ax2.plot(df.hora, df.bnb)
    ax2.add_artist(AnchoredText('Valor: $'+str(round(bnb,2)), loc=2, prop=dict(size=AnchoredTextSize, bbox=props),frameon=False)) 
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f')) #Formatando eixo x para 2 casas decimais

    #Dados do grafico 1 BTC
    ax3.set_ylim(btcMin,btcMax)
    ax3.tick_params(axis='x', labelrotation=labelrotation, labelsize=labelsize)
    ax3.grid(color = "gainsboro", linestyle='--', linewidth=lineSize)
    ax3.set_title('BTC')
    ax3.set_ylabel("VALOR EM DOLAR")
    ax3.plot(df.hora, df.btc)
    ax3.add_artist(AnchoredText('Valor: $'+str(round(btc,2)), loc=2, prop=dict(size=AnchoredTextSize, bbox=props),frameon=False)) 
    ax3.yaxis.set_major_formatter(FormatStrFormatter('%.0f')) #Formatando eixo x para 2 casas decimais 
    
    #Dados do grafico 2 ADA
    ax4.set_ylim(adaMin,adaMax)
    ax4.tick_params(axis='x', labelrotation=labelrotation, labelsize=labelsize)
    ax4.grid(color = "gainsboro", linestyle='--', linewidth=lineSize)
    ax4.set_title('ADA')
    ax4.set_ylabel("VALOR EM DOLAR")
    ax4.plot(df.hora, df.ada)
    ax4.add_artist(AnchoredText('Valor: $'+str(round(ada,2)), loc=2, prop=dict(size=AnchoredTextSize, bbox=props),frameon=False))   
    ax4.yaxis.set_major_formatter(FormatStrFormatter('%.2f')) #Formatando eixo x para 2 casas decimais 

#Chamando a funcao animation 
ani = animation.FuncAnimation(fig, animate, interval=15000) #interval=15000 Atualiza de 15 em 15 segundos

#Inserindo ajustes para melhor visualizacao os valores podem ser obtidos direto na feramenta de ajustes no grafico gerado.
#Faca os ajustes em tempo real usando a ferramenta depois passe os valores para essas variaveis.
plt.subplots_adjust(left=0.07, bottom=0.2, right=0.97, top=0.85, wspace=0.20, hspace=0.75)

#plt.get_current_fig_manager().full_screen_toggle() #Abre o grafico em FullScreen sem opcao de minimizar e maximizar
plt.get_current_fig_manager().window.state('zoomed') #Abre o grafico em FullScreen com opcao de minimizar e maximizar
plt.show()
