'''
Da aula 5 até a ?
'''
from tkinter import *
from functools import partial
from DNAStrand import *

def bt_click2():
    print('botão clicado')
    lb["text"] = "Funcionou"

def bt_click_shuffle():
    from random import shuffle
    foo=list(conteudos[1])
    shuffle(foo)
    foo=str().join(foo)
    lb_fita_2["text"] = foo
    conteudos[1]=foo
    lista=reset()

def bt_click_move(i=1):
    lista[0]+=(fonte[2]*i)
    lista[1]=lista[1]+(1*i)
    lb_fita_2.place(x=lista[0], y=180)
    if conteudos[0]:
        Recebe_Label_1, Recebe_Label_2 =DNAStrand(conteudos[0]).Move(DNAStrand(conteudos[1]), lista[1])
        lb_fita_1["text"] = Recebe_Label_1
        lb_fita_2["text"] = Recebe_Label_2
    else:
        lb_fita_1["text"] = ""
        lb_fita_2["text"] = conteudos[1]
    
    return lista

def bt_clickOk():
    conteudos[0]=ed1.get().upper()
    conteudos[1]=ed2.get().upper()
    bt_click_move(0)
    lista=reset()

def bt_size(i, step):
    if fonte[step]-i>1:
        fonte[step]+=i
        print(fonte)
        if step==1:
            lb_fita_1["font"] = (fonte[0], fonte[1]**2+1)
            lb_fita_2["font"] = (fonte[0], fonte[1]**2+1)
            print(f"tamanho = {fonte[1]}")
        else:
            print(f"passo={fonte[2]}px")
    else:
        fonte[step]=3
    return fonte

def bt_complement():
    print(telas["Complemento"])
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

def bt_max_possibilities():
    reset()
    foo=DNAStrand(conteudos[0])
    bar=DNAStrand(conteudos[1])
    dicioPossibilidades=findMaxAuxy(foo, bar)
    bt_click_move(dicioPossibilidades["MOV"])
    lb_fita_1["text"] = dicioPossibilidades["fita1"]
    lb_fita_2["text"] = dicioPossibilidades["fita2"]
    print(dicioPossibilidades)

def bt_credits():
    if telas["Credits"]:
        lb_credits["height"]=0
        lb_credits["width"]=0
    else:
        lb_credits["height"]=1
        lb_credits["width"]=1
    print(telas["Credits"], ":", lb_credits["height"], lb_credits["width"])
    telas["Credits"]=not(telas["Credits"])
    return telas

def findMaxAuxy(fita1, fita2):
    if type(fita1)!=DNAStrand: fita1=DNAStrand(fita1)
    if type(fita2)!=DNAStrand: fita2=DNAStrand(fita2)
    foo=fita1.findMaxPossibleMatches(fita2)
    bar=fita2.findMaxPossibleMatches(fita1)
    fita1D=dict()
    fita1D["MAX"]=(foo[0][0])
    fita1D["RES"]=foo[0][1] if foo[0][1]!=0 else fita1.strand.lower()
    fita1D["MOV"]=(foo[1])
    fita2D=dict()
    fita2D["MAX"]=(bar[0][0])
    fita2D["RES"]=(bar[0][1] if bar[0][1]!=0 else fita2.strand.lower())
    fita2D["MOV"]=(bar[1])
    retorno={"MOV":fita1D["MOV"], "fita1":fita1D["RES"], "fita2":fita2D["RES"]}
    return retorno
    
def reset():
    lista[0]=120
    lista[1]=0
    lb_fita_2.place(x=lista[0], y=180)
    bt_click_move(0)
    return lista

def posRelativa(num, h=0):
    x, y = janela.winfo_width(), janela.winfo_height()
    if not(x):
        x, y=400, 400
    if h:
        return int(y*num)
    return int(x*num)

#Aula 5
janela = Tk()
telas={"Complemento":True, "Credits":False, 'geometry':"400x400+200+200"}

#Botões
##Botões de movimento
y_mov=100
bt_left=Button(janela, width=12, text="<< Left")
bt_left['command']=partial(bt_click_move, -1)
bt_left.place(x=50, y=y_mov)
bt_right=Button(janela, width=12, text="Right >>", command=bt_click_move)
bt_right.place(x=180, y=y_mov)
bt_reset=Button(janela, width=2, text="R", command=reset)
bt_reset.place(x=150, y=y_mov)

## Botões para ajuste da fonte
bt_letra_maior=Button(janela, width=3, text="cls")
bt_letra_maior.place(x=20, y=140)
bt_letra_maior['command']=partial(print, '\n'*42)
bt_letra_menor=Button(janela, width=2, text="ɔɔ", command=bt_credits)
bt_letra_menor.place(x=posRelativa(0.8), y=posRelativa(0.8, 1))
#bt_letra_menor['command']=partial(bt_size, i=-1, step=1)


## Botões para ajuste dos passos
bt_Complement=Button(janela, width=2, text="CC", bg='blue')
bt_Complement.place(x=120, y=70)
bt_Complement['command']=partial(bt_complement)
bt_MelhorCaso=Button(janela, width=2, text="MC", bg='red')
bt_MelhorCaso.place(x=150, y=70)
bt_MelhorCaso['command']=partial(bt_max_possibilities)


#Botões para entrada de dado
bt_new=Button(janela, width=2, text="OK", command=bt_clickOk)
bt_new.place(x=20, y=70)
bt_shuffle=Button(janela, width=7, text="SHUFFLE", command=bt_click_shuffle)
bt_shuffle.place(x=50, y=70)

#Texto
#lb=Label(janela, text="Teste")
#lb.place(x=10, y=20)
conteudos=["AGTCCA", "TTC"]
lista=[120, 0]
fonte=["Fixedsys", 5, 25]
lb_fita_1=Label(janela, font=(fonte[0], fonte[1]**2), text=conteudos[0])
lb_fita_2=Label(janela, font=(fonte[0], fonte[1]**2), text=conteudos[1])
lb_fita_1.place(x=120, y=130)
lb_fita_2.place(x=lista[0], y=180)



#Entradas
ed1 = Entry(janela, width=30)
ed1.place(x=20, y=20)
ed2 = Entry(janela, width=30)
ed2.place(x=20, y=50)

textoCreditos="""\n\n\n\n\n\nProgramação de Interfaces Graficas\n
Professor: Paulo Roma
Feito por: Lucas Romer\n
Linguagem utilizada: Python 3.6 + TKinter\n
Eventualmente disponível em https://github.com/romerlrl/

                """
lb_credits=Label(janela, font=("Arial", 12), background="purple", width=1, height=1, text=textoCreditos)
lb_credits.place(x=5, y=5)


print(janela.winfo_width(), janela.winfo_height())
# width x height + left + top
janela.geometry(telas['geometry'])

print(janela.winfo_width(), janela.winfo_height())
janela.mainloop()

