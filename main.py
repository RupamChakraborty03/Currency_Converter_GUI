from tkinter import *
from google_currency import convert
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import Label
from google_currency import convert
import json
import time
import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt


root = Tk()
root.geometry("610x450")
root.title("Currency Convertor GUI Python")
root.iconbitmap("india.ico")
root.config(bg="lightgray")

with open("ind.txt") as f:
    lines = f.readlines()
alldata = {}   #Empty dictionary.
for line in lines:
    data = line.split("\t");
    alldata[data[1]] =  data[2]

def get_time():
	timeVar= time.strftime("%I : %M : %S %p")
	clock.config(text=timeVar)
	clock.after(200,get_time)

def converter_function():
    try:
        input1 = Combobox1.get()
        input2 = Combobox2.get()
        input_code = alldata[input1]    #Taking country code from input.
        output_code = alldata[input2]    #Taking country code from output.
        value = amount.get()
        get_yearly_rates(1, input_code, output_code, 365)
        fun = convert(input_code, output_code, value) #Passing the PARAMETERS of GOOGLE CURRENCY CONVERTER (Input1 Input2 Amount)
        finalval = json.loads(fun) #Final value is a dictionary
        result = finalval["amount"] #Taking the result / amount from the dictionary
        output1.set(result)

    except:
        show = messagebox.askretrycancel("A Problem Has Been Occured", "Please Check The Amount You Have Entered or your Internet Connection.")
def get_yearly_rates(amount,currency,converted_currency,amount_of_days):
    today_date = datetime.datetime.now()
    date_1year = (today_date-datetime.timedelta(days=1 * amount_of_days))
    url=f'https://api.exchangerate.host/timeseries'
    payload={'base':currency,'amount':amount,'start_date':date_1year.date(),'end_date':today_date.date()}
    response=requests.get(url,params=payload)
    data = response.json()
    currency_history={}
    rate_history_array=[]
    for item in data['rates']:
        current_date = item
        currency_rate = data['rates'][item][converted_currency]
        currency_history[current_date] = [currency_rate]
        rate_history_array.append(currency_rate)
    pd_data=pd.DataFrame(currency_history).transpose()
    pd_data.columns=['Rate']
    pd.set_option('display.max_rows',None)
    #print(pd_data)
    plt.plot(rate_history_array)
    plt.ylabel(f'{amount} {currency} to {converted_currency}')
    plt.xlabel('Days')
    plt.title(f'current rate for {amount} {currency} to {converted_currency} is {rate_history_array[-1]}')
    plt.show()

Title = Label(root, text="International Currency Converter ", fg="black", bg="lightgray", font=("Stencil", 20, "bold","underline"))
Title.place(x=28, y=8)

Lable1 = Label(root, text="Enter the Amount to Convert :- ", bg="lightgray", fg="midnightblue", font=("ubuntu", 15, "bold"))
Lable1.place(x=15, y=60)

amount = IntVar() #amount is the input value given by user.
feeder = Entry(root, width=24 ,text=amount, bg="LightCyan", fg="DarkSlateBlue", font=("ubuntu", 15, "bold"))
feeder.place(x=330, y=60)

Label2 = Label(root, text="Select the Input Currency", bg="lightgray", fg="darkgreen", font=("ubuntu", 12, "bold"))
Label2.place(x=200, y=110)

slider = StringVar()
Combobox1 = Combobox(root, width=30, textvariable=slider, state="readonly", font=("ubuntu", 10, "bold"))
Combobox1['values'] = [item for item in alldata.keys()] #Showing All data list
Combobox1.current(0)
Combobox1.place(x=200, y=150)

Label3 = Label(root, text="Select the Output Currency", bg="lightgray", fg="darkgreen", font=("ubuntu", 12, "bold"))
Label3.place(x=200, y=190)

foreground = StringVar()
Combobox2 = Combobox(root, width=30, textvariable=foreground, state="readonly", font=("ubuntu", 10, "bold"))
Combobox2['values'] = [item for item in alldata.keys()]
Combobox2.current(4)
Combobox2.place(x=200, y=230)
#convert button
Button1 = Button(root, bg="DarkSlateBlue", text="Convert", command=converter_function , fg="white", font=("ubuntu", 15, "bold"), relief=RAISED,\
                            cursor="hand2")
Button1.place(x=250, y=275)

Label4 = Label(root, text="Converted Amount Here :- ", bg="lightgray", fg="midnightblue", font=("ubuntu", 15, "bold"))
Label4.place(x=15, y=365)

output1 = IntVar()
Entry2 = Entry(root, textvariable=output1, fg="blue", state="readonly",width=27, font=("ubuntu", 15, "bold"))
Entry2.place(x=280, y=365)

footer = Label(root, text="Developed & Designed By @Group 52 \n All Rights reserved",bg="lightgray", fg="grey", font=("ubuntu", 10, "bold"))
footer.place(x=170, y=405)

clock=Label(root,font=("UniDreamLED",18),bg="lightgray",fg="black")
clock.pack()
get_time()
clock.place(x=240, y=325)

root.mainloop()