from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as connect
from datetime import datetime

def mainfn():
    global ViewMemButton, ViewBookButton, BorrowButton, ViewReqButton, main, ExitButton
    
    main=Tk()
    main.configure(bg='#D7D7D7')
    main.geometry('600x400')
    main.title('Library')
    main.eval('tk::PlaceWindow . center')
    main.minsize(600,400)
    main.maxsize(700,466)

    main.grid_rowconfigure(0,weight=1)
    main.grid_rowconfigure(3,weight=1)
    main.grid_columnconfigure(0,weight=1)
    main.grid_columnconfigure(2,weight=1)
    main.grid_columnconfigure(4,weight=1)

    ViewMemButton=Button(text='View/Edit Member Info',command=memberlist,bg='#FF8F37',activebackground='#FFA45D',font=('Bahnschrift',14),height=3,width=20)
    ViewMemButton.grid(row=0,column=1)
    ViewBookButton=Button(text='View/Edit Book Info',command=booklist,font=('Bahnschrift',14),activebackground='#FFA45D',bg='#FF8F37',height=3,width=20)
    ViewBookButton.grid(row=0,column=3)
    BorrowButton=Button(text='Borrow/Return Books',command=borrowreturn,bg='#FF8F37',activebackground='#FFA45D',font=('Bahnschrift',14),height=3,width=20)
    BorrowButton.place(relx=0.077,rely=0.5,anchor='nw')
    ViewReqButton=Button(text='View Book Requests',command=viewreq,font=('Bahnschrift',14),activebackground='#FFA45D',bg='#FF8F37',height=3,width=20)
    ViewReqButton.place(relx=0.539,rely=0.5,anchor='nw')
    ExitButton=Button(text='Exit',height=2,width=10,font=('Bahnschrift',11),bg='#FF1B1B',activebackground='#FF3E3E',command=exitfn)
    ExitButton.place(relx=0.96,rely=0.94,anchor='se')

    main.mainloop()

def memberstable():
        global table, canvas, scrollbar

        cursor.execute('select * from members')
        n=len(cursor.fetchall())
        if n>9:
            n=9
        
        canvas=Canvas(main,height=25+23*n,width=595,bg='#D7D7D7',highlightthickness=0)
        canvas.grid_propagate(False)
        canvas.grid(row=1,column=1)
        scrollbar=ttk.Scrollbar(main,orient=VERTICAL,command=canvas.yview)
        scrollbar.grid(row=1,column=2,sticky='nsw')

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))

        table=Canvas(canvas,bg='black',highlightthickness=0)
        canvas.create_window((0,0),window=table)
        
        cursor.execute('select * from members')

        buffer=Canvas(main,height=25+23*n,width=595,bg='#D7D7D7',highlightthickness=0)
        buffer.grid_propagate(False)
        buffer.grid(row=1,column=1)

        Label(table,text='MemberID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
        Label(table,text='Name',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
        Label(table,text='Date of Birth',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
        Label(table,text='Date of Joining',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)

        i=1
        j=1
        for e in cursor.fetchall():
            for a in e:
                Label(table,text=a,height=1,width=20,bg='#FFFEF2').grid(row=i,column=j,padx=0.5,pady=0.5)
                j+=1
                if j%5==0:
                    i+=1
                    j=1
        try:
            BackButton.config(command=back)
        except:
            pass
        
        canvas.update_idletasks()
        canvas.yview_moveto('0.0')
        buffer.destroy()

def back(*args):
    global w, main
    
    try:
        w.destroy()
    except:
        pass

    main.destroy()
    mainfn()

def exitfn(*args):
    global w, w1
    
    try:
        w.destroy()
    except:
        pass
    try:
        w1.destroy()
    except:
        pass
    main.destroy()

def check():
    global d
    x = main.winfo_pointerx()
    y = main.winfo_pointery()
    widget = main.winfo_containing(x,y)
    row=widget.grid_info()['row']
    if row in d:
        del d[row]
    else:
        d[row]=1

def focus_in(*args):
    EditSearch.delete(0,END)
    EditSearch.config(fg='black')

def clock():
    global clocklabel
    
    now=datetime.now()
    date=str(now.strftime('%d %b %Y'))
    time=str(now.strftime('%H:%M:%S'))

    clocklabel.config(text='%s\n%s'%(date,time))

    clocklabel.after(1, clock)
    
def memberlist():

    def widgets():
        global AddButton, EditButton, RemoveButton, BackButton, clocklabel, clocklabel2
        
        AddButton=Button(main,text='Add Record(s)',height=1,width=13,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=add)
        AddButton.place(relx=0.785,rely=0.172,anchor='se')
        EditButton=Button(main,text='Edit Record',height=1,width=10,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=search)
        EditButton.place(relx=0.62,rely=0.172,anchor='se')
        RemoveButton=Button(main,text='Remove Record(s)',height=1,width=15,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=remove)
        RemoveButton.place(relx=0.97,rely=0.172,anchor='se')
    
        ExitButton.place(relx=0.97,rely=0.96,anchor='se')
        BackButton=Button(main,text='< Back',height=2,width=10,font=('Bahnschrift',11),bg='#EFB700',activebackground='#EFCA50',command=back)
        BackButton.place(relx=0.84,rely=0.96,anchor='se')

        clocklabel=Label(main,width=25,font=('Yu Gothic bold',17),bg='#D7D7D7')
        clocklabel.place(relx=0.37,rely=0.2,anchor='se')
        clock()

    def searchback():
        global EditButton
        global EditSearch
        global SearchButton
        global EditLabel
        global BackButton

        try:
            errorlabel.destroy()
        except:
            pass
        try:
            notfound.destroy()
        except:
            pass
        
        EditLabel.destroy()
        EditButton.destroy()
        EditSearch.destroy()
        SearchButton.destroy()
        EditButton=Button(main,text='Edit Record',height=1,width=10,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=search)
        EditButton.place(relx=0.62,rely=0.172,anchor='se')
        BackButton.config(command=back)
            
    def editback():
        global canvas
        global SaveButton
        global scrollbar
 
        canvas.destroy()
        scrollbar.destroy()
        SaveButton.destroy()
        memberstable()
        widgets()
    
    def addback():
        global table
        global SaveButton
        global scrollbar
        global Add_Label
        global Add_Combobox

        table.destroy()
        SaveButton.destroy()
        Add_Label.destroy()
        Add_Combobox.destroy()
        memberstable()
        widgets()

    def removeback():
        global canvas
        global ConfirmRemoveButton
        global scrollbar

        scrollbar.destroy()
        canvas.destroy()
        ConfirmRemoveButton.destroy()
        memberstable()
        widgets()

    def editsave():
        try:
            global conn
            global MemberID_Entry
            global Name_Entry
            global DOB_Entry
            global DOJ_Entry
            global main

            for a in result:
                if MemberID_Entry.get()!=a[0]:
                    cursor.execute('update members set MemberID=%s where MemberID=%s'%(MemberID_Entry.get(),a[0]))
                    cursor.execute('update borrowedbooks set MemberID=%s where MemberID=%s',(MemberID_Entry.get(),a[0]))
                if Name_Entry.get()!=a[1]:
                    cursor.execute('update members set Name="%s" where MemberID=%s'%(Name_Entry.get(),MemberID_Entry.get()))
                if DOB_Entry.get()!=a[2]:
                    cursor.execute('update members set dateofbirth="%s" where MemberID=%s'%(DOB_Entry.get(),MemberID_Entry.get()))
                if DOJ_Entry.get()!=a[3]:
                    cursor.execute('update members set dateofjoining="%s" where MemberID=%s'%(DOJ_Entry.get(),MemberID_Entry.get()))
            conn.commit()
            messagebox.showinfo("Library", "Changes saved Successfully")
            editback()
        except:
            errormsg=Label(main,text='Error, please try again',width=25,font=('Bahnschrift',10),bg='#D7D7D7',fg='red')
            errormsg.grid(row=2,column=1)
            errormsg.after(1200,errormsg.destroy)

    def edit(*args):
        global errorlabel
        global notfound
        
        try:
            global MemberID_Entry, Name_Entry, DOB_Entry, DOJ_Entry
            global result, table, SaveButton, canvas, AddButton, EditButton, RemoveButton, scrollbar

            cursor.execute('select * from members where memberid=%s'%(EditSearch.get()))
            result=cursor.fetchall()
            if result==[]:
                errormsg=Label(main,text='Record not found',font=('Bahnschrift',8),bg='#D7D7D7',fg='red')
                errormsg.place(relx=0.53,rely=0.21,anchor='se')
                errormsg.after(1200,errormsg.destroy)
                EditSearch.select_range(0,END)
            else:
                searchback()
                AddButton.destroy()
                EditButton.destroy()
                RemoveButton.destroy()
                scrollbar.destroy()
                
                BackButton.config(command=editback)

                canvas.destroy()
                canvas=Canvas(main,height=206,width=595,bg='#D7D7D7',highlightthickness=0)
                canvas.grid(row=1,column=1)
                table=Canvas(canvas,bg='black',highlightthickness=0)
                table.grid()
                Label(table,text='MemberID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
                Label(table,text='Name',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
                Label(table,text='Date of Birth',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
                Label(table,text='Date of Joining',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)
                for a in result:
                    MemberID_Entry=Entry(table,width=24)
                    MemberID_Entry.insert(0,a[0])
                    MemberID_Entry.grid(row=1,column=1,pady=0.5)
                    Name_Entry=Entry(table,width=24)
                    Name_Entry.insert(0,a[1])
                    Name_Entry.grid(row=1,column=2,pady=0.5)
                    DOB_Entry=Entry(table,width=24)
                    DOB_Entry.insert(0,a[2])
                    DOB_Entry.grid(row=1,column=3,pady=0.5)
                    DOJ_Entry=Entry(table,width=24)
                    DOJ_Entry.insert(0,a[3])
                    DOJ_Entry.grid(row=1,column=4,pady=0.5)
                MemberID_Entry.focus()

                SaveButton=Button(main,text='Save',command=editsave,height=1,width=10,bg='#069408',font=('Bahnschrift',10),activebackground='#06C308')
                SaveButton.grid(row=3,column=1)                
        except:
            errormsg=Label(main,text='Enter a valid ID',width=15,font=('Bahnschrift',8),bg='#D7D7D7',fg='red')
            errormsg.place(relx=0.53,rely=0.21,anchor='se')
            errormsg.after(1200,errormsg.destroy)
            EditSearch.select_range(0,END)

    def confirmremove():
        cursor.execute('select * from members')
        result=cursor.fetchall()
        for n in d:
            cursor.execute('delete from members where memberid=%s'%(result[n-1][0]))
            cursor.execute('delete from borrowedbooks where memberid=%s'%(result[n-1][0]))
            conn.commit()
        messagebox.showinfo("Library", "Changes saved Successfully")
        removeback()

    def remove():
        global d, result, BackButton, ConfirmRemoveButton, table, AddButton, RemoveButton, EditButton, canvas

        try:
            searchback()
        except:
            pass

        AddButton.destroy()
        RemoveButton.destroy()
        EditButton.destroy()

        cursor.execute('select * from members')
        n=len(cursor.fetchall())
        if n>9:
            n=9
        
        canvas.configure(height=25*(n+1),width=627)
        
        buffer=Canvas(main,height=28+24*n,width=627,bg='#D7D7D7',highlightthickness=0)
        buffer.grid_propagate(False)
        buffer.grid(row=1,column=1)
        
        d={}
        i=1
        cursor.execute('select * from members')
        result=cursor.fetchall()
        Label(table,bg='#F3F3F3').grid(row=0,column=0,sticky='nsew')
        for a in result:
            Checkbutton(table,bg='#F3F3F3',command=check).grid(row=i,column=0)
            chkbtn=table.grid_slaves(row=i,column=0)
            chkbtn[0].deselect()
            i+=1

        canvas.update_idletasks()
        buffer.destroy()
        canvas.yview_moveto('0.0')
        
        ConfirmRemoveButton=Button(main,text='Remove',command=confirmremove,height=1,width=10,bg='#069408',font=('Bahnschrift',10),activebackground='#06C308')
        ConfirmRemoveButton.grid(row=3,column=1)
        BackButton.config(command=removeback)

    def addrows(*args):
        global table
        global canvas
        global scrollbar

        try:
            table.destroy()
        except:
            pass
        canvas.destroy()
        scrollbar.destroy()
        table=Canvas(main,bg='black',highlightthickness=0)
        table.grid(row=1,column=1)

        Label(table,text='MemberID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
        Label(table,text='Name',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
        Label(table,text='Date of Birth',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
        Label(table,text='Date of Joining',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)

        i=1
        for e in range(int(Add_Combobox.get())):
            for j in range(1,5):
                Entry(table,width=24).grid(row=i,column=j,pady=0.5)
            i+=1

    def add():
        global Add_Combobox, SaveButton, BackButton, Add_Label, AddButton, EditButton, RemoveButton

        try:
            searchback()
        except:
            pass

        AddButton.destroy()
        EditButton.destroy()
        RemoveButton.destroy()

        Add_Label=Label(main,text='Add                  records',width=18,font=('Bahnschrift',10),bg='#D7D7D7')
        Add_Label.place(relx=0.27,rely=0.24,anchor='se')
        Add_Combobox=ttk.Combobox(main,width=3)
        Add_Combobox['values']=(1,2,3,4,5)
        Add_Combobox.current(0)
        Add_Combobox.place(relx=0.2,rely=0.24,anchor='se')
        addrows()
        Add_Combobox.bind('<<ComboboxSelected>>',addrows)
        SaveButton=Button(main,text='Save',command=addsave,height=1,width=10,bg='#069408',font=('Bahnschrift',10),activebackground='#06C308')
        SaveButton.grid(row=3,column=1)
        BackButton.config(command=addback)
        
    def addsave():
        global table
        global SaveButton
        
        Label(main,width=25,font=('Bahnschrift',10),bg='#D7D7D7').grid(row=2,column=1)
        i=1
        c=True
        for e in range(int(Add_Combobox.get())):
            try:
                cursor.execute('insert into members values(%s,"%s","%s","%s")'%(int((table.grid_slaves(i,1)[0]).get()),(table.grid_slaves(i,2)[0]).get(),(table.grid_slaves(i,3)[0]).get(),(table.grid_slaves(i,4)[0]).get()))
                cursor.execute('insert into borrowedbooks(memberid) values(%s)'%(int((table.grid_slaves(i,1)[0]).get())))
                i+=1
            except:
                c=False
                break
        if c==True:
            conn.commit()
            messagebox.showinfo("Library", "Changes saved Successfully")
            addback()
        else:
            errormsg=Label(main,text='Error in entry %s'%(i),width=25,font=('Bahnschrift',10),bg='#D7D7D7',fg='red')
            errormsg.grid(row=2,column=1)
            errormsg.after(1200,errormsg.destroy)
        
    def search():
        global EditSearch
        global EditLabel
        global SearchButton
        global EditButton
        global BackButton
        global table
        global canvas

        EditButton.destroy()
        EditLabel=Label(main,text='Enter MemberID:',font=('Bahnschrift',10),bg='#D7D7D7')
        EditLabel.place(relx=0.395,rely=0.163,anchor='se')
        EditSearch=Entry(main,fg='grey')
        EditSearch.place(relx=0.55,rely=0.16,anchor='se')
        EditSearch.insert(0,'eg:10001')
        SearchButton=Button(text='Search',height=1,width=7,font=('Bahnschrift',9),bg='#6A6A6A',activebackground='#9B9B9B',command=edit)
        SearchButton.place(relx=0.63,rely=0.165,anchor='se')
        EditSearch.bind('<FocusIn>',focus_in)
        EditSearch.bind('<Return>',edit)

        BackButton.config(command=searchback)

    try:
        ViewBookButton.destroy()
        ViewMemButton.destroy()
        BorrowButton.destroy()
        ViewReqButton.destroy()
    except:
        pass
    
    global main
    main.geometry('800x500')
    main.grid_columnconfigure(4,weight=0)
    main.eval('tk::PlaceWindow . center')
    main.resizable(False,False)

    memberstable()
    widgets()

def bookstable():
    global table
    global canvas
    global scrollbar
    
    cursor.execute('select bookid,bookname,author,pubyear from books')
    n=len(cursor.fetchall())
    if n>9:
        n=9
        
    canvas=Canvas(main,height=25+23*n,width=695,bg='#D7D7D7',highlightthickness=0)
    canvas.grid_propagate(False)
    canvas.grid(row=1,column=1)
    scrollbar=ttk.Scrollbar(main,orient=VERTICAL,command=canvas.yview)
    scrollbar.grid(row=1,column=2,sticky='nsw')

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))

    table=Canvas(canvas,bg='black',highlightthickness=0)
    canvas.create_window((0,0),window=table)

    buffer=Canvas(main,height=28+22*n,width=695,bg='#D7D7D7',highlightthickness=0)
    buffer.grid_propagate(False)
    buffer.grid(row=1,column=1)
        
    Label(table,text='BookID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
    Label(table,text='BookName',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
    Label(table,text='Author',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
    Label(table,text='PubYear',font='Arial 9 bold',height=1,width=16,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)
    Label(table,text='Copies',font='Arial 9 bold',height=1,width=16,bg='#F3F3F3').grid(row=0,column=5,padx=2,pady=2)

    cursor.execute('select * from books')
    i=1
    j=1
    for e in cursor.fetchall():
        for a in e:
            if j in [4,5]:
                Label(table,text=a,height=1,width=16,bg='#FFFEF2').grid(row=i,column=j,padx=0.5,pady=0.5)
            else:
                Label(table,text=a,height=1,width=20,bg='#FFFEF2').grid(row=i,column=j,padx=0.5,pady=0.5)
            j+=1
            if j%6==0:
                i+=1
                j=1
    try:
        BackButton.config(command=back)
    except:
        pass
        
    canvas.update_idletasks()
    buffer.destroy()
    canvas.yview_moveto('0.0')
    
def booklist():

    def widgets2():
        global AddButton, EditButton, RemoveButton, clocklabel, clocklabel2
        
        AddButton=Button(main,text='Add Record(s)',height=1,width=13,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=add2)
        AddButton.place(relx=0.785,rely=0.172,anchor='se')
        EditButton=Button(main,text='Edit Record',height=1,width=10,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=search2)
        EditButton.place(relx=0.62,rely=0.172,anchor='se')
        RemoveButton=Button(main,text='Remove Record(s)',height=1,width=15,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=remove2)
        RemoveButton.place(relx=0.97,rely=0.172,anchor='se')

        clocklabel=Label(main,width=25,font=('Yu Gothic bold',17),bg='#D7D7D7')
        clocklabel.place(relx=0.37,rely=0.2,anchor='se')
        clock()


    def searchback2():
        global EditButton
        global EditSearch
        global SearchButton
        global EditLabel
        global BackButton
        
        EditLabel.destroy()
        EditButton.destroy()
        EditSearch.destroy()
        SearchButton.destroy()
        EditButton=Button(main,text='Edit Record',height=1,width=10,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=search2)
        EditButton.place(relx=0.62,rely=0.172,anchor='se')
        BackButton.config(command=back)
            
    def editback2():
        global canvas
        global SaveButton
        global scrollbar
 
        canvas.destroy()
        scrollbar.destroy()
        SaveButton.destroy()
        bookstable()
        widgets2()
    
    def addback2():
        global table
        global SaveButton
        global scrollbar
        global Add_Label
        global Add_Combobox

        table.destroy()
        SaveButton.destroy()
        Add_Label.destroy()
        Add_Combobox.destroy()
        bookstable()
        widgets2()

    def removeback2():
        global canvas
        global ConfirmRemoveButton
        global scrollbar

        scrollbar.destroy()
        canvas.destroy()
        ConfirmRemoveButton.destroy()
        bookstable()
        widgets2()

    def editsave2():
        try:
            global BookID_Entry, BookName_Entry, Author_Entry, PubYear_Entry, Copies_Entry
            global main, conn

            for a in result:
                if BookID_Entry.get()!=a[0]:
                    cursor.execute('update books set bookid=%s where bookid=%s'%(BookID_Entry.get(),a[0]))
                if BookName_Entry.get()!=a[1]:
                    cursor.execute('update books set bookname="%s" where bookid=%s'%(BookName_Entry.get(),BookID_Entry.get()))
                if Author_Entry.get()!=a[2]:
                    cursor.execute('update books set author="%s" where bookid=%s'%(Author_Entry.get(),BookID_Entry.get()))
                if PubYear_Entry.get()!=a[3]:
                    cursor.execute('update books set pubyear="%s" where bookid=%s'%(PubYear_Entry.get(),BookID_Entry.get()))
                if Copies_Entry.get()!=a[4]:
                    cursor.execute('update books set copies=%s where bookid=%s'%(Copies_Entry.get(),BookID_Entry.get()))
                    
            conn.commit()
            messagebox.showinfo("Library", "Changes saved Successfully")
            editback2()
        except:
            errormsg=Label(main,text='Error, please try again',width=25,font=('Bahnschrift',10),bg='#D7D7D7',fg='red')
            errormsg.grid(row=2,column=1)
            errormsg.after(1200,errormsg.destroy)

    def edit2(*args):
        global errorlabel
        global notfound
        
        try:
            global BookID_Entry, BookName_Entry, Author_Entry, PubYear_Entry, Copies_Entry
            global result, table, SaveButton, canvas, AddButton, EditButton, RemoveButton, scrollbar

            cursor.execute('select * from books where bookid=%s'%(EditSearch.get()))
            result=cursor.fetchall()
            if result==[]:
                errormsg=Label(main,text='Record not found',font=('Bahnschrift',8),bg='#D7D7D7',fg='red')
                errormsg.place(relx=0.53,rely=0.21,anchor='se')
                errormsg.after(1200,errormsg.destroy)
                EditSearch.select_range(0,END)
            else:
                searchback2()
                AddButton.destroy()
                EditButton.destroy()
                RemoveButton.destroy()
                scrollbar.destroy()
                
                BackButton.config(command=editback2)
                canvas.destroy()
                canvas=Canvas(main,height=206,width=595,bg='#D7D7D7',highlightthickness=0)
                canvas.grid(row=1,column=1)
                table=Canvas(canvas,bg='black',highlightthickness=0)
                table.grid()
                Label(table,text='BookID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
                Label(table,text='BookName',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
                Label(table,text='Author',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
                Label(table,text='PubYear',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)
                Label(table,text='Copies',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=5,padx=2,pady=2)
                for a in result:
                    BookID_Entry=Entry(table,width=24)
                    BookID_Entry.insert(0,a[0])
                    BookID_Entry.grid(row=1,column=1,pady=0.5)
                    BookName_Entry=Entry(table,width=24)
                    BookName_Entry.insert(0,a[1])
                    BookName_Entry.grid(row=1,column=2,pady=0.5)
                    Author_Entry=Entry(table,width=24)
                    Author_Entry.insert(0,a[2])
                    Author_Entry.grid(row=1,column=3,pady=0.5)
                    PubYear_Entry=Entry(table,width=24)
                    PubYear_Entry.insert(0,a[3])
                    PubYear_Entry.grid(row=1,column=4,pady=0.5)
                    Copies_Entry=Entry(table,width=24)
                    Copies_Entry.insert(0,a[4])
                    Copies_Entry.grid(row=1,column=5,pady=0.5)
                    
                BookID_Entry.focus()

                SaveButton=Button(main,text='Save',command=editsave2,height=1,width=10,bg='#069408',font=('Bahnschrift',10),activebackground='#06C308')
                SaveButton.grid(row=3,column=1)                
        except:
            errormsg=Label(main,text='Enter a valid ID',width=15,font=('Bahnschrift',8),bg='#D7D7D7',fg='red')
            errormsg.place(relx=0.53,rely=0.21,anchor='se')
            errormsg.after(1200,errormsg.destroy)
            EditSearch.select_range(0,END)

    def confirmremove2():
        cursor.execute('select * from books')
        result=cursor.fetchall()
        for n in d:
            cursor.execute('delete from books where bookid=%s'%(result[n-1][0]))
            conn.commit()
        messagebox.showinfo("Library", "Changes saved Successfully")
        removeback2()

    def remove2():
        global d, result, BackButton, ConfirmRemoveButton, table, AddButton, RemoveButton, EditButton, canvas

        try:
            searchback2()
        except:
            pass

        AddButton.destroy()
        RemoveButton.destroy()
        EditButton.destroy()
        
        cursor.execute('select * from books')
        n=len(cursor.fetchall())
        if n>9:
            n=9
        
        canvas.configure(height=25*(n+1),width=720)

        buffer=Canvas(main,height=28+22*n,width=720,bg='#D7D7D7',highlightthickness=0)
        buffer.grid_propagate(False)
        buffer.grid(row=1,column=1)
        
        d={}
        i=1
        cursor.execute('select * from books')
        result=cursor.fetchall()
        Label(table,bg='#F3F3F3').grid(row=0,column=0,sticky='nsew')
        for a in result:
            Checkbutton(table,bg='#F3F3F3',command=check).grid(row=i,column=0)
            chkbtn=table.grid_slaves(row=i,column=0)
            chkbtn[0].deselect()
            i+=1

        canvas.update_idletasks()
        buffer.destroy()
        canvas.yview_moveto('0.0')
        
        ConfirmRemoveButton=Button(main,text='Remove',command=confirmremove2,height=1,width=10,bg='#069408',font=('Bahnschrift',10),activebackground='#06C308')
        ConfirmRemoveButton.grid(row=3,column=1)
        BackButton.config(command=removeback2)

    def addrows2(*args):
        global table
        global canvas
        global scrollbar

        try:
            table.destroy()
        except:
            pass
        canvas.destroy()
        scrollbar.destroy()
        table=Canvas(main,bg='black',highlightthickness=0)
        table.grid(row=1,column=1)

        Label(table,text='BookID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
        Label(table,text='BookName',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
        Label(table,text='Author',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
        Label(table,text='PubYear',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)
        Label(table,text='Copies',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=5,padx=2,pady=2)
        
        i=1
        for e in range(int(Add_Combobox.get())):
            for j in range(1,6):
                Entry(table,width=24).grid(row=i,column=j,pady=0.5)
            i+=1
        
    def add2():
        global Add_Combobox
        global SaveButton
        global BackButton
        global Add_Label
        global AddButton
        global EditButton
        global RemoveButton

        try:
            searchback2()
        except:
            pass

        AddButton.destroy()
        EditButton.destroy()
        RemoveButton.destroy()

        Add_Label=Label(main,text='Add                  records',width=18,font=('Bahnschrift',10),bg='#D7D7D7')
        Add_Label.place(relx=0.27,rely=0.24,anchor='se')
        Add_Combobox=ttk.Combobox(main,width=3)
        Add_Combobox['values']=(1,2,3,4,5)
        Add_Combobox.current(0)
        Add_Combobox.place(relx=0.2,rely=0.24,anchor='se')
        addrows2()
        Add_Combobox.bind('<<ComboboxSelected>>',addrows2)
        SaveButton=Button(main,text='Save',command=addsave2,height=1,width=10,bg='#069408',font=('Bahnschrift',10),activebackground='#06C308')
        SaveButton.grid(row=3,column=1)
        BackButton.config(command=addback2)
        
    def addsave2():
        global table
        global SaveButton
        
        Label(main,width=25,font=('Bahnschrift',10),bg='#D7D7D7').grid(row=2,column=1)
        i=1
        c=True
        for e in range(int(Add_Combobox.get())):
            try:
                cursor.execute('insert into books values(%s,"%s","%s",%s,%s)'%(int((table.grid_slaves(i,1)[0]).get()),(table.grid_slaves(i,2)[0]).get(),(table.grid_slaves(i,3)[0]).get(),int((table.grid_slaves(i,4)[0]).get()),int((table.grid_slaves(i,5)[0]).get())))
                try:
                    cursor.execute('delete from requests where bookname="%s" and author="%s"'%(table.grid_slaves(i,2)[0].get(),table.grid_slaves(i,3)[0].get()))
                except:
                    pass
                i+=1
            except:
                c=False
                break
        if c==True:
            conn.commit()
            messagebox.showinfo("Library", "Changes saved Successfully")
            addback2()
        else:
            errormsg=Label(main,text='Error in entry %s'%(i),width=25,font=('Bahnschrift',10),bg='#D7D7D7',fg='red')
            errormsg.grid(row=2,column=1)
            errormsg.after(1200,errormsg.destroy)
        
    def search2():
        global EditSearch, EditLabel, SearchButton, EditButton, BackButton, table, canvas

        EditButton.destroy()
        EditLabel=Label(main,text='Enter BookID:',font=('Bahnschrift',10),bg='#D7D7D7')
        EditLabel.place(relx=0.395,rely=0.163,anchor='se')
        EditSearch=Entry(main,fg='grey')
        EditSearch.place(relx=0.55,rely=0.16,anchor='se')
        EditSearch.insert(0,'eg:1234567')
        SearchButton=Button(text='Search',height=1,width=7,font=('Bahnschrift',9),bg='#6A6A6A',activebackground='#9B9B9B',command=edit2)
        SearchButton.place(relx=0.63,rely=0.165,anchor='se')
        EditSearch.bind('<FocusIn>',focus_in)
        EditSearch.bind('<Return>',edit2)

        BackButton.config(command=searchback2)

    try:
        ViewBookButton.destroy()
        ViewMemButton.destroy()
        BorrowButton.destroy()
        ViewReqButton.destroy()        
    except:
        pass
    
    global main
    main.geometry('800x500')
    main.grid_columnconfigure(4,weight=0)
    main.eval('tk::PlaceWindow . center')
    main.resizable(False,False)

    bookstable()

    global BackButton
    
    ExitButton.place(relx=0.97,rely=0.96,anchor='se')
    BackButton=Button(main,text='< Back',height=2,width=10,font=('Bahnschrift',11),bg='#EFB700',activebackground='#EFCA50',command=back)
    BackButton.place(relx=0.84,rely=0.96,anchor='se')
    widgets2()
    
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
        else:
            cursor.execute('use Library')
        mainfn()
    except:
        wrongpass=Label(root,text='Wrong password',bg='#D7D7D7',font=('Bahnschrift',11),fg='red')
        wrongpass.grid(row=1,column=3)
        wrongpass.after(1200,wrongpass.destroy)

def borrowreturn():
    global TopLabel, clocklabel, clocklabel2
    
    def widgets3():
        global borrowbutton, returnbutton
        
        borrowbutton=Button(main,text='Borrow Books',command=borrowbooks,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B')
        borrowbutton.place(relx=0.35,rely=0.7)
        returnbutton=Button(main,text='Return Books',command=returnbooks,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B')
        returnbutton.place(relx=0.51,rely=0.7)
        
    def focus(*args):
         identry.delete(0,END)
         identry.config(fg='black')

    def idsearch(*args):
        global identry, memid, borrowbutton, returnbutton, removebutton, table, confirmremovebutton, TopLabel

        try:
            memid=int(identry.get())
            try:
                borrowbutton.destroy()
                returnbutton.destroy()
            except:
                pass

            try:
                removebutton.destroy()
            except:
                pass

            try:
                table.destroy()
            except:
                pass

            try:
                confirmborrowbutton.destroy()
            except:
                pass
            
            cursor.execute('select * from borrowedbooks where memberid=%s'%(memid))
            result=cursor.fetchall()
            if result==[]:
                
                errormsg=Label(main,text='Invalid ID',font=('Bahnschrift',9),bg='#D7D7D7',fg='red')
                errormsg.place(relx=0.545,rely=0.21,anchor='se')
                errormsg.after(1200,errormsg.destroy)
                identry.select_range(0,END)
                
                try:
                    TopLabel.destroy()
                except:
                    pass
            else:
                try:
                    TopLabel.destroy()
                except:
                    pass
                
                TopLabel=Label(main,width=14,text='MemberID:%s'%memid,font=('Bahnschrift',20),bg='#D7D7D7')
                TopLabel.place(relx=0.62,rely=0.3,anchor='se')
                borrowtable()
                widgets3()
        except:
            
            errormsg=Label(main,text='Invalid ID',font=('Bahnschrift',9),bg='#D7D7D7',fg='red')
            errormsg.place(relx=0.545,rely=0.21,anchor='se')
            errormsg.after(1200,errormsg.destroy)
            identry.select_range(0,END)
            
            try:
                TopLabel.destroy()
            except:
                pass
            
            try:
                table.destroy()
                borrowbutton.destroy()
                returnbutton.destroy()
            except:
                pass

    def borrowtable():
        global table, canvas, scrollbar, memid, i, TotalFeeLabel

        table=Canvas(main,bg='black',highlightthickness=0)
        table.grid(row=1,column=1)
            
        Label(table,text='BookID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
        Label(table,text='Book Name',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
        Label(table,text='Author',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
        Label(table,text='Borrow Date',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)
        Label(table,text='Return Date',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=5,padx=2,pady=2)

        cursor.execute('select book1,book2,book3 from borrowedbooks where memberid=%s'%(memid))
        result=cursor.fetchall()
        sdate=str(datetime.today())
        TotalLateFee=0

        i=1
        for bookid in result[0]:
            if bookid !=None:
                if i==1:
                    cursor.execute('select datediff("%s",date1) from borrowedbooks where memberid=%s'%(sdate,memid))
                    extradays=(cursor.fetchall()[0][0])-14
                    if extradays>0:
                        TotalLateFee+=extradays*5
                    cursor.execute('select bookid,bookname,author,date1,date_add(date1, interval 2 week) from books b natural join borrowedbooks bo where b.BookID=%s and bo.book1=%s and bo.memberid=%s'%(bookid,bookid,memid))
                elif i==2:
                    cursor.execute('select datediff("%s",date2) from borrowedbooks where memberid=%s'%(sdate,memid))
                    extradays=(cursor.fetchall()[0][0])-14
                    if extradays>0:
                        TotalLateFee+=extradays*5
                    cursor.execute('select bookid,bookname,author,date2,date_add(date2, interval 2 week) from books b natural join borrowedbooks bo where b.BookID=%s and bo.book2=%s and bo.memberid=%s'%(bookid,bookid,memid))
                elif i==3:
                    cursor.execute('select datediff("%s",date3) from borrowedbooks where memberid=%s'%(sdate,memid))
                    extradays=(cursor.fetchall()[0][0])-14
                    if extradays>0:
                        TotalLateFee+=extradays*5
                    cursor.execute('select bookid,bookname,author,date3,date_add(date3, interval 2 week) from books b natural join borrowedbooks bo where b.BookID=%s and bo.book3=%s and bo.memberid=%s'%(bookid,bookid,memid))
                j=1

                for a in cursor.fetchall()[0]:
                    Label(table,text=a,width=20,bg='#FFFEF2').grid(row=i,column=j,padx=0.5,pady=0.5)
                    j+=1
            i+=1

        try:
            TotalFeeLabel.destroy()
        except:
            pass

        TotalFeeLabel=Label(main,text='Total Late Fee: AED %s'%(TotalLateFee),font=('Bahnschrift',13),bg='#D7D7D7')
        TotalFeeLabel.place(relx=0.6,rely=0.67,anchor='se')

    def borrowback():
        global table, confirmborrowbutton, BackButton, w, w1

        try:
            closew()
        except:
            pass

        table.destroy()
        confirmborrowbutton.destroy()
        borrowtable()
        widgets3()
        BackButton.config(command=back)

    def returnback():
        global table, removebutton, BackButton, w, w1

        try:
            closew1()
        except:
            pass
        try:
            closew()
        except:
            pass

        table.destroy()
        removebutton.destroy()
        borrowtable()
        widgets3()
        BackButton.config(command=back)

    def borrowbooks():
        global borrowbutton, returnbutton, memid, table, d2, confirmborrowbutton, BackButton, TotalFeeLabel
        
        try:
            TotalFeeLabel.destroy()
        except:
            pass

        borrowbutton.destroy()
        returnbutton.destroy()

        try:
            table.destroy()
        except:
            pass

        BackButton.config(command=borrowback)
        
        table=Canvas(main,bg='black',highlightthickness=0)
        table.grid(row=1,column=1)
            
        Label(table,text='BookID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
        Label(table,text='BookName',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
        Label(table,text='Author',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
        Label(table,text='PubYear',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)
        
        cursor.execute('select book1,book2,book3 from borrowedbooks where memberid=%s'%memid)
        result=cursor.fetchall()[0]
        cursor.execute('select bookid,copies from books;')
        result2=cursor.fetchall()
        d2={}
        Label(table,bg='#F3F3F3').grid(row=0,column=0,sticky='nsew')
        i=1
        for e in result2:
            if e[0] not in result and e[1]!=0:
                Checkbutton(table,bg='#F3F3F3',command=borrowreturncheck).grid(row=i,column=0)
                chkbtn=table.grid_slaves(row=i,column=0)
                chkbtn[0].deselect()
                cursor.execute('select bookid,bookname,author,pubyear from books where bookid=%s'%e[0])
                j=1
                for a in cursor.fetchall()[0]:
                    Label(table,text=a,width=20,bg='#FFFEF2').grid(row=i,column=j,padx=0.5,pady=0.5)
                    j+=1
            i+=1
        confirmborrowbutton=Button(main,text='Confirm',command=borrowsave,height=2,width=10,bg='#069408',activebackground='#06C308',font=('Bahnschrift',12))
        confirmborrowbutton.place(relx=0.44,rely=0.715)

    def removenone(listvar):
        l2=[]
        try:
            for tup in listvar:
                for var in tup:
                    if var!=None:
                        l2.append(var)
        except:
            l2=[]
            
        return l2

    def borrowsave():
        global memid, d2
        
        l=list(d2)
        c=False
        count=0
        cursor.execute('select bookid from books;')
        result2=cursor.fetchall()
        cursor.execute('select book1,book2,book3 from borrowedbooks where memberid=%s'%memid)
        result=cursor.fetchall()
        sdate=str(datetime.today())
        
        for e in l:
            if (len(l)+len(removenone(result)))>3:
                errormsg=Label(main,text='You can only borrow 3 books at a time',width=30,font=('Bahnschrift',10),bg='#D7D7D7',fg='red')
                errormsg.place(relx=0.64,rely=0.71,anchor='se')
                errormsg.after(1200,errormsg.destroy)
                break

            bookid=result2[e-1][0]
            for a in range(3):
                cursor.execute('select book1,book2,book3 from borrowedbooks where memberid=%s'%memid)
                result=cursor.fetchall()[0]
                if result[a]==None:
                    if a==0:
                        cursor.execute('update borrowedbooks set book1=%s,date1="%s" where memberid=%s'%(bookid,sdate,memid))
                        cursor.execute('update books set copies=copies-1 where bookid=%s'%(bookid))
                    elif a==1:
                        cursor.execute('update borrowedbooks set book2=%s,date2="%s" where memberid=%s'%(bookid,sdate,memid))
                        cursor.execute('update books set copies=copies-1 where bookid=%s'%(bookid))
                    else:
                        cursor.execute('update borrowedbooks set book3=%s,date3="%s" where memberid=%s'%(bookid,sdate,memid))
                        cursor.execute('update books set copies=copies-1 where bookid=%s'%(bookid))
                    conn.commit()
                    c=True
                    break
        if len(l)==0:
            c=True

        if c==True:
            messagebox.showinfo("Library", "Changes saved Successfully")
            borrowback()
            
    def borrowreturncheck():
        global d2, bookid
        
        x = main.winfo_pointerx()
        y = main.winfo_pointery()
        widget = main.winfo_containing(x,y)
        r=widget.grid_info()['row']
        bookid=(table.grid_slaves(row=r,column=1))[0]['text']
        
        if r in d2:
            del d2[r]
        else:
            d2[r]=1
            
    def returnbooks():
        global memid, i, borrowbutton, returnbutton, d2, removebutton, BackButton, paid, TotalFeeLabel
        
        try:
            TotalFeeLabel.destroy()
        except:
            pass

        borrowbutton.destroy()
        returnbutton.destroy()

        BackButton.config(command=returnback)

        paid=False

        d2={}
        cursor.execute('select book1,book2,book3 from borrowedbooks where memberid=%s'%memid)
        result=cursor.fetchall()
        Label(table,bg='#F3F3F3').grid(row=0,column=0,sticky='nsew')
        i=1
        for b_id in result[0]:
            if b_id !=None:
                Checkbutton(table,bg='#F3F3F3',command=borrowreturncheck).grid(row=i,column=0)
                chkbtn=table.grid_slaves(row=i,column=0)
                chkbtn[0].deselect()
            i+=1
        removebutton=Button(main,text='Confirm',command=returnsave,height=2,width=10,bg='#069408',activebackground='#06C308',font=('Bahnschrift',12))
        removebutton.place(relx=0.44,rely=0.7)

    def paidfn():
        global paid
        
        paid=True
        cancel()
        returnsave()

    def cancel():
        global conn

        conn.rollback()
        closew1()

    def closew1(*args):
        global w1, removebutton, RequestButton, SearchButton, main, identry
        
        identry.bind('<Return>',idsearch)
        removebutton.config(state=ACTIVE)
        RequestButton.config(state=ACTIVE,bg='#6A6A6A')
        SearchButton.config(state=ACTIVE,bg='#6A6A6A')
        w1.destroy()
        
    def returnsave():
        global bookid, memid, paid, w1
        
        LateFee=0
        sdate=str(datetime.today())

        if len(d2)==0:
            FeeLabel=Label(main,text='Late Fee: AED %s'%(LateFee),font=('Bahnschrift',13),bg='#D7D7D7')
            FeeLabel.place(relx=0.58,rely=0.67,anchor='se')

        for n in d2:
            if n==1:
                cursor.execute('select datediff("%s",date1) from borrowedbooks where memberid=%s'%(sdate,memid))
                extradays=(cursor.fetchall()[0][0])-14
                if extradays>0:
                    LateFee+=extradays*5
                cursor.execute('update borrowedbooks set book1=null,date1=null where memberid=%s'%(memid))
                cursor.execute('update books set copies=copies+1 where bookid=%s'%(bookid))
            elif n==2:
                cursor.execute('select datediff("%s",date2) from borrowedbooks where memberid=%s'%(sdate,memid))
                extradays=(cursor.fetchall()[0][0])-14
                if extradays>0:
                    LateFee+=extradays*5
                cursor.execute('update borrowedbooks set book2=null,date2=null where memberid=%s'%(memid))
                cursor.execute('update books set copies=copies+1 where bookid=%s'%(bookid))
            elif n==3:
                cursor.execute('select datediff("%s",date3) from borrowedbooks where memberid=%s'%(sdate,memid))
                extradays=(cursor.fetchall()[0][0])-14
                if extradays>0:
                    LateFee+=extradays*5
                cursor.execute('update borrowedbooks set book3=null,date3=null where memberid=%s'%(memid))
                cursor.execute('update books set copies=copies+1 where bookid=%s'%(bookid))
            if LateFee==0 or paid==True:
                conn.commit()
                messagebox.showinfo("Library", "Changes saved Successfully")
                returnback()
            else:
                global removebutton, RequestButton, SearchButton, identry

                removebutton.config(state=DISABLED)
                RequestButton.config(state=DISABLED,bg='#9B9B9B')
                SearchButton.config(state=DISABLED,bg='#9B9B9B')
                identry.unbind('<Return>')
                
                w1=Tk()
                w1.configure(bg='#D7D7D7')
                w1.geometry('400x150')
                w1.title('Library')
                w1.eval('tk::PlaceWindow . center')
                w1.resizable(width=False, height=False)

                w1.protocol("WM_DELETE_WINDOW", closew1)

                FeeLabel1=Label(w1,text="Late Fee: AED %s"%(LateFee),bg='#D7D7D7',font=('Bahnschrift',16))
                FeeLabel1.place(relx=0.705,rely=0.3,anchor='se')
                PaidButton=Button(w1,text='Paid',bg='#069408',font=('Bahnschrift',12),height=2,width=10,activebackground='#06C308',command=paidfn)
                PaidButton.place(relx=0.3,rely=0.85,anchor='se')
                CancelButton=Button(w1,text='Cancel',font=('Bahnschrift',12),height=2,width=10,bg='#FF1B1B',activebackground='#FF3E3E',command=cancel)
                CancelButton.place(relx=0.95,rely=0.85,anchor='se')

                w1.mainloop()

    def request(*args):
        global RequestButton, SearchButton, borrowbutton, returnbutton, confirmborrowbutton, removebutton, identry
        global w, MemberID_Entry, Book_Entry, Author_Entry, Email_Entry

        try:
            borrowbutton.config(state=DISABLED,bg='#9B9B9B')
            returnbutton.config(state=DISABLED,bg='#9B9B9B')
        except:
            pass

        try:
            confirmborrowbutton.config(state=DISABLED)
        except:
            pass
        try:
            removebutton.config(state=DISABLED)
        except:
            pass

        identry.unbind('<Return>')
        
        RequestButton.config(state=DISABLED,bg='#9B9B9B')
        SearchButton.config(state=DISABLED,bg='#9B9B9B')
        w=Tk()
        w.grab_set()
        w.configure(bg='#D7D7D7')
        w.geometry('400x250')
        w.title('Book Request')
        w.eval('tk::PlaceWindow . center')
        w.resizable(width=False, height=False)

        w.grid_rowconfigure(0,weight=1)
        w.grid_rowconfigure(3,weight=1)
        w.grid_columnconfigure(0,weight=1)
        w.grid_columnconfigure(4,weight=1)

        MemberID_Label=Label(w,text="Enter MemberID:",bg='#D7D7D7',font=('Bahnschrift',15)).place(relx=0.4,rely=0.2,anchor='se')
        MemberID_Entry=Entry(w)
        MemberID_Entry.place(relx=0.5,rely=0.11)
        Book_Label=Label(w,text="Enter Book Name:",bg='#D7D7D7',font=('Bahnschrift',15)).place(relx=0.426,rely=0.348,anchor='se')
        Book_Entry=Entry(w)
        Book_Entry.place(relx=0.5,rely=0.26)
        Author_Label=Label(w,text="Enter Author Name:",bg='#D7D7D7',font=('Bahnschrift',15)).place(relx=0.465,rely=0.498,anchor='se')
        Author_Entry=Entry(w)
        Author_Entry.place(relx=0.5,rely=0.41)
        Email_Label=Label(w,text="Enter Email to get notified:",bg='#D7D7D7',font=('Bahnschrift',12)).place(relx=0.498,rely=0.649,anchor='se')
        Email_Entry=Entry(w)
        Email_Entry.place(relx=0.5,rely=0.56)
        Label(w,text='(Optional)',bg='#D7D7D7',font=('Bahnschrift',8)).place(relx=0.725,rely=0.73,anchor='se')

        ConfirmButton=Button(w,text='Confirm',bg='#069408',font=('Bahnschrift',12),activebackground='#06C308',command=saverequest)
        ConfirmButton.place(relx=0.59,rely=0.95,anchor='se')
        
        w.bind('<Return>',saverequest)
        w.protocol("WM_DELETE_WINDOW", closew)

    def closew():
        global w, RequestButton, SearchButton, main, borrowbutton, returnbutton, confirmborrowbutton, removebutton, identry

        try:
            borrowbutton.config(state=ACTIVE,bg='#6A6A6A')
            returnbutton.config(state=ACTIVE,bg='#6A6A6A')
        except:
            pass
        try:
            confirmborrowbutton.config(state=ACTIVE)
        except:
            pass
        try:
            removebutton.config(state=ACTIVE)
        except:
            pass

        identry.bind('<Return>',idsearch)
        w.destroy()
        RequestButton.config(state=ACTIVE,bg='#6A6A6A')
        SearchButton.config(state=ACTIVE,bg='#6A6A6A')
        main.update_idletasks()
            
    def saverequest(*args):
        global w, MemberID_Entry, Book_Entry, Author_Entry, Email_Entry

        if Email_Entry.get()=='':
            email='null'
        else:
            email=Email_Entry.get()

        cursor.execute('select memberid from members')

        result=cursor.fetchall()
        try:
            MemberID=int(MemberID_Entry.get())
            if (MemberID,) in result:
                if Book_Entry.get()=='':
                    Label(w,width=20,bg='#D7D7D7').place(relx=0.28,rely=0.025)
                    Error=Label(w,text='Book Name cannot be blank',font=('Bahnschrift',10),fg='red',bg='#D7D7D7').place(relx=0.28,rely=0.025)
                    
                elif Author_Entry.get()=='':
                    Label(w,width=20,bg='#D7D7D7').place(relx=0.28,rely=0.025)
                    Error=Label(w,text='Author Name cannot be blank',font=('Bahnschrift',10),fg='red',bg='#D7D7D7').place(relx=0.28,rely=0.025)

                else:
                    cursor.execute('insert into requests values(%s,"%s","%s","%s")'%(MemberID,Book_Entry.get(),Author_Entry.get(),email))
                    conn.commit()
                    ty=Label(w,text='Thank you',font=('Bahnschrift',25),height=6,width=21,bg='#D7D7D7')
                    ty.place(relx=0,rely=0)
                    ty.after(1500,closew)
                
            else:
                Label(w,width=50,bg='#D7D7D7').place(relx=0.28,rely=0.025)
                Error=Label(w,text='Enter a valid ID',font=('Bahnschrift',10),fg='red',bg='#D7D7D7').place(relx=0.38,rely=0.025)
        except:
            Label(w,width=20,bg='#D7D7D7').place(relx=0.28,rely=0.025)
            errormsg=Label(w,text='Enter a valid ID',font=('Bahnschrift',10),fg='red',bg='#D7D7D7')
            errormsg.place(relx=0.38,rely=0.025)
            errormsg.after(1200,errormsg.destroy)
        
    global main, identry, SearchButton

    main.destroy()
    
    main=Tk()
    main.configure(bg='#D7D7D7')
    main.geometry('800x500')
    main.title('Library')
    main.eval('tk::PlaceWindow . center')
    main.resizable(False,False)

    main.grid_rowconfigure(0,weight=1)
    main.grid_rowconfigure(3,weight=1)
    main.grid_columnconfigure(0,weight=1)
    main.grid_columnconfigure(4,weight=1)

    clocklabel=Label(main,width=25,font=('Yu Gothic bold',17),bg='#D7D7D7')
    clocklabel.place(relx=0.37,rely=0.2,anchor='se')
    clock()

    Label(main,text='Enter MemberID:',font=('Bahnschrift',10),bg='#D7D7D7').place(relx=0.43,rely=0.163,anchor='se')
    identry=Entry(main,fg='grey')
    identry.place(relx=0.585,rely=0.16,anchor='se')
    identry.insert(0,'eg:10001')
    SearchButton=Button(text='Search',height=1,width=9,font=('Bahnschrift',10),bg='#6A6A6A',activebackground='#9B9B9B',command=idsearch)
    SearchButton.place(relx=0.685,rely=0.17,anchor='se')
    identry.bind('<FocusIn>',focus)
    identry.bind('<Return>',idsearch)

    global BackButton, RequestButton
    
    ExitButton=Button(main,text='Exit',height=2,width=10,font=('Bahnschrift',11),bg='#FF1B1B',activebackground='#FF3E3E',command=exitfn)
    ExitButton.place(relx=0.97,rely=0.96,anchor='se')
    BackButton=Button(main,text='< Back',height=2,width=10,font=('Bahnschrift',11),bg='#EFB700',activebackground='#EFCA50',command=back)
    BackButton.place(relx=0.84,rely=0.96,anchor='se')
    RequestButton=Button(text='Request A Book',height=2,width=18,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=request)
    RequestButton.place(relx=0.22,rely=0.96,anchor='se')

    main.protocol("WM_DELETE_WINDOW", exitfn)

    main.mainloop()

def requeststable():
    global BackButton, RemoveButton, canvas, table, scrollbar
    
    RemoveButton=Button(main,text='Remove Record(s)',height=1,width=15,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=removereq)
    RemoveButton.place(relx=0.97,rely=0.172,anchor='se')

    cursor.execute('select * from requests')
    n=len(cursor.fetchall())
    if n>9:
        n=9
    
    canvas=Canvas(main,height=25+23*n,width=595,bg='#D7D7D7',highlightthickness=0)
    canvas.grid_propagate(False)
    canvas.grid(row=1,column=1)
    scrollbar=ttk.Scrollbar(main,orient=VERTICAL,command=canvas.yview)
    scrollbar.grid(row=1,column=2,sticky='nsw')

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))

    table=Canvas(canvas,bg='black',highlightthickness=0)
    canvas.create_window((0,0),window=table)
    
    cursor.execute('select * from requests')

    buffer=Canvas(main,height=25+23*n,width=595,bg='#D7D7D7',highlightthickness=0)
    buffer.grid_propagate(False)
    buffer.grid(row=1,column=1)

    Label(table,text='MemberID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
    Label(table,text='Book Name',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
    Label(table,text='Author',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
    Label(table,text='Email',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)

    i=1
    j=1
    for e in cursor.fetchall():
        for a in e:
            if a=='null':
                a=''
            Label(table,text=a,height=1,width=20,bg='#FFFEF2').grid(row=i,column=j,padx=0.5,pady=0.5)
            j+=1
            if j%5==0:
                i+=1
                j=1
    try:
        BackButton.config(command=back)
    except:
        pass
    
    canvas.update_idletasks()
    canvas.yview_moveto('0.0')
    buffer.destroy()    

def removereq():
    global d, result, BackButton, ConfirmRemoveButton, table, RemoveButton, canvas

    RemoveButton.destroy()
    
    cursor.execute('select * from requests')
    n=len(cursor.fetchall())
    if n>9:
        n=9
    
    canvas.configure(height=25*(n+1),width=627)

    buffer=Canvas(main,height=28+22*n,width=627,bg='#D7D7D7',highlightthickness=0)
    buffer.grid_propagate(False)
    buffer.grid(row=1,column=1)
    
    d={}
    i=1
    cursor.execute('select * from requests')
    result=cursor.fetchall()
    Label(table,bg='#F3F3F3').grid(row=0,column=0,sticky='nsew')
    for a in result:
        Checkbutton(table,bg='#F3F3F3',command=check).grid(row=i,column=0)
        chkbtn=table.grid_slaves(row=i,column=0)
        chkbtn[0].deselect()
        i+=1

    canvas.update_idletasks()
    buffer.destroy()
    canvas.yview_moveto('0.0')
    
    ConfirmRemoveButton=Button(main,text='Remove',command=confirmremove3,height=1,width=10,bg='#069408',font=('Bahnschrift',10),activebackground='#06C308')
    ConfirmRemoveButton.grid(row=3,column=1)
    BackButton.config(command=removeback3)

def confirmremove3():
        cursor.execute('select * from requests')
        result=cursor.fetchall()
        for n in d:
            cursor.execute('delete from requests where memberid=%s and bookname="%s"'%(result[n-1][0],result[n-1][1]))
            conn.commit()
        messagebox.showinfo("Library", "Changes saved Successfully")
        removeback3()

def removeback3():
        global canvas
        global ConfirmRemoveButton
        global scrollbar

        scrollbar.destroy()
        canvas.destroy()
        ConfirmRemoveButton.destroy()
        requeststable()
        BackButton.config(command=back)

def viewreq():
    try:
        ViewBookButton.destroy()
        ViewMemButton.destroy()
        BorrowButton.destroy()
        ViewReqButton.destroy()        
    except:
        pass

    global main, table, canvas, scrollbar, BackButton

    main.geometry('800x500')
    main.grid_columnconfigure(4,weight=0)
    main.eval('tk::PlaceWindow . center')
    main.resizable(False,False)

    ExitButton.place(relx=0.97,rely=0.96,anchor='se')
    BackButton=Button(main,text='< Back',height=2,width=10,font=('Bahnschrift',11),bg='#EFB700',activebackground='#EFCA50',command=back)
    BackButton.place(relx=0.84,rely=0.96,anchor='se')
    
    cursor.execute('select * from requests')
    if len(cursor.fetchall())!=0:
        requeststable()
    else:
        Label(text='No requests present',font=('Bahnschrift',25),bg='#D7D7D7').place(relx=0.68,rely=0.5,anchor='se')
        

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
