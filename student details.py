
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

# Database connection
#_____________________________________________________________________________
db = mysql.connector.connect(user='root', password='root', port=3306,database="studentdatabase")
mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS studentdatabase")

mycursor.execute("CREATE TABLE IF NOT EXISTS student (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100),email VARCHAR(100),contact VARCHAR(12),gender VARCHAR(12),class VARCHAR(5))")
#_______________________________________________________________________________
# styling component
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)
#__________________________________________________________________________________
main = Tk()
main.title('School Management System')
main.geometry('1000x600')


lf_bg = 'purple' 
cf_bg = 'orange' 

name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
class_strvar = StringVar()


#Reset all entry boxes
def reset_fields():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, class_strvar
   for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar', 'class_strvar']:
       exec(f"{i}.set('')")
def reset_form():
   global tree
   #tree.delete(*tree.get_children())
   reset_fields()


# save the data
def insert_value():
    name_entry=name_strvar.get()
    email_entry=email_strvar.get()
    contact_entry=contact_strvar.get()
    genter_entry=gender_strvar.get()
    class_entry=class_strvar.get()
   
    
    db = mysql.connector.connect(user='root', password='root', port=3306,database="studentdatabase")
    mycursor = db.cursor()
    mycursor.execute('INSERT INTO student(name, email, contact, gender, class)VALUES (%s, %s, %s, %s, %s)', (name_entry, email_entry, contact_entry,genter_entry,class_entry))

    db.commit()
    messagebox.showinfo("showinfo", "Data stored")
    reset_fields()
    display_records()


# auto treeview show datas
def display_records():
    tree.delete(*tree.get_children())
   
    

    curr = mycursor.execute('SELECT * FROM student')
    data=mycursor.fetchall()
    
    for records in data:
       tree.insert('', END, values=records)


# select data from table
def view_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
   if not tree.selection():
       mb.showerror('Error!', 'Please select a record to view')
   else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        name_strvar.set(selection[1]); email_strvar.set(selection[2])
        contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
        class_strvar.set(selection[5])


# Delete a record from treeview
def remove_record():
    if not tree.selection():
       mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        tree.delete(current_item)
        curr = mycursor.execute('DELETE FROM student WHERE id=%d' % selection[0])
        data=mycursor.fetchall()

        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
        display_records()
     

Label(main, text="SCHOOL MANAGEMENT SYSTEM", font=headlabelfont, bg='Blue').pack(side=TOP, fill=X)
left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)
center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)
right_frame = Frame(main, bg="Gray")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)



Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(relx=0.33, rely=0.05)
name_entry=Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.1)


Label(left_frame, text="Contact Number", font=labelfont, bg=lf_bg).place(relx=0.175, rely=0.18)
contact_entry=Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.23)

Label(left_frame, text="Email Address", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.31)
email_entry=Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.36)

Label(left_frame, text="Gender", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.44)
enter_entry=OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=45, rely=0.49, relwidth=0.5)

Label(left_frame, text="Class", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.6)
class_entry=Entry(left_frame, width=19, textvariable=class_strvar, font=entryfont).place(x=20, rely=0.65)

Button(left_frame, text='Submit and Add Record', font=labelfont, command=insert_value, width=18).place(relx=0.025, rely=0.85)

Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.45)
Label(right_frame, text='Students Records', font=headlabelfont, bg='red', fg='LightCyan').pack(side=TOP, fill=X)




tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                   columns=('Student ID', "Name", "Email Address", "Contact Number", "Gender", "Class"))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Class', text='Class', anchor=CENTER)

tree.column('#0',width=80 , stretch=NO)
tree.column('#1', width=100  ,stretch=NO)
tree.column('#2', width=100   ,stretch=NO)
tree.column('#3', width=50  ,stretch=NO)
tree.column('#4', width=50  ,stretch=NO)
tree.column('#5', width=50  ,stretch=NO)


display_records()


tree.place(y=30, relwidth=1, relheight=0.9, relx=0)





main.update()
main.mainloop()

