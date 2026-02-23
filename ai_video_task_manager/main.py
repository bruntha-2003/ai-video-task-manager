

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database        import init_db
from models          import (validate_user,
                              add_task, update_task, delete_task,
                              get_all_tasks, search_task,
                              add_stage, get_all_stages,
                              get_report)
from reminder_service import check_and_send_reminders


BG      = "#1e2a3a"
PANEL   = "#243447"
ACCENT  = "#2e86de"
WHITE   = "#ffffff"
LIGHT   = "#dfe6e9"
RED     = "#e74c3c"
GREEN   = "#2ecc71"
YELLOW  = "#f39c12"
GRAY    = "#636e72"

FONT    = ("Segoe UI", 11)
FONT_B  = ("Segoe UI", 11, "bold")
FONT_H  = ("Segoe UI", 15, "bold")


def make_btn(parent, text, cmd, color=ACCENT, fg=WHITE, width=12):
    return tk.Button(parent, text=text, command=cmd,
                     bg=color, fg=fg, font=FONT_B,
                     relief="flat", bd=0, padx=10, pady=6,
                     activebackground=color, activeforeground=fg,
                     cursor="hand2", width=width)

def make_label(parent, text, font=FONT, bg=PANEL, fg=LIGHT, anchor="w"):
    return tk.Label(parent, text=text, font=font,
                    bg=bg, fg=fg, anchor=anchor)

def make_entry(parent, textvariable=None, width=30, show=None):
    e = tk.Entry(parent, font=FONT,
                 bg="#2d3e50", fg=WHITE,
                 insertbackground=WHITE,
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=ACCENT,
                 highlightcolor=ACCENT,
                 width=width)
    if textvariable:
        e.config(textvariable=textvariable)
    if show:
        e.config(show=show)
    return e

def make_tree(parent, columns, col_widths):
    
    style = ttk.Style()
    style.configure("TV.Treeview",
                    background="#2d3e50",
                    foreground=WHITE,
                    fieldbackground="#2d3e50",
                    rowheight=26,
                    font=("Segoe UI", 10))
    style.configure("TV.Treeview.Heading",
                    background=ACCENT,
                    foreground=WHITE,
                    font=FONT_B,
                    relief="flat")
    style.map("TV.Treeview",
              background=[("selected", ACCENT)])

    tree = ttk.Treeview(parent, columns=columns,
                        show="headings", style="TV.Treeview")
    for col, w in zip(columns, col_widths):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    vsb = ttk.Scrollbar(parent, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set,
                   xscrollcommand=hsb.set)
    return tree, vsb, hsb


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("TrackBot — Login")
        self.root.geometry("420x500")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._center(420, 500)
        self._build_ui()

    def _center(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        
        tk.Label(self.root, text="  TrackBot",
                 font=("Segoe UI", 26, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=(50, 4))
        tk.Label(self.root,
                 text="AI Video Task Management System",
                 font=("Segoe UI", 10),
                 bg=BG, fg=GRAY).pack()

        
        card = tk.Frame(self.root, bg=PANEL, padx=40, pady=30)
        card.pack(padx=40, pady=30, fill="x")

        make_label(card, "Username", FONT_B).pack(anchor="w")
        self.v_user = tk.StringVar()
        make_entry(card, self.v_user, width=30).pack(fill="x", pady=(4, 14))

        make_label(card, "Password", FONT_B).pack(anchor="w")
        self.v_pass = tk.StringVar()
        make_entry(card, self.v_pass, width=30, show="*").pack(fill="x", pady=(4, 20))

        make_btn(card, "Sign In", self._login, width=30).pack(fill="x")

        tk.Label(self.root,
                 text="Default: admin / admin123",
                 font=("Segoe UI", 9),
                 bg=BG, fg=GRAY).pack()

    def _login(self):
        u = self.v_user.get().strip()
        p = self.v_pass.get().strip()
        if validate_user(u, p):
            self.root.destroy()
            root2 = tk.Tk()
            MainApp(root2, u)
            root2.mainloop()
        else:
            messagebox.showerror("Login Failed",
                                 "Invalid username or password!")



class MainApp:
    def __init__(self, root, username):
        self.root     = root
        self.username = username
        self.root.title(f"TrackBot — {username}")
        self.root.geometry("1100x700")
        self.root.configure(bg=BG)
        self._center(1100, 700)
        self._build_ui()

    def _center(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        
        bar = tk.Frame(self.root, bg=ACCENT, height=48)
        bar.pack(fill="x")
        tk.Label(bar,
                 text="  TrackBot — AI Video Task Management",
                 font=FONT_H, bg=ACCENT, fg=WHITE
                 ).pack(side="left", padx=20, pady=8)
        tk.Label(bar,
                 text=f"  {self.username}",
                 font=FONT_B, bg=ACCENT, fg=WHITE
                 ).pack(side="right", padx=20)

        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook",     background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL,
                        foreground=LIGHT, font=FONT_B,
                        padding=[18, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", WHITE)])
        style.configure("TFrame", background=PANEL)

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        t1 = ttk.Frame(nb)
        t2 = ttk.Frame(nb)
        t3 = ttk.Frame(nb)

        nb.add(t1, text="   Task Items  ")
        nb.add(t2, text="   Task Stage  ")
        nb.add(t3, text="   Report & Reminder ")

        TaskItemsTab(t1)
        TaskStageTab(t2)
        ReportTab(t3)


class TaskItemsTab:
    def __init__(self, parent):
        self.parent = parent
        self._init_vars()
        self._build_ui()
        self._refresh_grid()

    def _init_vars(self):
        self.v_id     = tk.StringVar()
        self.v_les    = tk.StringVar()
        self.v_asgn   = tk.StringVar()
        self.v_start  = tk.StringVar(value=str(date.today()))
        self.v_due    = tk.StringVar()
        self.v_status = tk.StringVar(value="Pending")

    def _build_ui(self):
        make_label(self.parent,
                   "  Task Items Management",
                   FONT_H, PANEL, ACCENT).pack(fill="x", pady=(10, 5))

        main = tk.Frame(self.parent, bg=PANEL)
        main.pack(fill="both", expand=True, padx=10, pady=5)

        form = tk.Frame(main, bg=PANEL, width=320)
        form.pack(side="left", fill="y", padx=(0, 10))
        form.pack_propagate(False)

        fields = [
            ("Task Item ID  (for Search / Update / Delete)", self.v_id),
            ("Lesson ID",                                    self.v_les),
            ("Assigned To",                                  self.v_asgn),
            ("Start Date  (YYYY-MM-DD)",                     self.v_start),
            ("Due Date    (YYYY-MM-DD)",                     self.v_due),
        ]
        for label, var in fields:
            make_label(form, label).pack(anchor="w", padx=10, pady=(8, 0))
            make_entry(form, var, width=34).pack(padx=10, fill="x")

        make_label(form, "Status").pack(anchor="w", padx=10, pady=(8, 0))
        ttk.Combobox(form,
                     textvariable=self.v_status,
                     values=["Pending", "In Progress", "Completed"],
                     state="readonly", font=FONT, width=32
                     ).pack(padx=10, fill="x")

       
        bf = tk.Frame(form, bg=PANEL)
        bf.pack(pady=16, padx=10, fill="x")
        make_btn(bf, " Add",     self._add,    GREEN,  WHITE, 11).grid(row=0, column=0, padx=3, pady=3)
        make_btn(bf, " Update",  self._update, YELLOW, WHITE, 11).grid(row=0, column=1, padx=3, pady=3)
        make_btn(bf, " Delete",  self._delete, RED,    WHITE, 11).grid(row=1, column=0, padx=3, pady=3)
        make_btn(bf, " Search",  self._search, ACCENT, WHITE, 11).grid(row=1, column=1, padx=3, pady=3)
        make_btn(bf, " Refresh", self._refresh_grid, GRAY, WHITE, 24).grid(
            row=2, column=0, columnspan=2, sticky="we", padx=3, pady=3)

        right = tk.Frame(main, bg=PANEL)
        right.pack(side="left", fill="both", expand=True)

        cols   = ["ID", "Lesson ID", "Assigned To",
                  "Start Date", "Due Date", "Status"]
        widths = [50,   120,         150, 110, 110, 110]
        self.tree, vsb, hsb = make_tree(right, cols, widths)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _add(self):
        les  = self.v_les.get().strip()
        asgn = self.v_asgn.get().strip()
        due  = self.v_due.get().strip()
        if not (les and asgn and due):
            messagebox.showwarning("Missing Fields",
                                   "Lesson ID, Assigned To & Due Date are required!")
            return
        add_task(les, asgn, self.v_start.get().strip(),
                 due, self.v_status.get())
        messagebox.showinfo("Success", "Task added successfully!")
        self._clear(); self._refresh_grid()

    def _update(self):
        tid = self.v_id.get().strip()
        if not tid:
            messagebox.showwarning("Required", "Enter Task Item ID to update!")
            return
        update_task(tid,
                    self.v_les.get(), self.v_asgn.get(),
                    self.v_start.get(), self.v_due.get(),
                    self.v_status.get())
        messagebox.showinfo("Updated", "Task updated successfully!")
        self._refresh_grid()

    def _delete(self):
        tid = self.v_id.get().strip()
        if not tid:
            messagebox.showwarning("Required", "Enter Task Item ID to delete!")
            return
        if messagebox.askyesno("Confirm Delete",
                               f"Delete Task ID {tid}?"):
            delete_task(tid)
            messagebox.showinfo("Deleted", "Task deleted!")
            self._clear(); self._refresh_grid()

    def _search(self):
        tid = self.v_id.get().strip()
        if not tid:
            messagebox.showwarning("Required", "Enter Task Item ID to search!")
            return
        row = search_task(tid)
        self.tree.delete(*self.tree.get_children())
        if row:
            self.tree.insert("", "end", values=tuple(row))
        else:
            messagebox.showinfo("Not Found", f"No task found with ID {tid}.")

    def _refresh_grid(self):
        self.tree.delete(*self.tree.get_children())
        for row in get_all_tasks():
            self.tree.insert("", "end", values=tuple(row))

    def _on_row_select(self, _event):
        sel = self.tree.selection()
        if sel:
            v = self.tree.item(sel[0])["values"]
            self.v_id.set(v[0]);    self.v_les.set(v[1])
            self.v_asgn.set(v[2]);  self.v_start.set(v[3])
            self.v_due.set(v[4]);   self.v_status.set(v[5])

    def _clear(self):
        self.v_id.set("");  self.v_les.set("");  self.v_asgn.set("")
        self.v_start.set(str(date.today()))
        self.v_due.set(""); self.v_status.set("Pending")


class TaskStageTab:
    def __init__(self, parent):
        self.parent = parent
        self._init_vars()
        self._build_ui()
        self._refresh_grid()

    def _init_vars(self):
        self.v_tid     = tk.StringVar()
        self.v_sname   = tk.StringVar()
        self.v_sstatus = tk.StringVar(value="Pending")
        self.v_date    = tk.StringVar(value=str(date.today()))
        self.v_status  = tk.StringVar(value="Active")

    def _build_ui(self):
        make_label(self.parent,
                   "  Task Stage Management",
                   FONT_H, PANEL, ACCENT).pack(fill="x", pady=(10, 5))

        main = tk.Frame(self.parent, bg=PANEL)
        main.pack(fill="both", expand=True, padx=10, pady=5)

        form = tk.Frame(main, bg=PANEL, width=320)
        form.pack(side="left", fill="y", padx=(0, 10))
        form.pack_propagate(False)

        make_label(form, "Task Item ID").pack(anchor="w", padx=10, pady=(8, 0))
        make_entry(form, self.v_tid, width=34).pack(padx=10, fill="x")

        make_label(form, "Stage Name").pack(anchor="w", padx=10, pady=(8, 0))
        ttk.Combobox(form,
                     textvariable=self.v_sname,
                     values=["AI Image Creation",
                             "Image Voice-over",
                             "Screen Recording",
                             "Screen Recording Voice-over",
                             "AI Audio Track",
                             "Video Editing"],
                     state="readonly", font=FONT, width=32
                     ).pack(padx=10, fill="x")

        make_label(form, "Stage Status").pack(anchor="w", padx=10, pady=(8, 0))
        ttk.Combobox(form,
                     textvariable=self.v_sstatus,
                     values=["Pending", "In Progress", "Completed"],
                     state="readonly", font=FONT, width=32
                     ).pack(padx=10, fill="x")

        make_label(form, "Last Updated Date  (YYYY-MM-DD)").pack(
            anchor="w", padx=10, pady=(8, 0))
        make_entry(form, self.v_date, width=34).pack(padx=10, fill="x")

        make_label(form, "Status").pack(anchor="w", padx=10, pady=(8, 0))
        ttk.Combobox(form,
                     textvariable=self.v_status,
                     values=["Active", "Inactive"],
                     state="readonly", font=FONT, width=32
                     ).pack(padx=10, fill="x")

        bf = tk.Frame(form, bg=PANEL)
        bf.pack(pady=16, padx=10, fill="x")
        make_btn(bf, " Submit",  self._submit,        GREEN, WHITE, 14).grid(
            row=0, column=0, padx=3, pady=3)
        make_btn(bf, " Refresh", self._refresh_grid, GRAY,  WHITE, 14).grid(
            row=0, column=1, padx=3, pady=3)

        
        right = tk.Frame(main, bg=PANEL)
        right.pack(side="left", fill="both", expand=True)

        cols   = ["Stage ID", "Task Item ID",
                  "Stage Status", "Last Updated", "Status"]
        widths = [80, 110, 130, 140, 90]
        self.tree, vsb, hsb = make_tree(right, cols, widths)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _submit(self):
        tid   = self.v_tid.get().strip()
        sname = self.v_sname.get().strip()
        if not (tid and sname):
            messagebox.showwarning("Missing Fields",
                                   "Task Item ID and Stage Name are required!")
            return
        add_stage(tid, sname, self.v_sstatus.get(),
                  self.v_date.get(), self.v_status.get())
        messagebox.showinfo("Saved", "Stage saved successfully!")
        self._clear(); self._refresh_grid()

    def _refresh_grid(self):
        self.tree.delete(*self.tree.get_children())
        for row in get_all_stages():
            self.tree.insert("", "end", values=tuple(row))

    def _on_row_select(self, _event):
        sel = self.tree.selection()
        if sel:
            v = self.tree.item(sel[0])["values"]
            self.v_tid.set(v[1]);     self.v_sstatus.set(v[2])
            self.v_date.set(v[3]);    self.v_status.set(v[4])

    def _clear(self):
        self.v_tid.set(""); self.v_sname.set("")
        self.v_sstatus.set("Pending")
        self.v_date.set(str(date.today()))
        self.v_status.set("Active")



class ReportTab:
    def __init__(self, parent):
        self.parent = parent
        self._build_ui()
        self._refresh_grid()

    def _build_ui(self):
        make_label(self.parent,
                   "  Task Report & Reminder System",
                   FONT_H, PANEL, ACCENT).pack(fill="x", pady=(10, 5))

        rf = tk.Frame(self.parent, bg=PANEL)
        rf.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        cols   = ["Stage ID", "Task Item ID",
                  "Due Date", "Last Updated", "Stage Status"]
        widths = [80, 110, 130, 140, 130]
        self.tree, vsb, _ = make_tree(rf, cols, widths)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        bf = tk.Frame(self.parent, bg=PANEL)
        bf.pack(fill="x", padx=10, pady=5)
        make_btn(bf, "Run Reminder Check",
                 self._run_reminder, RED,  WHITE, 25).pack(side="left", padx=5)
        make_btn(bf, " Refresh Report",
                 self._refresh_grid, GRAY, WHITE, 20).pack(side="left", padx=5)

        self.log = tk.Text(self.parent, height=10,
                           bg="#1a252f", fg=GREEN,
                           font=("Consolas", 10),
                           relief="flat", state="disabled", bd=0,
                           highlightthickness=1,
                           highlightbackground=ACCENT)
        self.log.pack(fill="x", padx=10, pady=(0, 10))
        self._write_log("System ready — click 'Run Reminder Check' to begin.\n")

    def _refresh_grid(self):
        self.tree.delete(*self.tree.get_children())
        for row in get_report():
            self.tree.insert("", "end", values=tuple(row))

    def _write_log(self, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg)
        self.log.see("end")
        self.log.config(state="disabled")

    def _run_reminder(self):
        check_and_send_reminders(log_callback=self._write_log)
        self._refresh_grid()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
