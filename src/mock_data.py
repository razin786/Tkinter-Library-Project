import mysql.connector as connect
from tkinter import *
from tkinter import messagebox

def checkpassw(*args):
    global cursor
    global conn
    try:
        conn=connect.connect(user='root',password=passw_entry.get(),host='localhost')
        root.destroy()

        cursor=conn.cursor()
        cursor.execute('show databases like "Library"')
        if cursor.fetchall()==[]:
            cursor.execute('create database Library')
            cursor.execute('use Library')
            cursor.execute('create table members(MemberID int(5) primary key,Name varchar(20),DateOfBirth date,DateOfJoining date)')
            cursor.execute('create table books(BookID int(7) primary key,BookName varchar(30),Author varchar(20),PubYear int(4),Copies int(2))')
            cursor.execute('create table borrowedbooks(MemberID int(5) primary key,Book1 int(7),Date1 date,Book2 int(7),Date2 date,Book3 int(7),Date3 date)')
            cursor.execute('create table requests(MemberID int(5),BookName varchar(30),Author varchar(20),Email varchar(30))')

        try:
            cursor.execute('use Library')
            
            cursor.execute('insert into members values(%s,"%s","%s","%s")'%(10001,'Tom Hanks','2000-01-01','2020-02-02'))
            cursor.execute('insert into members values(%s,"%s","%s","%s")'%(10002,'Porter Robinson','2004-04-08','2019-11-03'))
            cursor.execute('insert into members values(%s,"%s","%s","%s")'%(10003,'Mohammed Naasif','2005-11-20','2019-09-10'))
            cursor.execute('insert into members values(%s,"%s","%s","%s")'%(10004,'Karen Manson','1999-07-25','2021-05-12'))
            cursor.execute('insert into members values(%s,"%s","%s","%s")'%(10005,'Rahul Menon','2005-09-25','2022-04-02'))

            cursor.execute('insert into books values(%s,"%s","%s",%s,%s)'%(1234567,'The Book Thief','Markus Zusak',2005,2))
            cursor.execute('insert into books values(%s,"%s","%s",%s,%s)'%(9259987,'And Then There Were None','Agatha Christie',1939,5))
            cursor.execute('insert into books values(%s,"%s","%s",%s,%s)'%(1794856,'The Kite Runner','Khaled Hosseini',2003,1))
            cursor.execute('insert into books values(%s,"%s","%s",%s,%s)'%(4340938,'1984','George Orwell',1949,2))
            cursor.execute('insert into books values(%s,"%s","%s",%s,%s)'%(1228739,'The Maze Runner','James Dashner',2009,3))

            cursor.execute('insert into borrowedbooks(memberid) values(%s)'%(10001))
            cursor.execute('insert into borrowedbooks(memberid) values(%s)'%(10002))
            cursor.execute('insert into borrowedbooks(memberid) values(%s)'%(10003))
            cursor.execute('insert into borrowedbooks(memberid) values(%s)'%(10004))
            cursor.execute('insert into borrowedbooks(memberid) values(%s)'%(10005))
                
            conn.commit()
            messagebox.showinfo("Library", 'Values inserted')
        except:
            messagebox.showinfo("Library", "Error")
    except:
        wrongpass=Label(root,text='Wrong password',bg='#D7D7D7',font=('Bahnschrift',11),fg='red')
        wrongpass.grid(row=2,column=2)
        wrongpass.after(2500,wrongpass.destroy)

root=Tk()
root.configure(bg='#D7D7D7')
root.geometry('400x150')
root.title('Library')
root.eval('tk::PlaceWindow . center')
root.resizable(width=False, height=False)

root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(3,weight=1)
root.grid_columnconfigure(0,weight=1)
root.grid_columnconfigure(4,weight=1)

passwlabel=Label(root,text="Enter Password:",bg='#D7D7D7',font=('Bahnschrift',11)).grid(row=1,column=1)
passw_entry=Entry(root,show='*')
passw_entry.grid(row=1,column=2)
passw_entry.focus()
root.bind('<Return>',checkpassw)

root.mainloop()