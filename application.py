
import tkinter as tk
from tkinter import ttk
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

# URL API
API_BASE_URL = "https://developer-store.onrender.com/api/saled_products/"  # URL API خود را وارد کنید

def show_report():
    try:
        # Response to  API
        response = requests.get(API_BASE_URL)
        response.raise_for_status() 

    
        report_data = response.json()

       
        json_data = json.dumps(report_data, indent=4, ensure_ascii=False)  
        json_text.delete(1.0, tk.END)  
        json_text.insert(tk.END, json_data)  

        
        df = pd.DataFrame(report_data)

       
        if 'product' not in df.columns or 'amount' not in df.columns:
            status_label.config(text="خطا: ستون‌های مورد نیاز 'product' یا 'amount' یافت نشد.")
            return

       
        product_totals = df.groupby("product")["amount"].sum()

       
        fig, ax = plt.subplots(figsize=(5, 4))
        product_totals.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("گزارش فروش")
        ax.set_ylabel("مبلغ فروش")
        ax.set_xlabel("محصولات")

        
        for widget in report_frame.winfo_children():
            widget.destroy()

        
        canvas = FigureCanvasTkAgg(fig, master=report_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

       
        total_revenue = product_totals.sum()
        report_label.config(text=f"فروش کل: {total_revenue} افغانی")
    
    except requests.exceptions.RequestException as e:
      
        status_label.config(text=f"خطا در دریافت داده‌ها: {str(e)}")

root = tk.Tk()
root.title("Smart Management System")
root.geometry("700x300")
root.resizable(False, False)


notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

report_tab = ttk.Frame(notebook)
notebook.add(report_tab, text="Report Sale")


report_frame = tk.Frame(report_tab)
report_frame.pack(fill="both", expand=True, padx=10, pady=10)


report_label = tk.Label(report_tab, text="")
report_label.pack(pady=5)


fetch_report_button = tk.Button(report_tab, text="Show Report", command=show_report)
fetch_report_button.pack(pady=10)

 
json_frame = tk.Frame(report_tab)
json_frame.pack(fill="both", expand=True, padx=10, pady=10)


scrollbar = tk.Scrollbar(json_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


json_text = tk.Text(json_frame, wrap=tk.WORD, width=80, height=15, yscrollcommand=scrollbar.set)
json_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=json_text.yview)


status_label = tk.Label(root, text="")
status_label.pack(side="bottom", pady=5)

root.mainloop()
