from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as connect
from datetime import datetime

def mainfn():
    global ViewMemButton
    global ViewBookButton
    global BorrowButton
    global main
    global ExitButton
    
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
    BorrowButton=Button(text='Borrow/Return Books',command=borrowreturn,wraplength=130,bg='#FF8F37',activebackground='#FFA45D',font=('Bahnschrift',14),height=3,width=14)
    BorrowButton.place(relx=0.36,rely=0.5,anchor='nw')
    ExitButton=Button(text='Exit',height=2,width=10,font=('Bahnschrift',11),bg='#FF1B1B',activebackground='#FF3E3E',command=main.destroy)
    ExitButton.place(relx=0.96,rely=0.94,anchor='se')

    main.mainloop()

def memberstable():
        global table
        global canvas
        global scrollbar

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

def back():
    main.destroy()
    mainfn()

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
    
def memberlist():

    def clock():
        now=datetime.now()
        date=str(now.strftime('%d %b %Y'))
        time=str(now.strftime('%H:%M:%S'))

        clocklabel.config(text='%s\n%s'%(date,time))

        clocklabel.after(1, clock)

    def widgets():
        global AddButton, EditButton, RemoveButton, clocklabel, clocklabel2
        
        AddButton=Button(main,text='Add Record(s)',height=1,width=13,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=add)
        AddButton.place(relx=0.785,rely=0.172,anchor='se')
        EditButton=Button(main,text='Edit Record',height=1,width=10,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=search)
        EditButton.place(relx=0.62,rely=0.172,anchor='se')
        RemoveButton=Button(main,text='Remove Record(s)',height=1,width=15,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=remove)
        RemoveButton.place(relx=0.97,rely=0.172,anchor='se')

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
        Label(main,width=25,font=('Bahnschrift',10),bg='#D7D7D7').grid(row=2,column=1)
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
        Label(main,width=25,font=('Bahnschrift',10),bg='#D7D7D7').grid(row=2,column=1)
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
            Label(main,text='Error, please try again',width=25,font=('Bahnschrift',10),bg='#D7D7D7',fg='red').grid(row=2,column=1)

    def edit(*args):
        global errorlabel
        global notfound
        
        try:
            global result
            global MemberID_Entry
            global Name_Entry
            global DOB_Entry
            global DOJ_Entry
            global table
            global SaveButton
            global canvas
            global AddButton
            global EditButton
            global RemoveButton
            global scrollbar

            cursor.execute('select * from members where memberid=%s'%(EditSearch.get()))
            result=cursor.fetchall()
            if result==[]:
                try:
                    errorlabel.destroy()
                except:
                    pass
                try:
                    notfound.destroy()
                except:
                    pass
                notfound=Label(main,text='Record not found',font=('Bahnschrift',8),bg='#D7D7D7',fg='red')
                notfound.place(relx=0.53,rely=0.21,anchor='se')
                EditSearch.select_range(0,END)
            else:
                searchback()
                AddButton.destroy()
                EditButton.destroy()
                RemoveButton.destroy()
                scrollbar.destroy()
                
                BackButton.config(command=editback)
                try:
                    errorlabel.destroy()
                except:
                    pass
                try:
                    notfound.destroy()
                except:
                    pass
                
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
            try:
                errorlabel.destroy()
            except:
                pass
            try:
                notfound.destroy()
            except:
                pass
            errorlabel=Label(main,text='Enter a valid ID',width=15,font=('Bahnschrift',8),bg='#D7D7D7',fg='red')
            errorlabel.place(relx=0.53,rely=0.21,anchor='se')
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
        global d
        global result
        global BackButton
        global ConfirmRemoveButton
        global table
        global AddButton
        global RemoveButton
        global EditButton
        global canvas

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
        global Add_Combobox
        global SaveButton
        global BackButton
        global Add_Label
        global AddButton
        global EditButton
        global RemoveButton

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
            Label(main,text='Error in entry %s'%(i),width=25,font=('Bahnschrift',10),bg='#D7D7D7',fg='red').grid(row=2,column=1)
        
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
    except:
        pass
    
    global main
    main.geometry('800x500')
    main.grid_columnconfigure(4,weight=0)
    main.eval('tk::PlaceWindow . center')
    main.resizable(False,False)

    memberstable()

    global BackButton
    
    ExitButton.place(relx=0.97,rely=0.96,anchor='se')
    BackButton=Button(main,text='< Back',height=2,width=10,font=('Bahnschrift',11),bg='#EFB700',activebackground='#EFCA50',command=back)
    BackButton.place(relx=0.84,rely=0.96,anchor='se')
    widgets()

def bookstable():
    global table
    global canvas
    global scrollbar
    
    cursor.execute('select * from books')
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

    buffer=Canvas(main,height=28+22*n,width=595,bg='#D7D7D7',highlightthickness=0)
    buffer.grid_propagate(False)
    buffer.grid(row=1,column=1)
        
    Label(table,text='BookID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
    Label(table,text='BookName',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
    Label(table,text='Author',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
    Label(table,text='PubYear',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)

    cursor.execute('select * from books')
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
    buffer.destroy()
    canvas.yview_moveto('0.0')
    
def booklist():

    def buttons2():
        global AddButton
        global EditButton
        global RemoveButton
        
        AddButton=Button(main,text='Add Record(s)',height=1,width=13,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=add2)
        AddButton.place(relx=0.785,rely=0.172,anchor='se')
        EditButton=Button(main,text='Edit Record',height=1,width=10,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=search2)
        EditButton.place(relx=0.62,rely=0.172,anchor='se')
        RemoveButton=Button(main,text='Remove Record(s)',height=1,width=15,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B',command=remove2)
        RemoveButton.place(relx=0.97,rely=0.172,anchor='se')


    def searchback2():
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
        Label(main,width=25,font=('Bahnschrift',10),bg='#D7D7D7').grid(row=2,column=1)
        buttons2()
    
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
        Label(main,width=25,font=('Bahnschrift',10),bg='#D7D7D7').grid(row=2,column=1)
        bookstable()
        buttons2()

    def removeback2():
        global canvas
        global ConfirmRemoveButton
        global scrollbar

        scrollbar.destroy()
        canvas.destroy()
        ConfirmRemoveButton.destroy()
        bookstable()
        buttons2()

    def editsave2():
        try:
            global conn
            global BookID_Entry
            global BookName_Entry
            global Author_Entry
            global PubYear_Entry
            global main

            for a in result:
                if BookID_Entry.get()!=a[0]:
                    cursor.execute('update books set bookid=%s where bookid=%s'%(BookID_Entry.get(),a[0]))
                if BookName_Entry.get()!=a[1]:
                    cursor.execute('update books set bookname="%s" where bookid=%s'%(BookName_Entry.get(),BookID_Entry.get()))
                if Author_Entry.get()!=a[2]:
                    cursor.execute('update books set author="%s" where bookid=%s'%(Author_Entry.get(),BookID_Entry.get()))
                if PubYear_Entry.get()!=a[3]:
                    cursor.execute('update books set pubyear="%s" where bookid=%s'%(PubYear_Entry.get(),BookID_Entry.get()))
            conn.commit()
            messagebox.showinfo("Library", "Changes saved Successfully")
            editback2()
        except:
            Label(main,text='Error, please try again',width=25,font=('Bahnschrift',10),bg='#D7D7D7',fg='red').grid(row=2,column=1)

    def edit2(*args):
        global errorlabel
        global notfound
        
        try:
            global result
            global BookID_Entry
            global BookName_Entry
            global Author_Entry
            global PubYear_Entry
            global table
            global SaveButton
            global canvas
            global AddButton
            global EditButton
            global RemoveButton
            global scrollbar

            cursor.execute('select * from books where bookid=%s'%(EditSearch.get()))
            result=cursor.fetchall()
            if result==[]:
                try:
                    errorlabel.destroy()
                except:
                    pass
                try:
                    notfound.destroy()
                except:
                    pass
                notfound=Label(main,text='Record not found',font=('Bahnschrift',8),bg='#D7D7D7',fg='red')
                notfound.place(relx=0.53,rely=0.21,anchor='se')
                EditSearch.select_range(0,END)
            else:
                searchback2()
                AddButton.destroy()
                EditButton.destroy()
                RemoveButton.destroy()
                scrollbar.destroy()
                
                BackButton.config(command=editback2)
                try:
                    errorlabel.destroy()
                except:
                    pass
                try:
                    notfound.destroy()
                except:
                    pass
                canvas.destroy()
                canvas=Canvas(main,height=206,width=595,bg='#D7D7D7',highlightthickness=0)
                canvas.grid(row=1,column=1)
                table=Canvas(canvas,bg='black',highlightthickness=0)
                table.grid()
                Label(table,text='BookID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
                Label(table,text='BookName',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
                Label(table,text='Author',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
                Label(table,text='PubYear',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)
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
                BookID_Entry.focus()

                SaveButton=Button(main,text='Save',command=editsave2,height=1,width=10,bg='#069408',font=('Bahnschrift',10),activebackground='#06C308')
                SaveButton.grid(row=3,column=1)                
        except:
            try:
                errorlabel.destroy()
            except:
                pass
            try:
                notfound.destroy()
            except:
                pass
            errorlabel=Label(main,text='Enter a valid ID',width=15,font=('Bahnschrift',8),bg='#D7D7D7',fg='red')
            errorlabel.place(relx=0.53,rely=0.21,anchor='se')
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
        global d
        global result
        global BackButton
        global ConfirmRemoveButton
        global table
        global AddButton
        global RemoveButton
        global EditButton
        global canvas

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
        
        canvas.configure(height=25*(n+1),width=627)

        buffer=Canvas(main,height=28+22*n,width=595,bg='#D7D7D7',highlightthickness=0)
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
        
        i=1
        for e in range(int(Add_Combobox.get())):
            for j in range(1,5):
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
                cursor.execute('insert into books values(%s,"%s","%s","%s")'%(int((table.grid_slaves(i,1)[0]).get()),(table.grid_slaves(i,2)[0]).get(),(table.grid_slaves(i,3)[0]).get(),(table.grid_slaves(i,4)[0]).get()))
                i+=1
            except:
                c=False
                break
        if c==True:
            conn.commit()
            messagebox.showinfo("Library", "Changes saved Successfully")
            addback2()
        else:
            Label(main,text='Error in entry %s'%(i),width=25,font=('Bahnschrift',10),bg='#D7D7D7',fg='red').grid(row=2,column=1)
        
    def search2():
        global EditSearch
        global EditLabel
        global SearchButton
        global EditButton
        global BackButton
        global table
        global canvas

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
    buttons2()
    
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
            cursor.execute('create table books(BookID int(7) primary key,BookName varchar(30),Author varchar(20),PubYear int(4))')
            cursor.execute('create table borrowedbooks(MemberID int(5) primary key,Book1 int(7),Book2 int(7),Book3 int(7))')

            cursor.execute('insert into members values(%s,"%s","%s","%s")'%(10001,'Tom Hanks','2000-01-01','2020-02-02'))
            cursor.execute('insert into members values(%s,"%s","%s","%s")'%(10002,'Porter Robinson','2004-04-08','2019-11-03'))
            cursor.execute('insert into members values(%s,"%s","%s","%s")'%(10003,'Mohammed Naasif','2005-11-20','2019-09-10'))
            cursor.execute('insert into members values(%s,"%s","%s","%s")'%(10004,'Karen Manson','1999-07-25','2021-05-12'))
            cursor.execute('insert into members values(%s,"%s","%s","%s")'%(10005,'Rahul Menon','2005-09-25','2022-04-02'))

            cursor.execute('insert into books values(%s,"%s","%s",%s)'%(1234567,'The Book Thief','Markus Zusak',2005))
            cursor.execute('insert into books values(%s,"%s","%s",%s)'%(9259987,'And Then There Were None','Agatha Christie',1939))
            cursor.execute('insert into books values(%s,"%s","%s",%s)'%(1794856,'The Kite Runner','Khaled Hosseini',2003))
            cursor.execute('insert into books values(%s,"%s","%s",%s)'%(4340938,'1984','George Orwell',1949))
            cursor.execute('insert into books values(%s,"%s","%s",%s)'%(1228739,'The Maze Runner','James Dashner',2009))

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
        wrongpass=Label(root,text='Wrong password',bg='#D7D7D7',font=('Bahnschrift',11),fg='red').grid(row=1,column=3)

def borrowreturn():
    global TopLabel
    
    def buttons3():
        global borrowbutton
        global returnbutton
        
        borrowbutton=Button(main,text='Borrow Books',command=borrowbooks,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B')
        borrowbutton.place(relx=0.3,rely=0.7)
        returnbutton=Button(main,text='Return Books',command=returnbooks,font=('Bahnschrift',11),bg='#6A6A6A',activebackground='#9B9B9B')
        returnbutton.place(relx=0.535,rely=0.7)
        
    def focus(*args):
         identry.delete(0,END)
         identry.config(fg='black')

    def idsearch(*args):
        global identry
        global memid
        global borrowbutton
        global returnbutton
        global removebutton
        global table
        global confirmremovebutton
        global TopLabel

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
                
                Label(main,text='Invalid ID',font=('Bahnschrift',9),bg='#D7D7D7',fg='red').place(relx=0.53,rely=0.21,anchor='se')
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
                
                Label(main,width=10,font=('Bahnschrift',9),bg='#D7D7D7').place(relx=0.53,rely=0.21,anchor='se')
                TopLabel=Label(main,width=14,text='MemberID:%s'%memid,font=('Bahnschrift',15),bg='#D7D7D7')
                TopLabel.place(relx=0.62,rely=0.3,anchor='se')
                borrowtable()
                buttons3()
        except:
            
            Label(main,text='Invalid ID',font=('Bahnschrift',9),bg='#D7D7D7',fg='red').place(relx=0.53,rely=0.21,anchor='se')
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
        global table
        global canvas
        global scrollbar
        global memid
        global i

        table=Canvas(main,bg='black',highlightthickness=0)
        table.grid(row=1,column=1)
            
        Label(table,text='BookID',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=1,padx=2,pady=2)
        Label(table,text='BookName',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=2,padx=2,pady=2)
        Label(table,text='Author',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=3,padx=2,pady=2)
        Label(table,text='PubYear',font='Arial 9 bold',height=1,width=20,bg='#F3F3F3').grid(row=0,column=4,padx=2,pady=2)

        cursor.execute('select book1,book2,book3 from borrowedbooks where memberid=%s'%(memid))
        result=cursor.fetchall()
        i=1
        for bookid in result[0]:
            if bookid !=None:
                cursor.execute('select * from books where BookID=%s'%bookid)
                j=1
                for a in cursor.fetchall()[0]:
                    Label(table,text=a,width=20,bg='#FFFEF2').grid(row=i,column=j,padx=0.5,pady=0.5)
                    j+=1
            i+=1

    def borrowback():
        global table
        global confirmborrowbutton
        global BackButton

        table.destroy()
        confirmborrowbutton.destroy()
        Label(main,width=30,font=('Bahnschrift',10),bg='#D7D7D7').place(relx=0.69,rely=0.71,anchor='se')
        borrowtable()
        buttons3()
        BackButton.config(command=back)

    def returnback():
        global table
        global removebutton
        global BackButton

        table.destroy()
        removebutton.destroy()
        borrowtable()
        buttons3()
        BackButton.config(command=back)

    def borrowbooks():
        global borrowbutton
        global returnbutton
        global memid
        global table
        global d2
        global confirmborrowbutton
        global BackButton

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
        cursor.execute('select bookid from books;')
        result2=cursor.fetchall()
        d2={}
        Label(table,bg='#F3F3F3').grid(row=0,column=0,sticky='nsew')
        i=1
        for e in result2:
            if e[0] not in result:
                Checkbutton(table,bg='#F3F3F3',command=borrowreturncheck).grid(row=i,column=0)
                chkbtn=table.grid_slaves(row=i,column=0)
                chkbtn[0].deselect()
                cursor.execute('select * from books where bookid=%s'%e[0])
                j=1
                for a in cursor.fetchall()[0]:
                    Label(table,text=a,width=20,bg='#FFFEF2').grid(row=i,column=j,padx=0.5,pady=0.5)
                    j+=1
            i+=1
        confirmborrowbutton=Button(main,text='Confirm',command=borrowsave,height=2,width=10,bg='#6A6A6A',activebackground='#9B9B9B',font=('Bahnschrift',12))
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
        global memid
        global d2
        
        l=list(d2)
        c=False
        count=0
        cursor.execute('select bookid from books;')
        result2=cursor.fetchall()
        cursor.execute('select book1,book2,book3 from borrowedbooks where memberid=%s'%memid)
        result=cursor.fetchall()
        
        for e in l:
            if (len(l)+len(removenone(result)))>3:
                Label(main,text='You can only borrow 3 books at a time',width=30,font=('Bahnschrift',10),bg='#D7D7D7',fg='red').place(relx=0.69,rely=0.71,anchor='se')
                break

            Label(main,width=30,font=('Bahnschrift',10),bg='#D7D7D7').place(relx=0.69,rely=0.71,anchor='se')
            bookid=result2[e-1][0]
            for a in range(3):
                cursor.execute('select book1,book2,book3 from borrowedbooks where memberid=%s'%memid)
                result=cursor.fetchall()[0]
                if result[a]==None:
                    if a==0:
                        cursor.execute('update borrowedbooks set book1=%s where memberid=%s'%(bookid,memid))
                    elif a==1:
                        cursor.execute('update borrowedbooks set book2=%s where memberid=%s'%(bookid,memid))
                    else:
                        cursor.execute('update borrowedbooks set book3=%s where memberid=%s'%(bookid,memid))
                    conn.commit()
                    c=True
                    break
        if len(l)==0:
            c=True

        if c==True:
            messagebox.showinfo("Library", "Changes saved Successfully")
            borrowback()
            
    def borrowreturncheck():
        global d2
        
        x = main.winfo_pointerx()
        y = main.winfo_pointery()
        widget = main.winfo_containing(x,y)
        row=widget.grid_info()['row']
        if row in d2:
            del d2[row]
        else:
            d2[row]=1
            
    def returnbooks():
        global memid
        global i
        global borrowbutton
        global returnbutton
        global d2
        global removebutton
        global BackButton

        borrowbutton.destroy()
        returnbutton.destroy()

        BackButton.config(command=returnback)

        d2={}
        cursor.execute('select book1,book2,book3 from borrowedbooks where memberid=%s'%memid)
        result=cursor.fetchall()
        Label(table,bg='#F3F3F3').grid(row=0,column=0,sticky='nsew')
        i=1
        for bookid in result[0]:
            if bookid !=None:
                Checkbutton(table,bg='#F3F3F3',command=borrowreturncheck).grid(row=i,column=0)
                chkbtn=table.grid_slaves(row=i,column=0)
                chkbtn[0].deselect()
            i+=1
        removebutton=Button(main,text='Confirm',command=returnsave,height=2,width=10,bg='#6A6A6A',activebackground='#9B9B9B',font=('Bahnschrift',12))
        removebutton.place(relx=0.44,rely=0.7)
        
    def returnsave():
        for n in d2:
            if n==1:
                cursor.execute('update borrowedbooks set book1=null where memberid=%s'%(memid))
            elif n==2:
                cursor.execute('update borrowedbooks set book2=null where memberid=%s'%(memid))
            elif n==3:
                cursor.execute('update borrowedbooks set book3=null where memberid=%s'%(memid))
            conn.commit()
        messagebox.showinfo("Library", "Changes saved Successfully")
        returnback()
    
    global main
    global ExitButton
    global Backbutton
    global identry

    main.destroy()
    
    main=Tk()
    main.configure(bg='#D7D7D7')
    main.geometry('650x466')
    main.title('Library')
    main.eval('tk::PlaceWindow . center')
    main.resizable(False,False)

    main.grid_rowconfigure(0,weight=1)
    main.grid_rowconfigure(3,weight=1)
    main.grid_columnconfigure(0,weight=1)
    main.grid_columnconfigure(4,weight=1)

    Label(main,text='Enter MemberID:',font=('Bahnschrift',10),bg='#D7D7D7').place(relx=0.395,rely=0.163,anchor='se')
    identry=Entry(main,fg='grey')
    identry.place(relx=0.585,rely=0.16,anchor='se')
    identry.insert(0,'eg:10001')
    SearchButton=Button(text='Search',height=1,width=9,font=('Bahnschrift',10),bg='#6A6A6A',activebackground='#9B9B9B',command=idsearch)
    SearchButton.place(relx=0.705,rely=0.17,anchor='se')
    identry.bind('<FocusIn>',focus)
    identry.bind('<Return>',idsearch)

    global BackButton

    ExitButton=Button(text='Exit',height=2,width=10,font=('Bahnschrift',11),bg='#FF1B1B',activebackground='#FF3E3E',command=main.destroy)
    ExitButton.place(relx=0.97,rely=0.96,anchor='se')
    BackButton=Button(main,text='< Back',height=2,width=10,font=('Bahnschrift',11),bg='#EFB700',activebackground='#EFCA50',command=back)
    BackButton.place(relx=0.825,rely=0.96,anchor='se')

    main.mainloop()

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
