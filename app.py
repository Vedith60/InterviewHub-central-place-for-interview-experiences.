import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import traceback

from auth import register_user, login_user
from experiences import add_experience, fetch_experiences, search_experiences, get_experience_by_id


class InterviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interview Experience App")
        self.root.iconbitmap("logo.ico")
        self.user_id = None
        self.username = None
        self.show_home()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # --- Home ---
    def show_home(self):
        self.clear()
        self.root.geometry("600x360")
        tk.Label(self.root, text="Welcome", font=("Segoe UI", 18, "bold")).pack(pady=18)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="Register", width=18, command=self.show_register).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Login", width=18, command=self.show_login).grid(row=0, column=1, padx=10)

    # --- Register ---
    def show_register(self):
        self.clear()
        self.root.geometry("520x300")
        tk.Label(self.root, text="Register", font=("Segoe UI", 14, "bold")).pack(pady=10)

        frm = tk.Frame(self.root)
        frm.pack(pady=6)

        tk.Label(frm, text="Username").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        username_entry = tk.Entry(frm, width=28)
        username_entry.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(frm, text="Password").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        password_entry = tk.Entry(frm, show="*", width=28)
        password_entry.grid(row=1, column=1, padx=6, pady=6)

        def do_register():
            uname = username_entry.get().strip()
            pwd = password_entry.get().strip()
            if not uname or not pwd:
                messagebox.showwarning("Validation", "Username and password are required.")
                return
            ok, info = register_user(uname, pwd)
            if ok:
                self.user_id = info
                self.username = uname
                messagebox.showinfo("Registered", f"Welcome, {uname}!")
                self.show_menu()
            else:
                messagebox.showerror("Error", info)

        tk.Button(self.root, text="Register", width=18, command=do_register).pack(pady=8)
        tk.Button(self.root, text="Back", command=self.show_home).pack()

    # --- Login ---
    def show_login(self):
        self.clear()
        self.root.geometry("520x300")
        tk.Label(self.root, text="Login", font=("Segoe UI", 14, "bold")).pack(pady=10)

        frm = tk.Frame(self.root)
        frm.pack(pady=6)

        tk.Label(frm, text="Username").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        username_entry = tk.Entry(frm, width=28)
        username_entry.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(frm, text="Password").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        password_entry = tk.Entry(frm, show="*", width=28)
        password_entry.grid(row=1, column=1, padx=6, pady=6)

        def do_login():
            uname = username_entry.get().strip()
            pwd = password_entry.get().strip()
            if not uname or not pwd:
                messagebox.showwarning("Validation", "Username and password are required.")
                return
            ok, user_id = login_user(uname, pwd)
            if ok:
                self.user_id = user_id
                self.username = uname
                messagebox.showinfo("Welcome", f"Logged in as {uname}")
                self.show_menu()
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        tk.Button(self.root, text="Login", width=18, command=do_login).pack(pady=8)
        tk.Button(self.root, text="Back", command=self.show_home).pack()

    # --- Menu ---
    def show_menu(self):
        self.clear()
        self.root.geometry("700x420")
        tk.Label(self.root, text=f"Hello, {self.username}", font=("Segoe UI", 14, "bold")).pack(pady=12)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=6)

        tk.Button(btn_frame, text="➕ Add Experience", width=20, command=self.show_add_experience).grid(row=0, column=0, padx=8, pady=8)
        tk.Button(btn_frame, text="📖 See All Experiences", width=20, command=self.show_experiences).grid(row=0, column=1, padx=8, pady=8)
        tk.Button(btn_frame, text="🔍 Search Experiences", width=20, command=self.show_search).grid(row=0, column=2, padx=8, pady=8)
        tk.Button(self.root, text="🚪 Logout", width=14, command=self.logout).pack(pady=12)

    def logout(self):
        self.user_id = None
        self.username = None
        self.show_home()

    # --- Add Experience ---
    def show_add_experience(self):
        self.clear()
        self.root.geometry("700x520")
        tk.Label(self.root, text="Add Experience", font=("Segoe UI", 14, "bold")).pack(pady=10)

        frm = tk.Frame(self.root)
        frm.pack(pady=6)

        tk.Label(frm, text="Company").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        company_entry = tk.Entry(frm, width=45)
        company_entry.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(frm, text="Role (optional)").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        role_entry = tk.Entry(frm, width=45)
        role_entry.grid(row=1, column=1, padx=6, pady=6)

        # Experience text
        tk.Label(self.root, text="Your experience (brief)").pack(anchor="w", padx=12)
        exp_text = ScrolledText(self.root, width=80, height=10)
        exp_text.pack(padx=12, pady=6)

        # Difficulty
        tk.Label(self.root, text="Difficulty").pack(anchor="w", padx=12, pady=(4, 0))
        difficulty_var = tk.StringVar()
        difficulty_combo = ttk.Combobox(
            self.root,
            textvariable=difficulty_var,
            values=["Easy", "Medium", "Hard"],
            state="readonly",
            width=20
        )
        difficulty_combo.pack(padx=12, pady=6)
        difficulty_combo.current(0)

        def do_add():
            company = company_entry.get().strip()
            role = role_entry.get().strip()
            experience = exp_text.get("1.0", "end").strip()
            difficulty = difficulty_var.get()
            if not company or not experience:
                messagebox.showwarning("Validation", "Company and experience text are required.")
                return
            ok, err = add_experience(self.user_id, company, role, experience, difficulty)
            if ok:
                messagebox.showinfo("Success", "Experience added.")
                self.show_menu()
            else:
                messagebox.showerror("Error", f"Failed to add experience: {err}")

        tk.Button(self.root, text="Submit", width=16, command=do_add).pack(pady=8)
        tk.Button(self.root, text="Back", command=self.show_menu).pack()

    # --- See All Experiences ---
    def show_experiences(self, rows=None):
        self.clear()
        self.root.geometry("1000x520")
        tk.Label(self.root, text="All Experiences", font=("Segoe UI", 14, "bold")).pack(pady=8)

        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=8, pady=6)

        cols = ("ID", "User", "Company", "Role", "Summary", "Difficulty", "Date")
        tree = ttk.Treeview(container, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)

        tree.column("ID", width=60)
        tree.column("User", width=120)
        tree.column("Company", width=150)
        tree.column("Role", width=120)
        tree.column("Summary", width=250)
        tree.column("Difficulty", width=100)
        tree.column("Date", width=140)

        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, side="left")

        if rows is None:
            rows = fetch_experiences()

        for r in rows:
            truncated = (r[4][:80] + "...") if len(r[4]) > 80 else r[4]
            tree.insert("", "end", values=(r[0], r[1], r[2], r[3], truncated, r[5], r[6]))

     
        def on_double(event):
            sel = tree.selection()
            if not sel:
                return
            item = tree.item(sel[0])["values"]
            exp_id = item[0]
            detail = get_experience_by_id(exp_id)
            if detail:
                _id, user, company, role, summary, difficulty, date_posted = detail
                dlg = tk.Toplevel(self.root)
                dlg.title(f"{company} — {role or 'Role'}")
                dlg.geometry("700x500")
                text = ScrolledText(dlg, width=90, height=30)
                text.pack(padx=8, pady=8, fill="both", expand=True)
                text.insert("end", f"Company: {company}\n")
                text.insert("end", f"Role: {role}\n")
                text.insert("end", f"Shared by: {user} on {date_posted}\n\n")
                text.insert("end", f"Difficulty: {difficulty}\n\n")
                text.insert("end", "Experience:\n")
                text.insert("end", f"{summary}\n\n")
                text.config(state="disabled")
            else:
                messagebox.showerror("Error", "Could not fetch details.")

        tree.bind("<Double-1>", on_double)
        tk.Button(self.root, text="Back", command=self.show_menu).pack(pady=6)

    # --- Search ---
    def show_search(self):
        self.clear()
        self.root.geometry("900x520")
        tk.Label(self.root, text="Search Experiences", font=("Segoe UI", 14, "bold")).pack(pady=8)
        frm = tk.Frame(self.root)
        frm.pack(pady=8)

        tk.Label(frm, text="Company or Role").grid(row=0, column=0, padx=6, pady=6)
        q_entry = tk.Entry(frm, width=40)
        q_entry.grid(row=0, column=1, padx=6, pady=6)

        result_frame = tk.Frame(self.root)
        result_frame.pack(fill="both", expand=True, padx=8, pady=6)

        def do_search():
            for w in result_frame.winfo_children():
                w.destroy()
            term = q_entry.get().strip()
            if not term:
                messagebox.showwarning("Validation", "Enter a company or role to search.")
                return
            rows = search_experiences(term)
            cols = ("ID", "User", "Company", "Role", "Summary", "Difficulty", "Date")
            tree = ttk.Treeview(result_frame, columns=cols, show="headings")
            for c in cols:
                tree.heading(c, text=c)

            tree.column("ID", width=50)
            tree.column("User", width=110)
            tree.column("Company", width=120)
            tree.column("Role", width=100)
            tree.column("Summary", width=250)
            tree.column("Difficulty", width=100)
            tree.column("Date", width=140)

            vsb = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=vsb.set)
            vsb.pack(side="right", fill="y")
            tree.pack(fill="both", expand=True, side="left")

            for r in rows:
                truncated = (r[4][:80] + "...") if len(r[4]) > 80 else r[4]
                tree.insert("", "end", values=(r[0], r[1], r[2], r[3], truncated, r[5], r[6]))

            def on_double_search(ev):
                sel = tree.selection()
                if not sel:
                    return
                item = tree.item(sel[0])["values"]
                exp_id = item[0]
                detail = get_experience_by_id(exp_id)
                if detail:
                    _id, user, company, role, summary, difficulty, date_posted = detail
                    dlg = tk.Toplevel(self.root)
                    dlg.title(f"{company} — {role or 'Role'}")
                    dlg.geometry("700x500")
                    text = ScrolledText(dlg, width=90, height=30)
                    text.pack(padx=8, pady=8, fill="both", expand=True)
                    text.insert("end", f"Company: {company}\n")
                    text.insert("end", f"Role: {role}\n")
                    text.insert("end", f"Shared by: {user} on {date_posted}\n\n")
                    text.insert("end", f"Difficulty: {difficulty}\n\n")
                    text.insert("end", "Experience:\n")
                    text.insert("end", f"{summary}\n\n")
                    text.config(state="disabled")
                else:
                    messagebox.showerror("Error", "Could not fetch details.")

            tree.bind("<Double-1>", on_double_search)

        tk.Button(self.root, text="Search", width=14, command=do_search).pack(pady=6)
        tk.Button(self.root, text="Back", command=self.show_menu).pack(pady=6)


# -------------------- Run --------------------
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = InterviewApp(root)
        root.mainloop()
    except Exception:
        traceback.print_exc()
        messagebox.showerror("Fatal", "An unexpected error occurred. Check console for details.")
