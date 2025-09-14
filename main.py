from tkinter import *
from tkinter import messagebox        #not a class, is another module, hence why needs importing again
from random import randint,choice,shuffle
import pyperclip                      #for automating copying of passwords once generated for instant use
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_password():
    pass_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_list += [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]


    shuffle(password_list)
    password="".join(password_list)            #join string method
    pass_input.insert(0, password)
    pyperclip.copy(password)      #to auto copy passwords for immediate sign-in somewhere

    # ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    new_data={
        web_input.get().strip().title() : {
        "email" : email_input.get(),
        "password" : pass_input.get(),
        }
    }

    if len(web_input.get())==0 or len(pass_input.get())==0:
        messagebox.showinfo(title="Oops",message="Can't leave any fields empty.")
    else:
        try:
            with open("Password_Save_File.json",mode="r") as data_file:
                # json.dump(new_data,data_file,indent=4)
                data=json.load(data_file)    #update - reading the old data
        except FileNotFoundError:
            with open("Password_Save_File.json", mode="w") as data_file:  #creating the file
                json.dump(new_data, data_file, indent=4)                  #updating the new file with the newly entered data
        else:
            data.update(new_data)       #try worked - so just update the new data onto the existing file's old data
            with open("Password_Save_File.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)    #update - saving updated data
                messagebox.showinfo(title="Success",
                                    message=f"Password for {list(new_data.keys())[0]} saved successfully"
                )
        finally:
            web_input.delete(0, END)   #whichever works -try/except/else, we need to clear the entry fields
            pass_input.delete(0, END)
#------------------------------FIND PASSWORD(SEARCH)----------------------------------#
def find_password():
    search_data=web_input.get().title()
    try :
        with open("Password_Save_File.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Search Result", message="No Data File Found.")
    else:
        if search_data in data:  # search in the file
            email = data[search_data]["email"]
            passw = data[search_data]["password"]
            messagebox.showinfo(title=f"{search_data}", message=f" Email : {email}\nPassword : {passw}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for the website {search_data} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window=Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)
window.grid_columnconfigure(0,minsize=100)

canvas=Canvas(width=200,height=200)
lock_img=PhotoImage(file="logo.png")
canvas.create_image(100,100,image=lock_img)
canvas.grid(row=0,column=1)

website_label=Label(text="Website : ")
website_label.grid(row=1,column=0,sticky="e",padx=(0,8))

email_label=Label(text="Email/Username : ")
email_label.grid(row=2,column=0,sticky="e",padx=(0,8))

password_label=Label(text="Password : ")
password_label.grid(row=3,column=0,sticky="e",padx=(0,8))

search_button=Button(text="Search",command=find_password,width=13)
search_button.grid(row=1,column=2,pady=(10,0))

generate_button=Button(text="Generate Password",command=generate_password)
generate_button.grid(row=3,column=2,pady=(10,0))

add_button=Button(text="Add",width=36,command=save)
add_button.grid(row=4,column=1,columnspan=2,pady=(10,0))

web_input=Entry(width=21)
web_input.grid(row=1,column=1,sticky="ew",pady=(10,0))
web_input.focus()                 #start cursor in the first field

email_input=Entry(width=35)
email_input.grid(row=2,column=1,columnspan=2,sticky="ew",pady=(10,0))
email_input.insert(0,"example123@email.com")

pass_input=Entry(width=21)
pass_input.grid(row=3,column=1,sticky="ew",padx=(0,8),pady=(10,0))













window.mainloop()