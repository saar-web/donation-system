import csv
import os
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# הגדרת שם קובץ הנתונים והסיסמה למנהל
קובץ = "donors.csv"
סיסמת_מנהל = "1234"

# פונקציות חישוב
def חשב_יתרה(התחייבות, תרומה):
    יתרה = התחייבות - תרומה
    if יתרה > 0:
        return יתרה, "חובה"
    elif יתרה < 0:
        return abs(יתרה), "זכות"
    else:
        return 0, "אין יתרה"

def שמור_לקובץ(תורם):
    קיים = os.path.isfile(קובץ)
    with open(קובץ, mode='a', newline='', encoding='utf-8') as file:
        כותב = csv.DictWriter(file, fieldnames=["שם", "התחייבות", "תרם", "יתרה", "סטטוס"])
        if not קיים:
            כותב.writeheader()
        כותב.writerow(תורם)

def יצא_pdf(תורם):
    שם_קובץ = f"donor_{תורם['שם'].replace(' ', '_')}.pdf"
    c = canvas.Canvas(שם_קובץ, pagesize=A4)
    c.setFont("Helvetica", 14)

    c.drawString(100, 800, f"דו\"ח תורם: {תורם['שם']}")
    c.drawString(100, 770, f"התחייבות: ₪{תורם['התחייבות']}")
    c.drawString(100, 740, f"תרומה בפועל: ₪{תורם['תרם']}")
    c.drawString(100, 710, f"יתרה: ₪{תורם['יתרה']} ({תורם['סטטוס']})")

    if תורם['סטטוס'] == "חובה":
        c.drawString(100, 670, "פרטי תשלום:")
        c.drawString(120, 650, "בנק: 12 מזרחי")
        c.drawString(120, 630, "סניף: 345")
        c.drawString(120, 610, "חשבון: 123456789")
        c.drawString(120, 590, "על שם: עמותת חסד ישראל")

    c.save()
    messagebox.showinfo("הצלחה", f"\n✅ קובץ PDF נוצר: {שם_קובץ}\n")

# פונקציות הצגת פרטי תורם
def הצג_תורם(תורם):
    פרטי_תורם = f"""
    שם: {תורם['שם']}
    התחייבות: ₪{תורם['התחייבות']}
    תרם בפועל: ₪{תורם['תרם']}
    יתרה: ₪{תורם['יתרה']} ({תורם['סטטוס']})
    """
    if תורם['סטטוס'] == "חובה":
        פרטי_תורם += "\n⚠️ נשמח אם תשלים את התרומה.\nבנק: 12 מזרחי | סניף: 345 | חשבון: 123456789 | על שם: עמותת חסד ישראל"
    
    messagebox.showinfo("פרטי תורם", פרטי_תורם)

# חיפוש תורם
def חפש_תורם(שם_לחיפוש):
    נמצא = False
    if not os.path.isfile(קובץ):
        messagebox.showerror("שגיאה", "⚠️ אין עדיין נתונים.")
        return
    with open(קובץ, newline='', encoding='utf-8') as file:
        קורא = csv.DictReader(file)
        for שורה in קורא:
            if שורה["שם"] == שם_לחיפוש:
                תורם = {
                    "שם": שורה["שם"],
                    "התחייבות": float(שורה["התחייבות"]),
                    "תרם": float(שורה["תרם"]),
                    "יתרה": float(שורה["יתרה"]),
                    "סטטוס": שורה["סטטוס"]
                }
                הצג_תורם(תורם)
                נמצא = True
    if not נמצא:
        messagebox.showerror("שגיאה", f"❌ לא נמצא תורם בשם: {שם_לחיפוש}")

# הגדרת ממשק גרפי
class מערכת_תרומות:
    def __init__(self, root):
        self.root = root
        self.root.title("מערכת ניהול תרומות")
        self.root.geometry("400x400")
        self.root.config(bg="#f0f8ff")

        # כותרת ראשית
        self.header = Label(self.root, text="מערכת ניהול תרומות", font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#4B9CD3")
        self.header.pack(pady=20)

        # כפתורים
        self.manager_btn = Button(self.root, text="כניסת מנהל", width=25, height=2, command=self.כניסת_מנהל)
        self.manager_btn.pack(pady=10)

        self.donor_btn = Button(self.root, text="כניסת תורם", width=25, height=2, command=self.כניסת_תורם)
        self.donor_btn.pack(pady=10)

        self.exit_btn = Button(self.root, text="יציאה", width=25, height=2, command=self.root.quit)
        self.exit_btn.pack(pady=10)

    def כניסת_מנהל(self):
        סיסמה = askstring("סיסמה", "הכנס סיסמה למנהל:")
        if סיסמה != סיסמת_מנהל:
            messagebox.showerror("שגיאה", "❌ סיסמה שגויה!")
            return

        self.manager_screen()

    def כניסת_תורם(self):
        שם = askstring("חיפוש תורם", "הכנס שם לחיפוש:")
        חפש_תורם(שם)

    def manager_screen(self):
        self.clear_screen()
        
        self.header.config(text="מצב מנהל")

        # כפתורים למנהל
        self.add_btn = Button(self.root, text="הוסף תורם חדש", width=25, height=2, command=self.הוסף_תורם)
        self.add_btn.pack(pady=10)

        self.search_btn = Button(self.root, text="חפש תורם לפי שם", width=25, height=2, command=self.חפש_תורם_מנהל)
        self.search_btn.pack(pady=10)

        self.view_all_btn = Button(self.root, text="הצג את כל התורמים", width=25, height=2, command=self.הצג_את_כל_התורמים)
        self.view_all_btn.pack(pady=10)

        self.exit_btn = Button(self.root, text="חזור לתפריט ראשי", width=25, height=2, command=self.clear_screen)
        self.exit_btn.pack(pady=10)

    def הוסף_תורם(self):
        שם = askstring("הוסף תורם", "הכנס שם תורם:")
        התחייבות = float(askstring("הכנס התחייבות", "כמה התחייב לתרום?"))
        תרם = float(askstring("הכנס תרומה", "כמה תרם בפועל?"))
        יתרה, סטטוס = חשב_יתרה(התחייבות, תרם)

        תורם = {
            "שם": שם,
            "התחייבות": התחייבות,
            "תרם": תרם,
            "יתרה": יתרה,
            "סטטוס": סטטוס
        }

        שמור_לקובץ(תורם)
        messagebox.showinfo("הצלחה", f"התורם {שם} נוסף בהצלחה.")

    def חפש_תורם_מנהל(self):
        שם = askstring("חפש תורם", "הכנס שם לחיפוש:")
        חפש_תורם(שם)

    def הצג_את_כל_התורמים(self):
        if not os.path.isfile(קובץ):
            messagebox.showerror("שגיאה", "⚠️ אין עדיין נתונים.")
            return
        with open(קובץ, newline='', encoding='utf-8') as file:
            קורא = csv.DictReader(file)
            for שורה in קורא:
                תורם = {
                    "שם": שורה["שם"],
                    "התחייבות": float(שורה["התחייבות"]),
                    "תרם": float(שורה["תרם"]),
                    "יתרה": float(שורה["יתרה"]),
                    "סטטוס": שורה["סטטוס"]
                }
                הצג_תורם(תורם)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.__init__(self.root)

if __name__ == "__main__":
    root = Tk()
    app = מערכת_תרומות(root)
    root.mainloop()
