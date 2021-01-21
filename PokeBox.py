import win32com.client
import sqlite3
import os
import time
from tkinter import *
from tkinter import ttk
from AutoCompleteCombox import AutocompleteCombobox
from tkinter import messagebox
from PIL import ImageTk, Image

from HashMapAllPokemon import *

#Variable Estandar
nameDB= "PokeBoxDataBase"
nameAPP= "PokeBox"
backgroundColor="#112239"
actualSearch=""
actualSetup=""

#Listass de información
allgames=allGames()
allPokemonlist=allPokemon()
allTypesList=allTypes()
allPokemonName=[]
for i in allPokemonlist:
    allPokemonName.append(i[0])

#Encuentra MyDocuments del usuario y crea la carpeta "PokeBox"
objShell = win32com.client.Dispatch("WScript.Shell")
myDocuments = objShell.SpecialFolders("MyDocuments")
myDocuments += ("\\" + nameAPP)

#Crear Carpeta en Documentos
if not (os.path.exists(myDocuments)):
    os.makedirs(myDocuments)

#Crea la database en la ruta especificada
nameDataBase = myDocuments + "\\" 
nameDataBase += nameDB + ".db"
print(nameDataBase)
con = sqlite3.connect(nameDataBase)

c = con.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS pokemonDB (
    pokemon text,
    nickname text,
    gender text,
    type1 text,
    type2 text,
    ivs integer,
    evs integer,
    shiny integer,
    game text)""")

con.commit()
con.close()

#Crear Ventana
root = Tk()
root.title(nameAPP)
app_weight = 790
app_height = 430
screen_weight = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(str(app_weight)+"x"+str(app_height)+"+"+str(int(screen_weight/2 - app_weight/2))+"+"+str(int(screen_height/2 - app_height/2)))
root.resizable(False,False)
root.configure(background=backgroundColor)


#Cambiar Estilo Ventana
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
background="#474F5B",
foreground="white",
fieldbackground="#333942",
rowheight=25)

style.map("Treeview", background=[("selected","#0D1521")],foreground=[("selected","silver")])
style.configure("Treeview.Heading",
background="#9AA5B4",
font=(None,9 ,"bold"))

#Crear Frame Tabla
tree_frame = Frame(root)
tree_frame.grid(row=0,column=0,rowspan=7, padx=15,pady=5)

#Crear ScrollBar
tree_scrollbar = Scrollbar(tree_frame)
tree_scrollbar.pack(side=RIGHT, fill=Y)

#Crear tabla y definir columnas
my_tree = ttk.Treeview(tree_frame, yscrollcommand = tree_scrollbar.set)
tree_scrollbar.configure(command=my_tree.yview)
my_tree['columns'] = ("Pokemon","Nickname","Gender","Type 1","Type 2","Competitive IV","Full EVs","Shiny","Stored In")

#Formato Columnas
my_tree.column("#0", width = 0, stretch=NO)
my_tree.column("Pokemon", anchor=W, width=115, minwidth=115)
my_tree.column("Nickname", anchor=W,width=105, minwidth=40)
my_tree.column("Gender", anchor=W,width=50, minwidth=50)
my_tree.column("Type 1", anchor=CENTER,width=55, minwidth=55)
my_tree.column("Type 2", anchor=CENTER,width=55, minwidth=55)
my_tree.column("Competitive IV", anchor=CENTER,width=88, minwidth=88)
my_tree.column("Full EVs", anchor=CENTER,width=48, minwidth=48)
my_tree.column("Shiny", anchor=CENTER,width=40, minwidth=40)
my_tree.column("Stored In", anchor=E,width=100, minwidth=100)

#Formato Heading
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Pokemon", text="Pokemon", anchor=W,command=lambda: updateTreeview("pokemon"))
my_tree.heading("Nickname", text="Nickname", anchor=W,command=lambda: updateTreeview("nickname"))
my_tree.heading("Gender", text="Gender", anchor=W,command=lambda: updateTreeview("gender"))
my_tree.heading("Type 1", text="Type 1", anchor=W,command=lambda: updateTreeview("type1"))
my_tree.heading("Type 2", text="Type 2", anchor=W,command=lambda: updateTreeview("type2"))
my_tree.heading("Competitive IV", text="Competitive IV", anchor=W,command=lambda: updateTreeview("ivs DESC"))
my_tree.heading("Full EVs", text="Full EVs", anchor=W,command=lambda: updateTreeview("evs DESC"))
my_tree.heading("Shiny", text="Shiny", anchor=W,command=lambda: updateTreeview("shiny DESC"))
my_tree.heading("Stored In", text="Stored In", anchor=E,command=lambda: updateTreeview("game"))

my_tree.pack()

#Contador de tuplas
count_frame = Frame(root)
count_frame.grid(row=8,column=0, padx=10)
count_frame.configure(background=backgroundColor)

count_label_space = Label(count_frame,text="",background=backgroundColor)
count_label_space.grid(row=0,column=0, padx=240)

count=0
count_label = Label(count_frame,text="N° Pokemon: "+str(count),background=backgroundColor, fg="white", font=(None,10,"bold"))
count_label.grid(row=0,column=1)

#All Database con filtro y ordenado con order -> Treeview
def updateTreeview(order="pokemon"):
    con = sqlite3.connect(nameDataBase)
    c = con.cursor()
    c.execute("SELECT *, oid FROM  pokemonDB "+actualSearch+" ORDER BY "+order+", pokemon")
    data = c.fetchall()
    my_tree.delete(*my_tree.get_children())
    global count
    count=0
    for i in data:
        count +=1
        var = ""
        var2 = ""
        var3 = ""
        if(i[5]==1):
            var = "✓"    
        if(i[6]==1):
            var2 = "✓"
        if(i[7]==1):
            var3 = "✓"
        my_tree.insert(parent='',index='end', iid=i[9], text="", values=(i[0],i[1],i[2],i[3],i[4],var,var2,var3,i[8]))        
    con.close()
    count_label.configure(text="N° Pokemon: "+str(count))
    time.sleep(0)

#All Database -> Treeview
def updateAllTreeview(order="pokemon"):
    con = sqlite3.connect(nameDataBase)
    c = con.cursor()
    c.execute("SELECT *, oid FROM  pokemonDB ORDER BY "+order)
    data = c.fetchall()
    my_tree.delete(*my_tree.get_children())        
    global count
    count = 0
    for i in data:
        count+=1
        var = ""
        var2 = ""
        var3 = ""
        if(i[5]==1):
            var = "✓"    
        if(i[6]==1):
            var2 = "✓"
        if(i[7]==1):
            var3 = "✓"
        my_tree.insert(parent='',index='end', iid=i[9], text="", values=(i[0],i[1],i[2],i[3],i[4],var,var2,var3,i[8]))        
    con.close()
    count_label.configure(text="N° Pokemon: "+str(count))


#Frame de botones
frame_buttons = Frame(root)
frame_buttons.grid(row = 9, column=0)
frame_buttons.configure(background=backgroundColor)

#Remueve el menu actual
def RemoveinGrid():
    for item in frame_buttons.winfo_children():
        item.destroy()

#Arregla el nombre entregado del usuario para aumentar compatibilidad
#sgl=true para que el return sea compatible con los comandos sql
def pokemonNameFix(name,sql=False):
    pokemon_var = ""
    for i in name.rstrip().lstrip().title():
        if (i.isalpha()):
            pokemon_var += i
        elif (i == " "):
            pokemon_var += i
        elif (i.isnumeric()):
            pokemon_var += i
        elif (i == "'" and sql):
            pokemon_var += "''"
        elif (i == "'" and sql==False):
            pokemon_var += "'"
        elif (i == "-"):
            pokemon_var += "-"
    return pokemon_var

#Añade los campos para añadir pokemon
def addSetup():
    RemoveinGrid()

    cbox_label = Label(frame_buttons,text="Pokemon:")
    cbox_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    cbox_label.grid(row=1,column=0)

    nickname_label = Label(frame_buttons,text="Nickname:")
    nickname_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    nickname_label.grid(row=1,column=2)

    gender_label = Label(frame_buttons,text="Gender")
    gender_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    gender_label.grid(row=3,column=2)

    ivs_label = Label(frame_buttons,text="IVs")
    ivs_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    ivs_label.grid(row=2,column=4)

    evs_label = Label(frame_buttons,text="EVs")
    evs_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    evs_label.grid(row=2,column=5, padx=5)

    shiny_label = Label(frame_buttons,text="Shiny")
    shiny_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    shiny_label.grid(row=2,column=6, padx=5)

    store_label = Label(frame_buttons,text="Store In:")
    store_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    store_label.grid(row=3,column=0, padx=5)

    cbox = AutocompleteCombobox(frame_buttons, width=18)
    cbox.set_completion_list(allPokemonName)
    cbox.grid(row=2,column=0, padx=5)
    cbox.configure(font=(None,10,"bold"))
    
    nickname = Entry(frame_buttons, width=18)
    nickname.grid(row=2,column=2,padx=5)
    nickname.configure(font=(None,10,"bold"))

    gender = StringVar()

    gender_menu = OptionMenu(frame_buttons,gender, "", "♂","♀")
    gender_menu.configure(bg="white", activebackground='gray',activeforeground="white", padx=1, width=4, highlightthickness=0)
    gender_menu.grid(row=4,column=2, padx=5)

    ivs = IntVar()
    evs = IntVar()
    shiny = IntVar()

    iv_check = Checkbutton(frame_buttons,variable=ivs )
    iv_check.configure(bg=backgroundColor, activebackground = backgroundColor)
    iv_check.grid(row=3,column=4,padx=10)

    ev_check = Checkbutton(frame_buttons,variable=evs )
    ev_check.configure(bg=backgroundColor, activebackground = backgroundColor)
    ev_check.grid(row=3,column=5)

    shiny_check = Checkbutton(frame_buttons,variable=shiny )
    shiny_check.configure(bg=backgroundColor, activebackground = backgroundColor)
    shiny_check.grid(row=3,column=6)

    iv_check.deselect()
    ev_check.deselect()
    shiny_check.deselect()

    cbox_store = AutocompleteCombobox(frame_buttons, width=18)
    cbox_store.set_completion_list(allgames)
    cbox_store.grid(row=4,column=0,padx=5)
    cbox_store.configure(font=(None,10,"bold"))

    #Función para añadir pokemon al TreeView y Database    
    def addPokemon():
        global count
        
        pokemon_var = pokemonNameFix(cbox.get())
        
        if pokemon_var not in allPokemonName:
            cbox.delete(0,END)
            messagebox.showerror("Error","Pokemon name doesn't exist or misspelled")
            return
        if (len(nickname.get())>15):
            nickname.delete(0,END)
            messagebox.showerror("Error","Nickname is too long (MAX: 15)")
            return
        if cbox_store.get().rstrip().lstrip().title() not in allgames:
            print(cbox_store.get().rstrip().lstrip().title())
            cbox_store.delete(0,END)
            messagebox.showerror("Error","Game name doesn't exist or misspelled")
            return

        i = allPokemonName.index(pokemon_var)
        type1ADD = allPokemonlist[i][1]
        type2ADD = allPokemonlist[i][2]

        nicknameAdd=""
        
        for i in nickname.get():
            if(i=="'"):
                nicknameAdd += "ˈ"
            else:
                nicknameAdd += i

        con = sqlite3.connect(nameDataBase)
        c = con.cursor()
        c.execute("INSERT INTO pokemonDB VALUES (:pokemon, :nickname, :gender, :type1, :type2, :ivs, :evs, :shiny, :game)",
        {"pokemon" : pokemon_var,
        "nickname" : nicknameAdd,
        "gender" : gender.get(),
        "type1" : type1ADD,
        "type2" : type2ADD,
        "ivs" : ivs.get(),
        "evs" : evs.get(),
        "shiny" : shiny.get(),
        "game" : cbox_store.get()} 
        )
  
        c.execute("SELECT MAX(oid) FROM pokemonDB")
                
        var = ""
        var2 = ""
        var3 = ""
        if(ivs.get()==1):
            var = "✓"        
        if(evs.get()==1):
            var2 = "✓"
        if(shiny.get()==1):
            var3 = "✓"
        
        my_tree.insert(parent='',index=0, iid=(c.fetchone()[0]), text="", values=(pokemon_var,nicknameAdd,gender.get(),type1ADD,type2ADD,var,var2,var3,cbox_store.get().rstrip().lstrip().title()))
        
        cbox.delete(0,END)
        nickname.delete(0,END)
        #cbox_store.delete(0,END)
        iv_check.deselect()
        ev_check.deselect()
        shiny_check.deselect()
        gender.set("")

        con.commit()
        con.close()
        count+=1
        count_label.configure(text="N° Pokemon: "+str(count))


    final_add_button = Button(frame_buttons, text="Add",command=addPokemon)
    final_add_button.grid(row=3,column=7,padx=5)
    final_add_button.configure(font=(None,12,"bold"), bg="#9AA5B4", activebackground='#3B434D',activeforeground="white", width=7)

    
    updateAllTreeview()

#Función para eliminar pokemon al TreeView y Database    
def delPokemon():
    con = sqlite3.connect(nameDataBase)
    c = con.cursor()
    global count
    for i in my_tree.selection():
        count-=1
        my_tree.delete(i)
        c.execute("DELETE FROM pokemonDB WHERE oid="+"'"+i+"'")
        con.commit()
    con.close    
    count_label.configure(text="N° Pokemon: "+str(count))

#Añade los campos para buscar pokemon
def searchSetup():
    RemoveinGrid()

    cbox_label = Label(frame_buttons,text="Pokemon:")
    cbox_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    cbox_label.grid(row=0,column=0)

    nickname_label = Label(frame_buttons,text="Nickname:")
    nickname_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    nickname_label.grid(row=3,column=0, padx=5)

    type1_label = Label(frame_buttons,text="Type 1:")
    type1_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    type1_label.grid(row=0,column=1)

    type2_label = Label(frame_buttons,text="Type 2:")
    type2_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    type2_label.grid(row=3,column=1, padx=5)

    gender_label = Label(frame_buttons,text="Gender")
    gender_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    gender_label.grid(row=3,column=4)

    ivs_label = Label(frame_buttons,text="IVs")
    ivs_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    ivs_label.grid(row=0,column=2)

    evs_label = Label(frame_buttons,text="EVs")
    evs_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    evs_label.grid(row=0,column=3)

    shiny_label = Label(frame_buttons,text="Shiny")
    shiny_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    shiny_label.grid(row=0,column=4)

    store_label = Label(frame_buttons,text="Store In:")
    store_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    store_label.grid(row=3,column=2, padx=5, columnspan=2)

    cbox = AutocompleteCombobox(frame_buttons, width=18)
    cbox.set_completion_list(allPokemonName)
    cbox.grid(row=1,column=0)
    cbox.configure(font=(None,10,"bold"))
    
    nickname = Entry(frame_buttons, width=20)
    nickname.grid(row=4,column=0,padx=5)
    nickname.configure(font=(None,10,"bold"))

    ivs = StringVar()
    evs = StringVar()
    shiny = StringVar()
    gender = StringVar()

    gender_menu = OptionMenu(frame_buttons,gender,  "", "♂","♀" )
    gender_menu.configure(bg="#9AA5B4", activebackground='#3B434D',activeforeground="white", padx=1, width=4, highlightthickness=0)
    gender_menu.grid(row=4,column=4, padx=2)

    iv_menu = OptionMenu(frame_buttons,ivs, "", "Yes","No" )
    iv_menu.configure(bg="#9AA5B4", activebackground='#3B434D',activeforeground="white", padx=1, width=4, highlightthickness=0)
    iv_menu.grid(row=1,column=2, padx=2)

    ev_menu = OptionMenu(frame_buttons,evs, "", "Yes","No" )
    ev_menu.configure(bg="#9AA5B4", activebackground='#3B434D',activeforeground="white", padx=1, width=4, highlightthickness=0)
    ev_menu.grid(row=1,column=3, padx=2)

    shiny_menu = OptionMenu(frame_buttons,shiny, "", "Yes","No" )
    shiny_menu.configure(bg="#9AA5B4", activebackground='#3B434D',activeforeground="white", padx=1, width=4, highlightthickness=0)
    shiny_menu.grid(row=1,column=4, padx=2)

    ivs.set("")
    evs.set("")
    shiny.set("")
    gender.set("")

    cbox_store = AutocompleteCombobox(frame_buttons, width=14)
    cbox_store.set_completion_list(allgames)
    cbox_store.grid(row=4,column=2, columnspan=2)
    cbox_store.configure(font=(None,10,"bold"))

    cbox_type1 = AutocompleteCombobox(frame_buttons, width=15)
    cbox_type1.set_completion_list(allTypesList)
    cbox_type1.grid(row=1,column=1,padx=10)
    cbox_type1.configure(font=(None,10,"bold"))

    cbox_type2 = AutocompleteCombobox(frame_buttons, width=15)
    cbox_type2.set_completion_list(allTypesList)
    cbox_type2.grid(row=4,column=1)
    cbox_type2.configure(font=(None,10,"bold"))

    #Función para buscar pokemon al TreeView y Database    
    def searchPokemon():
        datos=[]
        pokemonSearch = pokemonNameFix(cbox.get(),True)
        nicknameSearch=""
        type1Search=cbox_type1.get().rstrip().lstrip().title()
        type2Search=cbox_type2.get().rstrip().lstrip().title()
        gameSearch= pokemonNameFix(cbox_store.get(),True)

        for i in nickname.get():
            if(i=="'"):
                nicknameSearch += "ˈ"
            else:
                nicknameSearch += i

        if(pokemonSearch!=""):
            datos.append(" pokemon = '" + pokemonSearch + "' ")
        if(nicknameSearch!=""):
            datos.append(" nickname = '" + nicknameSearch + "' ")
        if(type1Search!=""):
            if(type2Search!=""):
                datos.append("( type1 = '" + type1Search + "' OR  type2 = '"+type1Search+"' OR type2 = '" + type2Search + "' OR  type1 = '"+type2Search+"' ) AND NOT type2='' ")
            else:
                datos.append(" type1 = '" + type1Search + "' OR type2 = '"+type1Search+"' ")
        if(type2Search!=""):
            datos.append(" type2 = '" + type2Search + "' OR type1 = '"+type2Search+"' ")
        if(gameSearch!=""):
            datos.append(" game = '" + gameSearch + "' ")
        if(ivs.get()!=""):
            if(ivs.get()=="Yes"):
                datos.append(" ivs = 1 ")
            else:
                datos.append(" ivs = 0 ")
        if(evs.get()!=""):
            if(evs.get()=="Yes"):
                datos.append(" evs = 1 ")
            else:
                datos.append(" evs = 0 ")
        if(shiny.get()!=""):
            if(shiny.get()=="Yes"):
                datos.append(" shiny = 1 ")
            else:
                datos.append(" shiny = 0 ")
        if(gender.get()!=""):
            datos.append(" gender = '"+ gender.get() +"' ")
        
        if(len(datos)==0):
            updateAllTreeview()
            return

        datos = " and ".join(datos)
        global actualSearch
        actualSearch="Where "+datos        

        updateTreeview()

    
    search_button = Button(frame_buttons,text="Search", font=(None,14,"bold"),
    bg="#9AA5B4", activebackground='#3B434D',activeforeground="white", command=searchPokemon)
    search_button.grid(row=0,column=5, rowspan=2, padx=20)

    showAll_button = Button(frame_buttons,text="Show All", font=(None,12,"bold"),
    bg="#9AA5B4", activebackground='#3B434D',activeforeground="white", command=updateAllTreeview)
    showAll_button.grid(row=3,column=5, rowspan=2, padx=20)

#Añade los campos para actualizar pokemon
def updateSetup(e):
    selected_id = my_tree.focus()
    values = my_tree.item(selected_id,"values")

    #Ver si no se esta haciendo doble click en un heading
    try:
        values[0]
    except:
        return

    RemoveinGrid()

    cbox_label = Label(frame_buttons,text="Pokemon:")
    cbox_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    cbox_label.grid(row=1,column=0)

    nickname_label = Label(frame_buttons,text="Nickname:")
    nickname_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    nickname_label.grid(row=1,column=2)

    gender_label = Label(frame_buttons,text="Gender")
    gender_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    gender_label.grid(row=3,column=2)

    ivs_label = Label(frame_buttons,text="IVs")
    ivs_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    ivs_label.grid(row=2,column=4)

    evs_label = Label(frame_buttons,text="EVs")
    evs_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    evs_label.grid(row=2,column=5, padx=5)

    shiny_label = Label(frame_buttons,text="Shiny")
    shiny_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    shiny_label.grid(row=2,column=6, padx=5)

    store_label = Label(frame_buttons,text="Store In:")
    store_label.configure(font=(None,12,'bold'),bg=backgroundColor,fg="Silver")
    store_label.grid(row=3,column=0, padx=5)

    cbox = AutocompleteCombobox(frame_buttons, width=18)
    cbox.set_completion_list(allPokemonName)
    cbox.grid(row=2,column=0, padx=5)
    cbox.configure(font=(None,10,"bold"))
    cbox.insert(0,values[0])
    
    nickname = Entry(frame_buttons, width=18)
    nickname.grid(row=2,column=2,padx=5)
    nickname.configure(font=(None,10,"bold"))
    nickname.insert(0,values[1])
    
    ivs = IntVar()
    evs = IntVar()
    shiny = IntVar()
    gender = StringVar()

    gender_menu = OptionMenu(frame_buttons,gender, "", "♂","♀")
    gender_menu.configure(bg="white", activebackground='gray',activeforeground="white", padx=1, width=4, highlightthickness=0)
    gender_menu.grid(row=4,column=2, padx=5)
    gender.set(values[2])

    iv_check = Checkbutton(frame_buttons,variable=ivs)
    iv_check.configure(bg=backgroundColor, activebackground = backgroundColor)
    iv_check.grid(row=3,column=4,padx=10)

    ev_check = Checkbutton(frame_buttons,variable=evs )
    ev_check.configure(bg=backgroundColor, activebackground = backgroundColor)
    ev_check.grid(row=3,column=5)

    shiny_check = Checkbutton(frame_buttons,variable=shiny )
    shiny_check.configure(bg=backgroundColor, activebackground = backgroundColor)
    shiny_check.grid(row=3,column=6)    

    if(values[5]==""):
        iv_check.deselect()
    else:
        iv_check.select()
        
    if(values[6]==""):
        ev_check.deselect()
    else:
        ev_check.select()

    if(values[7]==""):
        shiny_check.deselect()
    else:
        shiny_check.select()

    cbox_store = AutocompleteCombobox(frame_buttons, width=18)
    cbox_store.set_completion_list(allgames)
    cbox_store.grid(row=4,column=0,padx=5)
    cbox_store.configure(font=(None,10,"bold"))
    cbox_store.insert(0,values[8])

    #Función para actualizar pokemon al TreeView y Database    
    def updatePokemon():
        nicknameUpdate=""
        gameUpdate=pokemonNameFix(cbox_store.get())
        gameUpdate2=pokemonNameFix(cbox_store.get(),True)

        pokemon_var = pokemonNameFix(cbox.get())
        pokemon_var2 = pokemonNameFix(cbox.get(),True)

        for i in nickname.get():
            if(i=="'"):
                nicknameUpdate += "ˈ"
            else:
                nicknameUpdate += i
        
        if pokemon_var not in allPokemonName:
            cbox.delete(0,END)
            cbox.insert(0,values[0])
            messagebox.showerror("Error","Pokemon name doesn't exist or misspelled")
            return
        if (len(nicknameUpdate)>15):
            nickname.delete(0,END)
            nickname.insert(0,values[1])
            messagebox.showerror("Error","Nickname is too long (MAX: 15)")
            return
        if gameUpdate not in allgames:
            cbox_store.delete(0,END)
            cbox_store.insert(0,values[8])
            messagebox.showerror("Error","Game name doesn't exist or misspelled")
            return

        i = allPokemonName.index(pokemon_var)
        type1ADD = allPokemonlist[i][1]
        type2ADD = allPokemonlist[i][2]

        var = ""
        var2 = ""
        var3 = ""
        if(ivs.get()==1):
            var = "✓"        
        if(evs.get()==1):
            var2 = "✓"
        if(shiny.get()==1):
            var3 = "✓"
        my_tree.item(selected_id,text="",values=(pokemon_var,nicknameUpdate,gender.get(),type1ADD,type2ADD,var,var2,var3,gameUpdate))
        con = sqlite3.connect(nameDataBase)
        c = con.cursor()
        c.execute("UPDATE pokemonDB SET pokemon = '"+pokemon_var2+"', nickname = '"+nicknameUpdate+"', type1 = '"
        +type1ADD+"', type2 = '"+type2ADD+"', ivs = "+str(ivs.get())+" , evs = "+str(evs.get())+" , shiny = "+str(shiny.get())
        +" , game = '"+gameUpdate2+"', gender = '"+gender.get()+"' WHERE oid = "+str(selected_id))
        con.commit()
        con.close()
        

    update_button = Button(frame_buttons, text="Update",command=updatePokemon)
    update_button.grid(row=3,column=8,columnspan=2)
    update_button.configure(font=(None,11,"bold"), bg="#9AA5B4", activebackground='#3B434D',activeforeground="white", width=8)


#Cuadro de info
def infoBox():
    messagebox.showinfo("Info","""
    Add Pokemon:
    Press \"Add\" to open the menu to add pokemon.
    Then fill in the fields to add a pokemon to the database.
    
    Edit Pokemon:
    Para actualizar la informacion de un pokemon debes hacer 
    doble clic sobre el pokemon para abrir el menu de edicion.
    
    Delete Pokemon:
    If you press the \"Delete\" all selected pokemon will be
    deleted.
    (To select several, hold down \"Control\")
    
    Search Pokemon:
    To open the search menu press the \"Search\" botton on the
    right side.
    Fill in the fields that you consider important to filter
    
    Save Data:
    The information of the app is saved in Documents/PokeBox
    
    Games Includes:
    All from 3DS, Switch and Bank
    
    Creator:
    Tomas Secul (AlphaGuilty)
    
    Contact:
    alphaguiltycode@gmail.com """ )


#Botones
add_button = Button(root,text= "Add", command= addSetup,
 bg="#9AA5B4", activebackground='#3B434D',activeforeground="white",font=(None,15),width=6)
add_button.grid(row=0,column=1,sticky="E",rowspan=1)

del_botton = Button(root,text= "Delete", command= delPokemon,
 bg="#9AA5B4", activebackground='#3B434D',activeforeground="white",font=(None,15), width=6)
del_botton.grid(row=2,column=1, sticky="E",rowspan=1)

ser_botton = Button(root,text="Search", command= searchSetup,
 bg="#9AA5B4", activebackground='#3B434D',activeforeground="white",font=(None,15),width=6)
ser_botton.grid(row=4,column=1, sticky="E",rowspan=1)

upd_botton = Button(root,text= "?", command= infoBox,
 bg="#9AA5B4", activebackground='#3B434D',activeforeground="white", width=4,font=(None,10))
upd_botton.grid(row=6,column=1, sticky="N",rowspan=1)

#Funcion doble clic
my_tree.bind("<Double-1>", updateSetup)

#Colocar todos los datos
updateTreeview()
searchSetup()
root.mainloop()

