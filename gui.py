
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from database import connect_database

# -------------------- COLORS --------------------
BG = "#F3F6FB"
NAVY = "#172554"
BLUE = "#2563EB"
WHITE = "#FFFFFF"
TEXT = "#111827"
RED = "#B91C1C"


class AttendanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg=BG)

        self.setup_styles()
        self.build_dashboard()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=30,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=NAVY,
            foreground=WHITE,
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", BLUE)],
            foreground=[("selected", WHITE)]
        )

    # -------------------- DATABASE --------------------
    def db(self):
        conn = connect_database()

        if conn is None:
            raise RuntimeError(
                "Could not connect to MySQL. Make sure MySQL is running "
                "and database.py has the correct login details."
            )

        return conn

    def show_db_error(self, title, error, parent):
        messagebox.showerror(title, str(error), parent=parent)

    # -------------------- COMMON WINDOW --------------------
    def make_window(self, title, geometry="900x560"):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry(geometry)
        win.minsize(650, 430)
        win.configure(bg=BG)
        win.transient(self.root)

        header = tk.Frame(win, bg=NAVY, height=68)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=title.upper(),
            bg=NAVY,
            fg=WHITE,
            font=("Arial", 18, "bold")
        ).pack(expand=True)

        return win

    def make_button(self, parent, text, command, color=BLUE):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            bg=color,
            fg=WHITE,
            activebackground=NAVY,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=10,
            width=25
        )

    # -------------------- DASHBOARD --------------------
    def build_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        header = tk.Frame(self.root, bg=NAVY, height=125)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="ATTENDANCE MANAGEMENT SYSTEM",
            bg=NAVY,
            fg=WHITE,
            font=("Arial", 24, "bold")
        ).pack(expand=True)

        tk.Label(
            self.root,
            text="Manage students and attendance records",
            bg=BG,
            fg=TEXT,
            font=("Arial", 14)
        ).pack(pady=(25, 15))

        button_frame = tk.Frame(self.root, bg=BG)
        button_frame.pack(expand=True)

        actions = [
            ("Add Student", self.add_student_window, BLUE),
            ("View Students", self.view_students_window, BLUE),
            ("Mark Attendance", self.mark_attendance_window, BLUE),
            ("View Attendance", self.view_attendance_window, BLUE),
            ("Attendance Report", self.attendance_report_window, BLUE),
            ("Exit", self.root.destroy, RED)
        ]

        for label, action, color in actions:
            self.make_button(
                button_frame, label, action, color
            ).pack(pady=7)

        tk.Label(
            self.root,
            text="Python + MySQL Attendance Management System",
            bg=NAVY,
            fg=WHITE,
            font=("Arial", 9)
        ).pack(side="bottom", fill="x", ipady=8)

    # -------------------- ADD STUDENT --------------------
    def add_student_window(self):
        win = self.make_window("Add Student", "620x590")

        form = tk.Frame(
            win,
            bg=WHITE,
            padx=35,
            pady=25
        )
        form.pack(fill="both", expand=True, padx=25, pady=25)

        fields = [
            ("Register Number", "reg_no"),
            ("Student Name", "name"),
            ("Department", "department"),
            ("Year", "year"),
            ("Section", "section")
        ]

        entries = {}

        for row, (label_text, key) in enumerate(fields):
            tk.Label(
                form,
                text=label_text,
                bg=WHITE,
                fg=TEXT,
                font=("Arial", 12, "bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(0, 18),
                pady=12
            )

            entry = tk.Entry(
                form,
                font=("Arial", 12),
                bg="#F8FAFC",
                fg=TEXT,
                insertbackground=TEXT,
                relief="solid",
                bd=1
            )

            entry.grid(
                row=row,
                column=1,
                sticky="ew",
                pady=12,
                ipady=7
            )

            entries[key] = entry

        form.grid_columnconfigure(1, weight=1)

        def save_student():
            values = {
                key: field.get().strip()
                for key, field in entries.items()
            }

            if not all(values.values()):
                messagebox.showwarning(
                    "Missing information",
                    "Please fill in all five fields.",
                    parent=win
                )
                return

            try:
                year_value = int(values["year"])

                if year_value < 1:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Invalid year",
                    "Year must be a positive whole number.",
                    parent=win
                )
                return

            conn = None
            cursor = None

            try:
                conn = self.db()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO students
                    (reg_no, name, department, year, section)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        values["reg_no"],
                        values["name"],
                        values["department"],
                        year_value,
                        values["section"]
                    )
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Student added successfully!",
                    parent=win
                )

                win.destroy()

            except Exception as exc:
                if conn:
                    conn.rollback()

                self.show_db_error(
                    "Could not add student", exc, win
                )

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        self.make_button(
            form, "SAVE STUDENT", save_student
        ).grid(
            row=len(fields),
            column=0,
            columnspan=2,
            pady=(25, 5)
        )

        entries["reg_no"].focus_set()

    # -------------------- TABLE DISPLAY --------------------
    def show_table(
        self,
        title,
        columns,
        headings,
        query,
        params=None,
        geometry="950x560"
    ):
        win = self.make_window(title, geometry)

        area = tk.Frame(
            win,
            bg=BG,
            padx=18,
            pady=18
        )
        area.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            area,
            columns=columns,
            show="headings"
        )

        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(
                col,
                width=140,
                minwidth=90,
                anchor="center"
            )

        yscroll = ttk.Scrollbar(
            area,
            orient="vertical",
            command=tree.yview
        )

        xscroll = ttk.Scrollbar(
            area,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=yscroll.set,
            xscrollcommand=xscroll.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        area.grid_rowconfigure(0, weight=1)
        area.grid_columnconfigure(0, weight=1)

        conn = None
        cursor = None

        try:
            conn = self.db()
            cursor = conn.cursor()

            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            records = cursor.fetchall()

            for record in records:
                tree.insert("", "end", values=record)

            if not records:
                tk.Label(
                    area,
                    text="No records found.",
                    bg=BG,
                    fg=TEXT,
                    font=("Arial", 12)
                ).grid(row=2, column=0, pady=12)

        except Exception as exc:
            self.show_db_error(
                "Could not load records", exc, win
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return win, tree

    # -------------------- VIEW STUDENTS --------------------
    def view_students_window(self):
        self.show_table(
            "View Students",
            (
                "student_id",
                "reg_no",
                "name",
                "department",
                "year",
                "section"
            ),
            (
                "Student ID",
                "Register No.",
                "Name",
                "Department",
                "Year",
                "Section"
            ),
            """
            SELECT student_id, reg_no, name,
                   department, year, section
            FROM students
            ORDER BY student_id
            """
        )

    # -------------------- MARK ATTENDANCE --------------------
    def mark_attendance_window(self):
        win = self.make_window(
            "Mark Attendance", "650x520"
        )

        form = tk.Frame(
            win,
            bg=WHITE,
            padx=35,
            pady=30
        )
        form.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            form,
            text="Select Student",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 12, "bold")
        ).grid(
            row=0, column=0, sticky="w",
            padx=(0, 15), pady=16
        )

        student_var = tk.StringVar()

        student_box = ttk.Combobox(
            form,
            textvariable=student_var,
            state="readonly",
            font=("Arial", 12),
            width=32
        )
        student_box.grid(
            row=0, column=1, sticky="ew", pady=16, ipady=5
        )

        tk.Label(
            form,
            text="Date (YYYY-MM-DD)",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 12, "bold")
        ).grid(
            row=1, column=0, sticky="w",
            padx=(0, 15), pady=16
        )

        date_entry = tk.Entry(
            form,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )
        date_entry.grid(
            row=1, column=1, sticky="ew", pady=16, ipady=7
        )
        date_entry.insert(0, date.today().isoformat())

        tk.Label(
            form,
            text="Status",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 12, "bold")
        ).grid(
            row=2, column=0, sticky="w",
            padx=(0, 15), pady=16
        )

        status_var = tk.StringVar(value="Present")

        status_box = ttk.Combobox(
            form,
            textvariable=status_var,
            values=("Present", "Absent"),
            state="readonly",
            font=("Arial", 12)
        )
        status_box.grid(
            row=2, column=1, sticky="ew", pady=16, ipady=5
        )

        form.grid_columnconfigure(1, weight=1)

        conn = None
        cursor = None
        student_map = {}

        try:
            conn = self.db()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT student_id, reg_no, name
                FROM students
                ORDER BY reg_no
                """
            )

            for student_id, reg_no, name in cursor.fetchall():
                display = f"{student_id} | {reg_no} | {name}"
                student_map[display] = student_id

            student_box["values"] = list(student_map.keys())

            if student_map:
                student_box.current(0)
            else:
                messagebox.showwarning(
                    "No students",
                    "Add a student before marking attendance.",
                    parent=win
                )

        except Exception as exc:
            self.show_db_error(
                "Could not load students", exc, win
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        def save_attendance():
            selected = student_var.get()

            if not selected:
                messagebox.showwarning(
                    "Select student",
                    "Please select a student.",
                    parent=win
                )
                return

            try:
                selected_date = date.fromisoformat(
                    date_entry.get().strip()
                )
            except ValueError:
                messagebox.showerror(
                    "Invalid date",
                    "Enter the date in YYYY-MM-DD format.",
                    parent=win
                )
                return

            conn = None
            cursor = None

            try:
                conn = self.db()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO attendance
                    (student_id, attendance_date, status)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        student_map[selected],
                        selected_date,
                        status_var.get()
                    )
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Attendance marked successfully!",
                    parent=win
                )

                win.destroy()

            except Exception as exc:
                if conn:
                    conn.rollback()

                self.show_db_error(
                    "Could not mark attendance", exc, win
                )

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        self.make_button(
            form, "SAVE ATTENDANCE", save_attendance
        ).grid(
            row=3, column=0, columnspan=2, pady=28
        )

    # -------------------- VIEW ATTENDANCE --------------------
    def view_attendance_window(self):
        self.show_table(
            "View Attendance",
            (
                "attendance_id",
                "reg_no",
                "name",
                "attendance_date",
                "status"
            ),
            (
                "Attendance ID",
                "Register No.",
                "Student Name",
                "Date",
                "Status"
            ),
            """
            SELECT a.attendance_id, s.reg_no, s.name,
                   a.attendance_date, a.status
            FROM attendance a
            INNER JOIN students s
                ON a.student_id = s.student_id
            ORDER BY a.attendance_date DESC, s.reg_no
            """,
            geometry="1000x580"
        )

    # -------------------- ATTENDANCE REPORT --------------------
    def attendance_report_window(self):
        self.show_table(
            "Attendance Report",
            (
                "reg_no",
                "name",
                "total",
                "present",
                "absent",
                "percentage"
            ),
            (
                "Register No.",
                "Student Name",
                "Total Classes",
                "Present",
                "Absent",
                "Attendance %"
            ),
            """
            SELECT
                s.reg_no,
                s.name,
                COUNT(a.attendance_id) AS total_classes,
                COALESCE(
                    SUM(
                        CASE
                            WHEN a.status = 'Present'
                            THEN 1 ELSE 0
                        END
                    ), 0
                ) AS present_days,
                COALESCE(
                    SUM(
                        CASE
                            WHEN a.status = 'Absent'
                            THEN 1 ELSE 0
                        END
                    ), 0
                ) AS absent_days,
                ROUND(
                    CASE
                        WHEN COUNT(a.attendance_id) = 0 THEN 0
                        ELSE
                            SUM(
                                CASE
                                    WHEN a.status = 'Present'
                                    THEN 1 ELSE 0
                                END
                            ) * 100.0 / COUNT(a.attendance_id)
                    END,
                    2
                ) AS attendance_percentage
            FROM students s
            LEFT JOIN attendance a
                ON s.student_id = a.student_id
            GROUP BY
                s.student_id,
                s.reg_no,
                s.name
            ORDER BY s.reg_no
            """,
            geometry="1000x580"
        )


# -------------------- RUN APPLICATION --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceGUI(root)
    root.mainloop()
