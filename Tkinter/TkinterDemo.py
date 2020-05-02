from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import filedialog
import sqlite3


root=Tk()

root.title("Tkinter Demo")
#root.iconbitmap("path")
#root.geometry(500x500)

quitbtn=Button(root,text="exit",command=root.quit)
quitbtn.pack()

#img= ImageTk.PhotoImage(Image.open("path"))
# imglabel=Label(image=my_img)
# imglabel.pack()
#----------------------------------------
# mylabel=Label(root,text="hello world")

# label2=Label(root,text="sanyam jain")
# mylabel.grid(row=1,column=0,colspan=3)

#if we want to stretch label then we can add 'sticky=W+E' (west+east sides )
# label2.grid(row=0,column=2)
#----------------------------------------

def buttonFn():
    #label if we have to give border then bd=1, relief=SUNKEN
    #if we want to move it on right or left then anchor=E(right)
    lbl=Label(root,text=inputbox.get(),anchor=E)
    lbl.pack()

#fg foreground clor, bg background color
#in command we can use lambda:buttonFn(value) if we want to pass some value
#state=DISABLED will disable the button
mybtn=Button(root,text="Click me",command=buttonFn,fg="#f1f1f1",bg="black",padx=30,pady=10)
mybtn.pack()

#from inputbox.get() we get the text inside the box
inputbox=Entry(root,width=30,borderwidth=5)
inputbox.pack()
inputbox.insert(0,"Enter Text") #placeholder 
#inputbox.delete(0,END)
#mylabel.pack()

frame=LabelFrame(root,text="this is my frame",padx=30,pady=10)
frame.pack(padx=50,pady=30)

b=Button(frame,text="click on frame button")
b.grid(row=4,column=1)

#var=StringVar()
#RadioButton(root,text="my radio button",variable=var,value="radio").pack(anchor=W)
#var.get() and var.set("value")

def openPopUp():
    #showinfo,showwarning,showerror,askquestion,askokcancel,askyesno
    respone = messagebox.askyesno("This is my popop","hello world")
    if respone:
        Label(root,text="you clcked yes").pack()
    else:
        Label(root,text="you clcked No").pack()


popoupBtn=Button(root,text="popup",command=openPopUp)
popoupBtn.pack()


def openSecondWindow():


    top=Toplevel()
    top.title("Second Window")
    Label(top,text="second window").pack(padx=50,pady=50)

openWindow=Button(root,text="open window",command=openSecondWindow).pack(padx=50,pady=30)

#dialog box open
#return the path of that file , we can use it to open somefile also
#root.filename=filedialog.askopenfilename(initialdir="/c",title="my dialog",filetypes=(("png","*.png"),("all","*.*") ))

#------------------------
#RadioButton ::
# chkvar=StringVar()
# c=Checkbutton(root,text="This is my check box",variable=chkvar,onvalue="yes",offvalue="no")
# c.deselect()
# c.pack()
# Label(root,text=chkvar.get()).pack()
#------------------------

options=[
"sanyam","annkit","ina","nisha","sanchit"
]



clicked=StringVar()
clicked.set(options[0])

drop=OptionMenu(root,clicked,*options)

drop.pack()

# c.execute(""" CREATE  TABLE customer(
#     fname text,
#     lname text,
#     addr text
# )""")



lblfname=Label(root,text="first name")
lblfname.grid(row=0,column=0)
lbllname=Label(root,text="last name")
lbllname.grid(row=1,column=0)
lbladdr=Label(root,text="address")
lbladdr.grid(row=2,column=0)


fname=Entry(root,width=30)
fname.grid(row=0,column=1,padx=30)
lname=Entry(root,width=30)
lname.grid(row=1,column=1,padx=30)
addr=Entry(root,width=30)
addr.grid(row=2,column=1,padx=30)


def submit():

    conn = sqlite3.connect("inventory.db")
    c=conn.cursor()

    c.execute("INSERT INTO customer VALUES ('%s','%s','%s')"%(fname.get(),lname.get(),addr.get()))

    conn.commit()
    conn.close()

submitBtn=Button(root,text="submit",command=submit)
submitBtn.grid(row=4,column=0,columnspan=2,pady=10,ipadx=100)
root.mainloop()

