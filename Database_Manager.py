import sqlite3
from sqlite3 import Error
from tkinter import messagebox
import os

class Stock:
    
    def __init__(self,db):

        self.dbname=db
        self.conn=None
    
    def create_connection(self):

        try:
            if(not os.path.exists(os.getcwd()+"\\"+self.dbname)):
                print("Creating Database .. \n")
            print("'%s' Exists! \n"%(self.dbname))
            self.conn=sqlite3.connect(self.dbname)

        except Error as e:
            print(e)
        
        finally:
            return self.conn

    def get_cursor(self):

        return self.conn.cursor()
        
    def create_table(self,query):
        
        if(self.conn != None):
                
            c=self.conn.cursor()
            c.execute(query)
            self.conn.commit()
            print('Table Created !')
        
        else:

            print("Connection Not Established! \n")
            return
    
    def list_tables(self):
        
        if(self.conn != None):
            c=self.conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print(c.fetchall())
        
        else:
            print('No connection')
    
    def insert(self,query,value,table):
        
        for val in value:
            if(len(val)==0):
                messagebox.showerror("Error","Failed to insert")
                return
                
        c=self.conn.cursor()
        
        try:

            query = query%value
            c.execute(query)
            self.conn.commit()
            last_row = c.execute('select * from '+table).fetchall()[-1]
            print('Insertion Successfull -> ',last_row)
            if(last_row):
                messagebox.showinfo("Database Insertion","Insertion Successfull")

        except Error as e:
            print(e)
            messagebox.showerror("Database Insertion Failed","Insertion Failed")

        

        
    def get_Columns(self,table):

        c=self.conn.cursor()
        c.execute("SELECT * from "+str(table))
        columns = [col[0] for col in c.description]
        return columns
        