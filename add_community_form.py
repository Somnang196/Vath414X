import tkinter as tk
from tkinter import messagebox
import json

FILE_PATH = r"C:\Users\VATH\Desktop\Xmanagement\X\community_list.json"

def load_data():
    try:
        with open(FILE_PATH, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def add_entry():
    account = entry_account.get().strip()
    community = entry_community.get().strip()
    
    if not account or not community:
        messagebox.showwarning("Warning", "Please fill in both fields")
        return
    
    community_list = [c.strip() for c in community.split(',') if c.strip()]
    
    data = load_data()
    
    existing_entry = next((item for item in data if item["account"] == account), None)
    
    if existing_entry:
        existing_communities = existing_entry.get("community", [])
        for comm in community_list:
            if comm not in existing_communities:
                existing_communities.append(comm)
        existing_entry["community"] = existing_communities
        messagebox.showinfo("Success", f"Added {len(community_list)} community(ies) to '{account}'")
    else:
        new_entry = {"account": account, "community": community_list}
        data.append(new_entry)
        messagebox.showinfo("Success", f"Added new account '{account}'")
    
    save_data(data)
    entry_account.delete(0, tk.END)
    entry_community.delete(0, tk.END)
    entry_account.focus()

def clear_fields():
    entry_account.delete(0, tk.END)
    entry_community.delete(0, tk.END)
    entry_account.focus()

root = tk.Tk()
root.title("Add to Community List")
root.geometry("550x400")
root.resizable(False, False)

WINDOW_BG = "#1a1a2e"
CARD_BG = "#16213e"
ACCENT = "#0f3460"
HIGHLIGHT = "#e94560"
TEXT_WHITE = "#ffffff"
TEXT_GRAY = "#a0a0a0"
INPUT_BG = "#0f3460"

root.configure(bg=WINDOW_BG)

main_frame = tk.Frame(root, bg=CARD_BG, padx=40, pady=40)
main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

title_label = tk.Label(main_frame, text="Community List Manager", 
                       font=('Segoe UI', 22, 'bold'), bg=CARD_BG, fg=HIGHLIGHT)
title_label.pack(pady=(0, 5))

subtitle = tk.Label(main_frame, text="Add accounts & communities", 
                    font=('Segoe UI', 10), bg=CARD_BG, fg=TEXT_GRAY)
subtitle.pack(pady=(0, 25))

def create_labeled_entry(label_text, var):
    tk.Label(main_frame, text=label_text, font=('Segoe UI', 11, 'bold'), 
             bg=CARD_BG, fg=TEXT_WHITE).pack(anchor='w', pady=(10, 5))
    entry = tk.Entry(main_frame, textvariable=var, width=40, font=('Segoe UI', 11),
                     bg=INPUT_BG, fg=TEXT_WHITE, insertbackground='white',
                     bd=0, highlightthickness=2, highlightcolor=HIGHLIGHT,
                     highlightbackground=ACCENT)
    entry.pack(ipady=8)
    return entry

entry_account = tk.StringVar()
entry_community = tk.StringVar()

entry_account_widget = create_labeled_entry("Account", entry_account)
entry_community_widget = create_labeled_entry("Community (comma-separated)", entry_community)

btn_frame = tk.Frame(main_frame, bg=CARD_BG)
btn_frame.pack(pady=25)

def create_btn(text, cmd, color):
    return tk.Button(btn_frame, text=text, command=cmd,
                     font=('Segoe UI', 11, 'bold'), bg=color, fg=TEXT_WHITE,
                     bd=0, padx=25, pady=10, cursor="hand2", activebackground=ACCENT)

add_btn = create_btn("ADD ENTRY", add_entry, HIGHLIGHT)
add_btn.pack(side=tk.LEFT, padx=5)

clear_btn = create_btn("CLEAR", clear_fields, ACCENT)
clear_btn.pack(side=tk.LEFT, padx=5)

footer = tk.Label(main_frame, text="Accounts get auto-merged if they already exist", 
                  font=('Segoe UI', 8), bg=CARD_BG, fg=TEXT_GRAY)
footer.pack(pady=(15, 0))

entry_account_widget.focus()
root.mainloop()
