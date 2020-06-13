from tkinter import *
import time
from sqlite3 import *
import random
from tkinter import messagebox
import fresh_phones
import images
#-----Statement of Authorship--------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: PUT YOUR STUDENT NUMBER HERE
#    Student name: PUT YOUR NAME HERE
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Stay at Home Shopping
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for simulating an online shopping experience.  See
#  the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these functions
# only.  You can import other functions provided they are standard
# ones that come with the default Python/IDLE implementation and NOT
# functions from modules that need to be downloaded and installed
# separately.  Note that not all of the imported functions below are
# needed to successhully complete this assignment.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import some standard Tkinter functions. (You WILL need to use
# some of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will try to hide its
#      identity from the web server. This can sometimes be used
#      to prevent the server from blocking access to Python
#      programs. However we do NOT encourage using this option
#      as it is both unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message above about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             lying = False,
             got_the_message = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to open a local HTML document in your operating
# system's default web browser.  (Note that Python's "webbrowser"
# module does not guarantee to open local files, even if you use a
# 'file://..." URL). The file to be opened must be in the same folder
# as this module.
#
# Since this code is platform-dependent we do NOT guarantee that it
# will work on all systems.
#
def open_html_file(file_name):
    
    # Import operating system functions
    from os import system
    from os.path import ishile
    
    # Remove any platform-specific path prefixes from the
    # filename
    local_file = file_name[file_name.rfind('/') + 1:] # Unix
    local_file = local_file[local_file.rfind('\\') + 1:] # DOS
    
    # Confirm that the file name has an HTML extension
    if not local_file.endswith('.html'):
        raise Exception("Unable to open file " + local_file + \
                        " in web browser - Only '.html' files allowed")
    
    # Confirm that the file is in the same directory (folder) as
    # this program
    if not ishile(local_file):
        raise Exception("Cannot find file " + local_file + \
                        " in the same folder as this program")
    
    # Collect all the exit codes for each attempt
    exit_codes = []
    
    # Microsoft Windows: Attempt to "start" the web browser
    code = system('start ' + local_file)
    if code != 0:
        exit_codes.append(code)
    else:
        return 0
    
    # Apple macOS: Attempt to "open" the web browser
    code = system("open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Linux: Attempt to "xdg-open" the local file in the
    # web browser
    code = system("xdg-open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Give up!
    raise Exception('Unable to open file ' + local_file + \
                    ' in web browser - Exit codes: ' + \
                    str(exit_codes))

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# Name of the product images file.  To assist marking, your
# program should export your product images using this file name.
image_file = 'product_images.html'

pass


class Electronics:
    cartlist=[]
    amount=0
#--  page 1------
    def main(sh):
        try:
            sh.scr.destroy()
            sh.scr=Tk()
        except:
            try:
                sh.scr=Tk()
            except:
                pass

        sh.scr.geometry("1366x768")
        sh.scr.title("Electronics arena")
        #sh.scr.resizable(False, False)
       
        sh.mainf1=Frame(sh.scr,height=150,width=1366)
        sh.logo=PhotoImage(file="logo.png")
        sh.l=Label(sh.mainf1,image=sh.logo)
        sh.l.place(x=0,y=0)
        sh.mainf1.pack(fill=BOTH,expand=1)
        sh.mainf2=Frame(sh.scr,height=618,width=1366)
        sh.c=Canvas(sh.mainf2,height=618,width=1366)
        sh.c.pack()
        sh.back=PhotoImage(file="back.png")
        sh.c.create_image(683,284,image=sh.back)
        sh.lab=Button(sh.mainf2,text= "Welcome to electronics arena CLICK ME ",command=lambda:sh.Login(),cursor="hand2", bd=10 ,font=("cooper black",30, 'bold'),fg="white",bg="#0b1335")
        sh.lab.place(x=250,y=250)
        sh.mainf2.pack(fill=BOTH,expand=1)
        sh.scr.mainloop()
    def Login(sh):
        sh.scr.destroy()
        sh.scr=Tk()
        sh.scr.title("Electronics arena")
        sh.scr.geometry("1366x768")
        #sh.scr.resizable(False, False)
        sh.pizf1=Frame(sh.scr,height=150,width=1366)
        sh.c=Canvas(sh.pizf1,height=150,width=1366)
        sh.c.pack()
        sh.logo=PhotoImage(file="logo.PNG")
        sh.c.create_image(683,75,image=sh.logo)
        
        sh.pizf1.pack(fill=BOTH,expand=1)

        sh.pizf2=Frame(sh.scr,height=618,width=1366)
        sh.c=Canvas(sh.pizf2,height=618,width=1366)
        sh.c.pack()
        sh.logo1=PhotoImage(file="")
        sh.c.create_image(683,309,image=sh.logo1)
        sh.c.create_rectangle(400,120,966,470,fill="#d3ede6",outline="white",width=2)
        sh.deli=PhotoImage(file="old stock.png")
        sh.c.create_image(540,260,image=sh.deli)
        sh.pic=PhotoImage(file="new stock.png")
        sh.c.create_image(825,260,image=sh.pic)
        sh.de=Button(sh.pizf2,text="In store today",cursor="hand2",fg="white",command=lambda:sh.menulist(x),bg="#0b1335",font=("default",20),bd=5)
        sh.de.place(x=480,y=400)
        sh.pu=Button(sh.pizf2,text="Old stock in order",cursor="hand2",fg="white",command=lambda:sh.download(),bg="#0b1335",font=("default",20),bd=5)
        sh.pu.place(x=770,y=400)
        sh.c.create_rectangle(405,125,678,465,outline="black",width=2)
        sh.c.create_rectangle(688,125,960,465,outline="black",width=2)
        sh.pizf2.pack(fill=BOTH,expand=1)
        sh.scr.mainloop()
    def menulist(sh,x):
        sh.x=x
        sh.scr.destroy()
        sh.scr=Tk()
        sh.scr.title("Electronics arena")
        sh.scr.geometry("1366x768")
        #sh.scr.resizable(False, False)
        sh.menuf1=Frame(sh.scr,height=150,width=1366)
        sh.c=Canvas(sh.menuf1,height=150,width=1366)
        sh.c.pack()
        sh.logo=PhotoImage(file="logo.PNG")
        sh.c.create_image(683,75,image=sh.logo)
        sh.localtime=time.asctime(time.localtime(time.time()))
        sh.c.create_text(1000,50,text=sh.localtime,fill="Blue",font=("default",16))
        sh.menuf1.pack(fill=BOTH,expand=1)

        sh.menuf2=Frame(sh.scr,height=618,width=1366)
        sh.c=Canvas(sh.menuf2,height=618,width=1366)
        sh.c.pack()
        sh.logo1=PhotoImage(file="new1.png")
        sh.c.create_image(683,309,image=sh.logo1)
        sh.c.create_rectangle(50, 140, 1316, 420,fill="#d3ede6",outline="white",width=6)
        sh.veg=PhotoImage(file="new2.png")
        sh.c.create_image(230,250,image=sh.veg)
        sh.vegbut=Button(sh.menuf2,text="Phones",cursor="hand2",fg="white",command=lambda:sh.phones(sh.x),bg="#0b1335",bd=5,font=("default",18,'bold'))
        sh.vegbut.place(x=170,y=350)
        sh.nonveg=PhotoImage(file="new3.png")
        sh.c.create_image(530,250,image=sh.nonveg)
        sh.nonvegbut=Button(sh.menuf2,text="TVS",cursor="hand2",fg="white",command=lambda:sh.Tvs(sh.x),bg="#0b1335",bd=5,font=("default",18,'bold'))
        sh.nonvegbut.place(x=440,y=350)
        sh.chi=PhotoImage(file="evap.png")
        sh.c.create_image(830,250,image=sh.chi)
        sh.chibut=Button(sh.menuf2,text="SHome apppliances",cursor="hand2",fg="white",command=lambda:sh.Homeapplia(sh.x),bg="#0b1335",bd=5,font=("default",18,'bold'))
        sh.chibut.place(x=730,y=350)
        sh.side=PhotoImage(file="evap.png")
        sh.c.create_image(1130,250,image=sh.side)
        sh.sidebut=Button(sh.menuf2,text="Cookers",cursor="hand2",fg="white",command=lambda:sh.cookers(sh.x),bg="#0b1335",bd=5,font=("default",18,'bold'))
        sh.sidebut.place(x=1000,y=350)
        sh.menuf2.pack(fill=BOTH,expand=1)
        sh.scr.mainloop()
        #ORDERS
    def phones(sh,x):
        sh.x=x
        sh.scr.destroy()
        sh.scr=Tk()
        sh.scr.title("Electronics arena")
        sh.scr.geometry("1366x768")
        #sh.scr.resizable(False, False)
        sh.vegf1=Frame(sh.scr,height=150,width=1366)
        sh.c=Canvas(sh.vegf1,height=150,width=1366)
        sh.c.pack()
        sh.logo=PhotoImage(file="logo.PNG")
        sh.c.create_image(683,75,image=sh.logo)
        sh.localtime=time.asctime(time.localtime(time.time()))
        sh.c.create_text(1000,50,text=sh.localtime,fill="blue",font=("default",16))
        sh.vegf1.pack(fill=BOTH,expand=1)

        sh.phonesf2=Frame(sh.scr,height=618,width=1366)
        
        sh.c=Canvas(sh.phonesf2,height=618,width=1366)
        sh.c.pack()
        sh.log=Label(sh.phonesf2,text="PHONES ",bg="#9db1f2",font=("Cooper Black",22))
        sh.log.place(x=600,y=4)
        sh.c.create_rectangle(400, 40, 966, 540,fill="#d3ede6",outline="white",width=6)
        sh.q1=StringVar()
        sh.q2=StringVar()
        sh.q3=StringVar()
        sh.q4=StringVar()
        sh.q1.set("0")
        sh.q2.set("0")
        sh.q3.set("0")
        sh.q4.set("0")
        # phone 1
        sh.c.create_rectangle(405, 50, 960, 170,width=2)
        
        sh.c.create_text(650,80,text="Samsung",fill="#000000",font=("Cooper Black",20))
        sh.c.create_text(860,80,text="$450/$650/$250",fill="#ff3838",font=("default",17,'bold'))
        #ch1=sh.check(sh.phone2,100)
        sh.v1=IntVar()
        sh.C11=Radiobutton(sh.phonesf2,text = "Medium",value=10,variable=sh.v1)
        sh.C11.place(x=550,y=100)
        sh.C12 = Radiobutton(sh.phonesf2, text = "Large",value = 20, variable =sh.v1)
        sh.C12.place(x=650,y=100)
        sh.C13 = Radiobutton(sh.phonesf2, text = "Regular",value = 30, variable =sh.v1)
        sh.C13.place(x=750,y=100)
        sh.C11.select()
        sh.C11.deselect()    
        sh.C11.invoke()
        sh.c.create_text(590,150,text="Quantity : ",fill="#000000",font=("default",12))
        sh.qty1=Entry(sh.phonesf2,textvariable=sh.q1,bg="#aae2d7",font=("default",12),width=4,)
        sh.qty1.place(x=650,y=140)
        sh.add1=Button(sh.phonesf2,text="ADD",command=lambda:addch1(),bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'))
        sh.add1.place(x=850,y=120)
        def addch1():
            if sh.v1.get()==10:
                ch1="Medium"
                pric1=450
            elif sh.v1.get()==20:
                ch1="Large"
                pric1=650
            else:
                ch1="Regular"
                pric1=250
            sh.addlist(["Samsung",ch1,sh.q1.get(),pric1*int(sh.q1.get())])
            
        #pizza 2
        sh.c.create_rectangle(405, 170, 960, 290,width=2)
        sh.c.create_text(650,200,text="Iphone",fill="#000000",font=("Cooper Black",20))
        sh.c.create_text(860,200,text="$400/$600/$250",fill="#ff3838",font=("default",17,'bold'))
##        ch2=sh.check(sh.phonesf2,220)
        sh.v2=IntVar()
        sh.C21=Radiobutton(sh.phonesf2,text = "Medium",value=10,variable=sh.v2)
        sh.C21.place(x=550,y=220)
        sh.C22 = Radiobutton(sh.phonesf2, text = "Large",value = 20, variable =sh.v2)
        sh.C22.place(x=650,y=220)
        sh.C23 = Radiobutton(sh.phonesf2, text = "Regular",value = 30, variable =sh.v2)
        sh.C23.place(x=750,y=220)
        sh.C21.select()
        sh.C21.deselect()    
        sh.C21.invoke()
        sh.c.create_text(590,270,text="Quantity : ",fill="#000000",font=("default",12))
        sh.qty2=Entry(sh.phonesf2,textvariable=sh.q2,bg="#aae2d7",font=("default",12),width=4,)
        sh.qty2.place(x=650,y=260)
        sh.add2=Button(sh.phonesf2,text="ADD",command=lambda:addch2(),bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'))
        sh.add2.place(x=850,y=240)
        def addch2():
            if sh.v2.get()==10:
                ch2="Medium"
                pric2=400
            elif sh.v2.get()==20:
                ch2="Large"
                pric2=600
            else:
                ch2="Regular"
                pric2=250

            sh.addlist(["Iphone",ch2,sh.q2.get(),pric2*int(sh.q2.get())])
        #Phone 3
        sh.c.create_rectangle(405, 290, 960, 410,width=2)
        
        sh.c.create_text(650,320,text="Nokia",fill="#000000",font=("Cooper Black",20))
        sh.c.create_text(860,320,text="$385/$550/$225",fill="#ff3838",font=("default",17,'bold'))
        #ch3=sh.check(sh.phonesf2,340)
        sh.v3=IntVar()
        sh.C31=Radiobutton(sh.phonesf2,text = "Medium",value=10,variable=sh.v3)
        sh.C31.place(x=550,y=340)
        sh.C32 = Radiobutton(sh.phonesf2, text = "Large",value = 20, variable =sh.v3)
        sh.C32.place(x=650,y=340)
        sh.C33 = Radiobutton(sh.phonesf2, text = "Regular",value = 30, variable =sh.v3)
        sh.C33.place(x=750,y=340)
        sh.C31.select()
        sh.C31.deselect()    
        sh.C31.invoke()

        sh.c.create_text(590,390,text="Quantity : ",fill="#000000",font=("default",12))
        sh.qty3=Entry(sh.phonesf2,textvariable=sh.q3,bg="#aae2d7",font=("default",12),width=4,)
        sh.qty3.place(x=650,y=380)

        sh.add3=Button(sh.phonesf2,text="ADD",command=lambda:addch3(),bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'))
        sh.add3.place(x=850,y=360)
        def addch3():
            if sh.v3.get()==10:
                ch3="Medium"
                pric3=385
            elif sh.v3.get()==20:
                ch3="Large"
                pric3=550
            else:
                ch3="Regular"
                pric3=225
            sh.addlist(["Nokia    ",ch3,sh.q3.get(),pric3*int(sh.q3.get())])
            
        #phone 4
        sh.c.create_rectangle(405, 410, 960, 530,width=2)
    
        sh.c.create_text(650,440,text="INFINIX",fill="#000000",font=("Cooper Black",20))
        sh.c.create_text(860,440,text="$195/$385/$99",fill="#ff3838",font=("default",17,'bold'))
        #ch4=sh.check(sh.phonesf2,460)
        sh.v4=IntVar()
        sh.C41=Radiobutton(sh.phonesf2,text = "Medium",value=10,variable=sh.v4)
        sh.C41.place(x=550,y=460)
        sh.C42 = Radiobutton(sh.phonesf2, text = "Large",value = 20, variable =sh.v4)
        sh.C42.place(x=650,y=460)
        sh.C43 = Radiobutton(sh.phonesf2, text = "Regular",value = 30, variable =sh.v4)
        sh.C43.place(x=750,y=460)
        sh.C41.select()
        sh.C41.deselect()    
        sh.C41.invoke()
        
        sh.c.create_text(590,500,text="Quantity : ",fill="#000000",font=("default",12))
        sh.qty4=Entry(sh.phonesf2,textvariable=sh.q4,bg="#aae2d7",font=("default",12),width=4,)
        sh.qty4.place(x=650,y=500)
        
        sh.add4=Button(sh.phonesf2,text="ADD",command=lambda:addch4(),bg="#0b1335",cursor="hand2",fg="white",bd=4,font=("default",12,'bold'))
        sh.add4.place(x=850,y=480)
        def addch4():
            if sh.v4.get()==10:
                ch4="Medium"
                pric4=195
            elif sh.v4.get()==20:
                ch4="Large"
                pric4=385
            else:
                ch4="Regular"
                pric4=99
            sh.addlist(["INFINIX  ",ch4,sh.q4.get(),pric4*int(sh.q4.get())])
        sh.more=Button(sh.phonesf2,text="SHOW IMAGES",command=lambda:sh.download(),bg="#0b1335",cursor="hand2",fg="white",bd=5,font=("default",18,'bold'))
        sh.more.place(x=1050,y=150)

        sh.con=Button(sh.phonesf2,text="Confirm Order",command=lambda:sh.Orderde(sh.x),bg="#0b1335",cursor="hand2",fg="white",bd=5,font=("default",18,'bold'))
        sh.con.place(x=1050,y=250)
        sh.more=Button(sh.phonesf2,text="Add More..",command=lambda:sh.menulist(sh.x),bg="#0b1335",cursor="hand2",fg="white",bd=5,font=("default",18,'bold'))
        sh.more.place(x=1050,y=350)
       
        sh.phonesf2.pack(fill=BOTH,expand=1)
        sh.scr.mainloop()
        #add to product list
    def addlist(sh,q):
        if q[-2]!="0" and q[-2].isdigit():
            sh.cartlist.append(q)
            sh.amount=sh.amount+q[-1]
            messagebox.showinfo("Cart","Item Successhully added")
        else:
            messagebox.showinfo("Cart","Enter Valid Quantity to add")
        print(sh.cartlist,sh.amount)
    def download(sh):
        cm = images.phone("NOKIA",
                          "Best phone",
                         "https://www.jumia.co.ke/nokia-c1-5.45-android-9-1gb-16gb-dual-sim-black-29166581.html")

        ae = images.phone("Samsung","Best phone",
                          "https://saruk.co.ke/products/category/samsung?utm_source=google&utm_medium=cpc&utm_campaign=In-Market%20Audience&gclid=CjwKCAjwk6P2B")

       

    # Store the phone objects in a list.
        phones = [cm, ae]

    # Open the phone website in the user's browser, featuring the phones above.
        fresh_phones.open_phones_page(phones)
    def Orderde(sh,x):
        sh.x=x
        sh.scr.destroy()
        sh.scr=Tk()
        sh.scr.title("Electronics arena")
        sh.scr.geometry("1366x768")
        #sh.scr.resizable(False, False)
        sh.ordf1=Frame(sh.scr,height=150,width=1366)
        sh.c=Canvas(sh.ordf1,height=150,width=1366)
        sh.c.pack()
        sh.logo=PhotoImage(file="logo.PNG")
        sh.c.create_image(683,75,image=sh.logo)
       
        sh.localtime=time.asctime(time.localtime(time.time()))
        sh.c.create_text(1000,50,text=sh.localtime,fill="blue",font=("default",16))
        sh.ordf1.pack(fill=BOTH,expand=1)
        
        sh.ordf2=Frame(sh.scr,height=618,width=1366)
        sh.c=Canvas(sh.ordf2,height=618,width=1366)
        sh.c.pack()
        sh.log=Label(sh.ordf2,text="YOUR ORDER",bg="#9db1f2",font=("Cooper Black",22))
        sh.log.place(x=450,y=4)
        sh.c.create_rectangle(250, 50, 800, 500,fill="#d3ede6",outline="white",width=6)
        sh.amt=sh.amount
        sh.text="Total : "+str(sh.amt)
        sh.tot=Label(sh.ordf2,text=sh.text,bg="#f2da9d",width=12,font=("Cooper Black",22))
        sh.tot.place(x=900,y=250)
        sh.pay=Button(sh.ordf2,text="Pay",command=lambda:sh.y(sh.x),bg="#0b1335",cursor="hand2",fg="white",bd=5,font=("default",18,'bold'))
        sh.pay.place(x=900,y=300)
        sh.exi=Button(sh.ordf2,text="Add more",command=lambda:sh.menulist(sh.x),bg="#0b1335",cursor="hand2",fg="white",bd=5,font=("default",18,'bold'))
        sh.exi.place(x=1070,y=300)
        sh.c.create_text(525,80,text="Items\tSize\tQty\tPrice",font=("cooper black",18))
        sh.c.create_text(525,90,text="_______________________________________",font=("cooper black",18))
        y=100
        for i in sh.cartlist:
            y+=30
            s=i[0]+"\t"+i[1]+"\t"+i[2]+"\t"+str(i[3])
            sh.c.create_text(525,y,text=s,font=("default",16))
            
        sh.ordf2.pack(fill=BOTH,expand=1)
        sh.scr.mainloop()

if __name__ == '__main__':

        x=Electronics()
        x.main()