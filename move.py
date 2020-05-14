import time
ini=time.time()
import sys
from tkinter import *
from functools import partial
from DNAStrand import *
import random
def bt_click_shuffle():
    foo=list(conteudos[1])
    random.shuffle(foo)
    foo=str().join(foo)
    lb_fita_2["text"] = foo
    conteudos[1]=foo
    lista=reset()

def bt_click_move(i=1):
    lista[0]+=(fonte[2]*i)
    lista[1]=lista[1]+(1*i)
    lb_fita_2.place(x=lista[0])
    if conteudos[0]:
        Recebe_Label_1, Recebe_Label_2 =DNAStrand(conteudos[0]).Move(DNAStrand(conteudos[1]), lista[1], telas["Verbo"])
        lb_fita_1["text"] = Recebe_Label_1
        lb_fita_2["text"] = Recebe_Label_2
    else:
        lb_fita_1["text"] = ""
        lb_fita_2["text"] = conteudos[1]
    lb_total['text']=ContaCasais()
    printv(f"Matches: {lb_total['text']}")
    #Reseta se passar das bordas
    borda=janela.winfo_width()
    posFinal=lb_fita_2.winfo_width()+lista[0]
    if (lista[0]>borda) or posFinal<0:
        reset()
    printv(lista)
    return lista

#Função que movimenta a label 2 no eixo vertical.
def bt_UPDOWN(i=0.05):
    lista[2]+=i
    lb_fita_2.place(x=lista[0], rely=lista[2])
    printv(lista)
    if not(0<lista[2]<1):
        reset()
    return lista

#Funçao que lê o que está escrito nos formulários
#Se receber um dígito, gera uma fita válida aleatória
#com tamanho igual ao número recebido.
def bt_clickOk():
    conteudos[0]=ed1.get().upper()
    conteudos[1]=ed2.get().upper()
    for k in range(2):
        if conteudos[k].isdigit():
            cria_strand_por_tamanho(k)
    bt_click_move(0)
    reset()

def cria_strand_por_tamanho(fita):
    printv("Gerada aleatoriamente")
    conteudos[fita]=str().join([random.choice("GATC") for fita in range(abs(int(conteudos[fita])))])
    
#Exibe o complemento da segunda fita.
def bt_complement():
    printv(telas["Complemento"])
    if telas["Complemento"]:
        foo=DNAStrand(conteudos[0])
        if foo.isValid():
            foo=foo.createComplement()
        else:
            foo=""
        lb_fita_1["text"] = foo
        lb_fita_2["text"] = ""
    else:
        bt_click_move(0)
    telas["Complemento"]=not(telas["Complemento"])
    return (telas)

#Usando o DNAStrand.py encontra o maior número de pares possíveis.
def bt_max_possibilities():
    reset()
    foo=DNAStrand(conteudos[0])
    bar=DNAStrand(conteudos[1])
    dicioPossibilidades=findMaxAuxy(foo, bar)
    bt_click_move(dicioPossibilidades["MOV"])
    lb_fita_1["text"] = dicioPossibilidades["fita1"]
    lb_fita_2["text"] = dicioPossibilidades["fita2"]
    printv(dicioPossibilidades)

#Abre a janela de ajuda/créditos.
def bt_janelas_auxiliares(h=0):
    h=1 if h else 0
    novaJanela=Tk()
    textoCreditos=textos[h]
    lb_credits=Label(novaJanela, font=("Arial", 12), justify='left', text=textoCreditos)
    lb_credits.pack(fill='both')
    novaJanela.mainloop()

#Captura eventos do teclado
def key(event):
    x=event.keysym.lower()
    printv(x)
    try:
        dicioEventos[x]()
    except:
        pass

def argumentos_do_prompt(prompt):
    for w in range(0, len(prompt)):
        x=prompt[w]
        if x in ['-n', '-m']:
            index=0
            if x =='-m': index=1
            conteudos[index]=int(prompt[w+1])
            cria_strand_por_tamanho(index)
        elif '--dna' in x:
            aux=int(x[7:])
            index=int(x[5])-1
            conteudos[index]=aux
            cria_strand_por_tamanho(index)
        elif x =='-v':
            dicioEventos['v']()
        elif '-h' in x:
            for linha in textos:
                print(linha)
        else:
            pass


def ContaCasais():
    string=lb_fita_2["text"]
    soma=0
    for k in string:
        soma+=k in ("GATC")
    #printv(f"Total de pares:{soma}")
    return soma

def printv(string1):
    if telas['Verbo']:
        print(string1)
    pass
        
def findMaxAuxy(fita1, fita2):
    if type(fita1)!=DNAStrand: fita1=DNAStrand(fita1)
    if type(fita2)!=DNAStrand: fita2=DNAStrand(fita2)
    foo=fita1.findMaxPossibleMatches(fita2, telas["Verbo"])
    bar=fita2.findMaxPossibleMatches(fita1, telas["Verbo"])
    #MOV=foo[1]
    fita1D=dict()
    #fita1D["MAX"]=(foo[0][0])
    fita1D["RES"]=foo[0][1] if foo[0][1] else fita1.strand.lower()
    fita1D["MOV"]=(foo[1])
    fita2D=dict()
    #fita2D["MAX"]=(bar[0][0])
    fita2D["RES"]=(bar[0][1] if bar[0][1] else fita2.strand.lower())
    #fita2D["MOV"]=(bar[1])
    retorno={"MOV":fita1D["MOV"], "fita1":fita1D["RES"], "fita2":fita2D["RES"]}
    return retorno

def verborragico():
    print(f"Método verboso alterado")
    telas['Verbo']=not(telas['Verbo'])
    return telas
    
def reset():
    lista[0]=120
    lista[1]=0
    lista[2]=0.58
    lb_fita_2.place(x=lista[0], rely=lista[2])
    bt_click_move(0)
    return lista


arquivo=open('textos auxiliares.txt', 'r', encoding='utf-8')
textos=arquivo.readlines()
textos=[k.replace('¬', '\n -->').replace('{{', 'o botão ').replace('[[', 'a tecla ').replace('}', '').replace(']', '') for k in textos]
arquivo.close()

janela = Tk()

telas={"Complemento":False, "Verbo":False}
dicioEventos={
            #tudo em minúscula para ser lido com o caps lock ativo
              'u':bt_janelas_auxiliares,  #u de about Us
              'v':verborragico,           #v de verborragico
              'i':bt_complement,          #i de inverso
              'r':reset,                  #r de reset
              'return':bt_clickOk,        #Enter
              'escape':janela.destroy,           #esc
              'delete':partial(print, '\n'*42),
              's':bt_click_shuffle,       #s de shuffle
                                          #Del para limpar o terminal

              #Comandos do professor
              'm':bt_max_possibilities,   
              'left':partial(bt_click_move, -1),
              'shift_l':bt_click_shuffle,       
              'right':bt_click_move,
              'h':partial(bt_janelas_auxiliares, 1),
              'down':partial(bt_UPDOWN),
              'up':partial(bt_UPDOWN, -0.05),
              }
conteudos=["AGTCCA", "TTC"] #Fitas padrão do programa
if len(sys.argv):
    argumentos_do_prompt(sys.argv)
#Botões
##Botões de movimento
bt_left=Button(janela, width=2, text=(chr(0x2b05)), command=dicioEventos['left'])
bt_left.place(x=50, y=130)
bt_right=Button(janela, width=2, text=(chr(0x27a1)), command=dicioEventos['right'])
bt_right.place(x=110, y=130)
bt_reset=Button(janela, width=2, text=(chr(0x21BA)), command=dicioEventos['r'])
bt_reset.place(x=80, y=130)
bt_up=Button(janela, width=2, text=(chr(0x2b06)), command=dicioEventos['up'])
bt_up.place(x=80, y=100)
bt_down=Button(janela, width=2, text=(chr(0x2b07)), command=dicioEventos['down'])
bt_down.place(x=80, y=160)

#setas=[0x2b05, 0x27a1, 0x21ba, 0x2b06, 0x2b07]

## Botões auxiliares do eixo 70. 
bt_Complement=Button(janela, width=2, text="CC", bg='blue', command=dicioEventos['i'])
bt_Complement.place(x=120, y=70)
bt_MelhorCaso=Button(janela, width=2, text="MC", bg='gold', command=dicioEventos['m'])
bt_MelhorCaso.place(x=150, y=70)
bt_limpa_terminal=Button(janela, width=3, text="cls", bg='red', command=dicioEventos['delete'])
bt_limpa_terminal.place(x=180, y=70)
bt_verbo=Button(janela, width=2, text='v', bg='green', command=dicioEventos['v'])
bt_verbo.place(x=220, y=70)
##Botões para entrada de dado
bt_new=Button(janela, width=2, text="OK", command=bt_clickOk)
bt_new.place(x=20, y=70)
bt_shuffle=Button(janela, width=7, text="SHUFFLE", command=bt_click_shuffle)
bt_shuffle.place(x=50, y=70)

#Texto
lista=[120, 0, 0.58]        #posX, armazena deslocamento, posY

fonte=["Fixedsys", 5, 25]   #tipo de fonte, tamanho e ?
##Exibe as duas fitas
lb_fita_1=Label(janela, font=(fonte[0], fonte[1]**2), text=conteudos[0])
lb_fita_2=Label(janela, font=(fonte[0], fonte[1]**2), text=conteudos[1])
lb_fita_1.place(x=120, rely=0.42)
lb_fita_2.place(x=lista[0], rely=lista[2])

##Exibe a quantidade de pares de uma dada combinação
lb_total=Label(janela, font=('Verdana', fonte[1]**2), text='',)
lb_total.place(x=210, y=20)


#Entradas
ed1 = Entry(janela, width=30)
ed1.place(x=20, y=20)
ed2 = Entry(janela, width=30)
ed2.place(x=20, y=50)


## Menu de créditos e ajuda
bt_about=Button(janela, background='pink', text="about us", command=bt_janelas_auxiliares)
bt_about.pack(side='bottom', fill='x')
#bt_credits.place(relx=0.95, rely=0.10)
bt_help=Button(janela, background='red', text="help", command=dicioEventos['h'])
#bt_help.place(relx=0.95, rely=0.05)
bt_help.pack(side='bottom', fill='x')

    
janela.bind_all('<Key>', key)
ini=time.time()-ini
print(ini)
# width x height + left + top

janela.geometry("400x400+200+200")
janela.mainloop()

