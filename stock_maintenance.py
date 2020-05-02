import sqlite3
from sqlite3 import Error
from tkinter import messagebox
from PIL import ImageTk,Image
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from Database_Manager import Stock
import re,csv

DATABASE = "Inventory_Mgt.db"

#------------------------------------------------------------------------------------

root =Tk()
root.geometry("600x500")
root.title("Inventory Management")

db = Stock(DATABASE)
conn = db.create_connection()
cursor = db.get_cursor()

bg_Image = PhotoImage(file=r"images/stock2.gif")
bg_label = Label(root,image=bg_Image)
bg_label.place(x=0,y=0,relwidth=1,relheight=1)





#------------------------------------------------------------------------------------
#all functions

#view all stock items,search and delete them
def list_items():
    
    all_Items = Toplevel()
    all_Items.geometry("1060x530")
    all_Items.title("ITEMS")
    style = ttk.Style()
    
    style.configure("Treeview",font="helvetica 9 bold",rowheight=45,foreground="darkgrey",background="black")
    style.configure("Treeview.Heading",font="helvetica 13 bold")
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    stockView = ttk.Treeview(all_Items)
    stockView['columns']=['model','name','category','company','qty','price','total']
    stockView.grid(row=1,column=1)

    verscrlbar = ttk.Scrollbar(all_Items, orient ="vertical",  command = stockView.yview) 
    verscrlbar.grid(row=1,column=0,ipadx=2)
    stockView.configure(xscrollcommand = verscrlbar.set) 
    
    search = Entry(all_Items,width = 40,justify="center",font="helvetica 9 bold",bd=5,fg="grey",bg="#f1f1f1",relief="sunken")
    search.grid(row=0,column=1,pady=5,ipady=5,sticky="w")
    search.insert(0,"SEARCH YOUR ITEM")
    #search.focus()
    
    #CATEGORY COMBOBOX
    cursor.execute("SELECT category from Item")
    Item_Category = cursor.fetchall()
    Item_Category = [item[0] for item in Item_Category ]
    Item_Category = list(set(Item_Category))
    
    categoryCombo = ttk.Combobox(all_Items,value=Item_Category,justify="center",state="readonly",font="helvetica 9 bold",foreground="grey")
    categoryCombo.current(0)
    categoryCombo.place(x=420,y=5,relheight=0.055)

    #COMPANIES COMBOBOX
    cursor.execute("SELECT company from Item")
    companies = cursor.fetchall()
    companies = [item[0] for item in companies ]
    companies = list(set(companies))
    
    companyCombo = ttk.Combobox(all_Items,value=companies,justify="center",state="readonly",font="helvetica 9 bold",foreground="grey")
    companyCombo.current(0)
    companyCombo.place(x=700,y=5,relheight=0.055)

    # columns in table item : ['id', 'name', 'category', 'company', 'quantity', 'price']
    columns = db.get_Columns("Item")
    print(columns)

    stockView.heading("#0",text="",anchor="w")
    stockView.column("#0",anchor="center",width=1,stretch=False)

    stockView.heading("model",text="Model No",anchor="center",command= lambda: filter(columns[0]))
    stockView.column("model",anchor="center",width=120,minwidth=120,stretch=NO)

    stockView.heading("name",text="Item",anchor="center",command= lambda: filter(columns[1]))
    stockView.column("name",anchor="center",width=200,minwidth=190)

    stockView.heading("category",text="Category",anchor="center",command= lambda: filter(columns[2]))
    stockView.column("category",anchor="center",width=200,minwidth=190)
    
    stockView.heading("company",text="Company",anchor="center",command= lambda: filter(columns[3]))
    stockView.column("company",anchor="center",width=150,minwidth=140)
    
    stockView.heading("qty",text="Quantity",anchor="center",command= lambda: filter(columns[4]))
    stockView.column("qty",anchor="center",width=100,minwidth=90)
    
    stockView.heading("price",text="Price",anchor="center",command= lambda: filter(columns[5]))
    stockView.column("price",anchor="center",width=120,minwidth=120)
    
    stockView.heading("total",text="Total",anchor="center")
    stockView.column("total",anchor="center",width=160,minwidth=160)

    def removeChild():
        remove = stockView.get_children()
        for child in remove:
            stockView.delete(child)

    def show_all_data():
        #showing data in he treeview
        removeChild()
        cursor.execute("SELECT * from Item")
        myresult = cursor.fetchall()
        for i in myresult:
            stockView.insert("","end",text="",values=(i[0],i[1].upper(),i[2].upper(),i[3].upper(),i[4],i[5],float(i[4]*i[5])))
    

    #filtering data when heading is clicked
    def filter(field):
        removeChild()
        cursor.execute("SELECT * from Item ORDER BY %s"%(field))
        result = cursor.fetchall()
        for i in result:
            stockView.insert("","end",text="",values=(i[0],i[1].upper(),i[2].upper(),i[3].upper(),i[4],i[5],float(i[4]*i[5])))

    def search_Db(event):
        removeChild()
        #print(event.keysym)
        value = search.get()
        #print("value=",value)
        if(value == ""):
            show_all_data()
        else:
            cursor.execute("SELECT * from Item where name LIKE '%{}%' OR id LIKE '%{}%'".format(value,value))
            result = cursor.fetchall()
            for i in result:
                stockView.insert("","end",text="",values=(i[0],i[1].upper(),i[2].upper(),i[3].upper(),i[4],i[5],float(i[4]*i[5])))

    def search_category(event):
        removeChild()
        cursor.execute("SELECT* From Item WHERE category='%s' ORDER BY price"%(categoryCombo.get()))
        result = cursor.fetchall()
        for i in result:
            stockView.insert("","end",text="",values=(i[0],i[1].upper(),i[2].upper(),i[3].upper(),i[4],i[5],float(i[4]*i[5])))
    
    def search_company(event):

        removeChild()
        cursor.execute("SELECT* From Item WHERE company='%s' ORDER BY price"%(companyCombo.get()))
        result = cursor.fetchall()
        for i in result:
            stockView.insert("","end",text="",values=(i[0],i[1].upper(),i[2].upper(),i[3].upper(),i[4],i[5],float(i[4]*i[5])))

    def deleteRow(event):
        items = stockView.selection()
        print(items)
        itemData=[]
        for i in items:
            itemData.append(stockView.item(i)['values'])
        print("Delete -> ",itemData)
        
        cursor.execute("DELETE from Item WHERE id='%s'"%(itemData[0][0]))
        conn.commit()
        messagebox.showinfo("Deletion Message","Successfully Deleted")
        show_all_data()

    view_img = PhotoImage(file=r"images/view2.png").subsample(23,23)
    all_item_btn=Button(all_Items,text="View All",image=view_img,command=show_all_data)
    all_item_btn.place(x=1020,y=7)

    show_all_data()
    stockView.bind("<Delete>",deleteRow)

    search.bind("<Key>",search_Db)
    search.bind("<FocusIn>",lambda args: search.delete('0','end'))
    search.bind("<FocusOut>",lambda args: search.insert('0','SEARCH YOUR ITEM'))

    categoryCombo.bind("<<ComboboxSelected>>",search_category)
    companyCombo.bind("<<ComboboxSelected>>",search_company)
    all_Items.resizable(0,0)
    all_Items.mainloop()


def insert_item():

    insert_frame = Toplevel(bg="lightgrey")
    insert_frame.title("Insert Your Item")
    insert_frame.geometry("520x550")

    insertImg = PhotoImage(file="images/insert.png").subsample(4,4)
    updateImg = PhotoImage(file="images/update.png").subsample(12,12)
    apple = PhotoImage(file="images/apple.png").subsample(13,13)
    headphones = PhotoImage(file="images/headphones.png").subsample(13,13)
    iron = PhotoImage(file="images/press.png").subsample(12,12)
    Laptop = PhotoImage(file="images/laptop.png").subsample(14,14)
    fridge = PhotoImage(file="images/fridge.png").subsample(14,14)
    w_machine = PhotoImage(file="images/machine.png").subsample(14,14)
    delete_img = PhotoImage(file="images/delete.png").subsample(29,29)



    Label(insert_frame,image=insertImg,bg="lightgrey").place(x=120,y=5)
    Label(insert_frame,image=updateImg,bg="lightgrey").place(x=410,y=6)
    Label(insert_frame,image=apple,bg="lightgrey").place(x=440,y=337)
    Label(insert_frame,image=headphones,bg="lightgrey").place(x=440,y=140)
    Label(insert_frame,image=iron,bg="lightgrey").place(x=440,y=205)
    Label(insert_frame,image=Laptop,bg="lightgrey").place(x=443,y=277)
    Label(insert_frame,image=fridge,bg="lightgrey").place(x=445,y=80)
    Label(insert_frame,image=w_machine,bg="lightgrey").place(x=443,y=410)

    heading = Label(insert_frame,text="Insert / Update",font="helvetica 20 bold",fg="white",bg="grey")
    heading.grid(row=0,column=1,pady=15,columnspan=1,ipadx=10)

    model_l = Label(insert_frame,text="Model No",font="helvetica 12 bold").grid(row=1,column=0,padx=20,pady=15,ipadx=30,ipady=5,sticky=W)
    name_l = Label(insert_frame,text="Name",font="helvetica 12 bold").grid(row=2,column=0,padx=15,pady=15,ipadx=30,ipady=5,sticky=W)
    cat_l = Label(insert_frame,text="Category",font="helvetica 12 bold").grid(row=3,column=0,padx=15,pady=15,ipadx=30,ipady=5,sticky=W)
    com_l = Label(insert_frame,text="Company",font="helvetica 12 bold").grid(row=4,column=0,padx=15,pady=15,ipadx=30,ipady=5,sticky=W)
    qty_l = Label(insert_frame,text="Quantity",font="helvetica 12 bold").grid(row=5,column=0,padx=15,pady=15,ipadx=30,ipady=5,sticky=W)
    price_l = Label(insert_frame,text="Price",font="helvetica 12 bold").grid(row=6,column=0,padx=15,ipadx=30,ipady=5,sticky=W)
    

    #----------------------------------------------------------------------------------------------------------------------------------------------

    model_E = Entry(insert_frame,bd=4,font="helvetica 10 bold",justify="center",width=25,bg="#f1f1f1")
    model_E.grid(row=1,column=1,pady=15,ipady=4,ipadx=5,columnspan=3,sticky=E)
    name_E = Entry(insert_frame,bd=4,font="helvetica 10 bold",justify="center",width=25,bg="#f1f1f1")
    name_E.grid(row=2,column=1,pady=15,ipady=4,ipadx=5,columnspan=3,sticky=E)
    
    cat=StringVar()
    cat_list = [
        "LED","Washing Machine","Mobile","Refrigerator","Laptop","AC","Cooler","Heater","Fan",
        "Iron","JMG","Microwave"
    ]
    category = ttk.Combobox(insert_frame,value=cat_list,textvariable=cat,justify="center",state="readonly",font="helvetica 9 bold",width=23)
    category.current(0)
    category.grid(row=3,column=1,pady=15,ipady=4,ipadx=5,columnspan=3,sticky=E)
    
    com=StringVar()
    com_list = [
        "LG","Apple","Samsung","Oppo","Vivo","Panasonic","videocon","Hitachi","Sony","Micromax",
        "Lava","Huaewi","One Plus","Onida","Godrej","Whirlpool","Dell","Hp","Lenovo","Philips",
        "Maharaja","Nokia","Havells","Bajaj","Khaitan","Coolmaster"
    ]
    company = ttk.Combobox(insert_frame,value=com_list,textvariable=com,justify="center",state="readonly",font="helvetica 9 bold",width=23)
    company.current(0)
    company.grid(row=4,column=1,ipady=4,ipadx=5,pady=15,columnspan=3,sticky=E)
    
    qty_E = Entry(insert_frame,bd=4,font="helvetica 10 bold",justify="center",width=25,bg="#f1f1f1")
    qty_E.grid(row=5,column=1,pady=15,ipady=4,ipadx=5,columnspan=3,sticky=E)
    price_E = Entry(insert_frame,bd=4,font="helvetica 10 bold",justify="center",width=25,bg="#f1f1f1")
    price_E.grid(row=6,column=1,pady=15,ipady=4,ipadx=5,columnspan=3,sticky=E)

    def insert_db(operation):
        # columns in table item : ['id', 'name', 'category', 'company', 'quantity', 'price']
        id = model_E.get()
        name= name_E.get()
        qty = re.sub("[^0-9]","",qty_E.get()) 
        price = re.sub("[^0-9]","",price_E.get()) 
        #print(qty," ",price)

        if(operation == 1):
                                    
            cursor.execute("SELECT * FROM Item WHERE id='{}' OR name='{}'".format(id,name))
            result = cursor.fetchall()
            
            submit_btn.config(bg="#f1f1f1",fg="grey",text = "Insert Item")

            #print(result)

            if(len(result) > 0):
                
                response = messagebox.askyesno("Item Already exists","Do you want to update?")
                submit_btn.config(bg="#f1f1f1",fg="black")
                if response:    
                    query="UPDATE Item SET id='%s',name='%s',category='%s',company='%s',quantity='%s',price='%s' WHERE id='%s'"
                    values = (id,name_E.get(),cat.get(),com.get(),qty,price,id)
                    for val in values:
                        if(len(val)==0):
                            messagebox.showerror("Error","Fields Empty")
                            return
                    cursor.execute(query%values)
                    conn.commit()
                else:
                    model_E.delete(0,END)
                    name_E.delete(0,END)
                    category.current(0)
                    company.current(0)
                    qty_E.delete(0,END)
                    price_E.delete(0,END)                    
            else:
                query = "INSERT into Item values ('%s','%s','%s','%s','%s','%s')"
                values = (model_E.get(),name_E.get(),cat.get(),com.get(),qty,price)
                db.insert(query,values,"Item")
                        
                model_E.delete(0,END)
                name_E.delete(0,END)
                category.current(0)
                company.current(0)
                qty_E.delete(0,END)
                price_E.delete(0,END)

        elif operation==2:

            if(len(id) or len(name)):
                cursor.execute("SELECT * FROM Item WHERE id='{}' OR name='{}'".format(id,name))
                result = cursor.fetchall()
                if(len(result) > 0):
                    result = result[0]

                    model_E.delete(0,END)
                    name_E.delete(0,END)
                    qty_E.delete(0,END)
                    price_E.delete(0,END)

                    model_E.insert(0,result[0])
                    name_E.insert(0,result[1])
                    category.current(cat_list.index(result[2]))
                    company.current(com_list.index(result[3]))
                    qty_E.insert(0,result[4])
                    price_E.insert(0,result[5])

                    submit_btn.config(bg="black",fg="white",text="Update Now")
                
                else:
                    messagebox.showinfo("Database Updation","No Item Exists")
                    model_E.delete(0,END)
                    name_E.delete(0,END)
                    category.current(0)
                    company.current(0)
                    qty_E.delete(0,END)
                    price_E.delete(0,END)

            else:
                messagebox.showinfo("Fields Empty","Enter Id or Name of the item")
                return

    def clear_data():

        model_E.delete(0,END)
        name_E.delete(0,END)
        category.current(0)
        company.current(0)
        qty_E.delete(0,END)
        price_E.delete(0,END)



    def restrict_qty(event):

        qty = qty_E.get()
        qty_E.delete(0,END)
        qty = re.sub("[^0-9]","",qty)
        qty_E.insert(0,qty)

    def restrict_price(event):

        price = price_E.get()
        price_E.delete(0,END)
        price = re.sub("[^0-9]","",price)
        price_E.insert(0,price)

    Button(insert_frame,image=delete_img,bg="lightgrey",bd=6,command=clear_data).place(x=485,y=515)
    submit_btn = Button(insert_frame,text="Insert Item",bg="#f1f1f1",fg="grey",width=12,font="helvetica 12 bold",activebackground="grey",bd=4,command=lambda: insert_db(1))
    submit_btn.grid(row=7,column=0,padx=15,pady=15,ipadx=10,sticky=W)
    update_btn = Button(insert_frame,text="Update Details",bg="#f1f1f1",fg="grey",font="helvetica 12 bold",activebackground="grey",bd=4,command= lambda: insert_db(2))
    update_btn.grid(row=7,column=1,padx=15,ipadx=15,sticky=E)
    #----------------------------------------------------------------------------------------------------------------------------------------------

    qty_E.bind("<Key>",restrict_qty)
    price_E.bind("<Key>",restrict_price)

    insert_frame.resizable(0,0)
    insert_frame.mainloop()


def save_to_excel():

    cursor.execute("SELECT * FROM Item")
    stock = cursor.fetchall()
    if(len(stock) == 0):
        return
    heading = ['Model','Item Name','Category','Company','Quantity','Price']
    w=csv.writer(open('Stock.csv','w',newline=""),delimiter=',')

    w.writerow([head for head in heading])
    for record in stock:
        w.writerow(record)
    print("Successfully Stored In Excel")

#------------------------------------------------------------------------------------

#creating menubar

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0,bg="lightgrey",font="helvetica 9",activebackground="black")
filemenu.add_command(label="Save Your Stock",command=save_to_excel)
filemenu.add_separator()
filemenu.add_command(label="Close All",command=lambda : root.destroy())
menubar.add_cascade(label="File", menu=filemenu)

#filemenu.add_separator()
#filemenu.add_command(label="Exit", command=root.quit)

editmenu = Menu(menubar, tearoff=0,bg="lightgrey",font="helvetica 9",activebackground="black")
editmenu.add_command(label="Update Item",command=insert_item)
editmenu.add_separator()
editmenu.add_command(label="Insert New Item",command=insert_item)
editmenu.add_separator()
editmenu.add_command(label="Search Item",command=list_items)
menubar.add_cascade(label="Edit", menu=editmenu)


root.config(menu=menubar)

#creating icons

list_item_img = PhotoImage(file = r"images/list.png").subsample(15,15)
insert_item_img = PhotoImage(file = r"images/insert_item.png").subsample(15,15)

list_item_btn = Button(root,image=list_item_img,activebackground="white",bd=6,command=list_items,bg="#f1f1f1")
list_item_btn.grid(row=0,column=0,padx=(15,0),pady=15) 
insert_item_btn = Button(root,image=insert_item_img,activebackground="white",bd=6,command=insert_item,bg="#f1f1f1")
insert_item_btn.grid(row=1,column=0,padx=(15,0),pady=15)

#------------------------------------------------------------------------------------



root.mainloop()