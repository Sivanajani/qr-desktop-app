import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR-Code Generator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="QR-Code Generator", font=("Arial", 18, "bold"), bg="#f0f0f0")
        title.pack(pady=20)

        self.input_text = tk.Entry(self.root, font=("Arial", 14), width=35)
        self.input_text.pack(pady=10)

        generate_btn = tk.Button(self.root, text="QR-Code erstellen", command=self.generate_qr, font=("Arial", 12))
        generate_btn.pack(pady=10)

        self.qr_canvas = tk.Label(self.root, bg="#f0f0f0")
        self.qr_canvas.pack(pady=20)

        save_btn = tk.Button(self.root, text="QR-Code speichern", command=self.save_qr, font=("Arial", 12))
        save_btn.pack(pady=10)

        choose_logo_btn = tk.Button(self.root, text="Logo auswählen", command=self.choose_logo, font=("Arial", 12))
        choose_logo_btn.pack(pady=5)


    def generate_qr(self):
        data = self.input_text.get()
        if not data:
            messagebox.showwarning("Fehler", "Bitte gib einen Link oder Text ein.")
            return
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # Höchste Fehlertoleranz
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Logo hinzufügen (wenn vorhanden)
        if hasattr(self, "logo_path"):
            logo = Image.open(self.logo_path)
            
            # Logo skalieren
            qr_width, qr_height = qr_img.size
            logo_size = int(qr_width / 4)  # z. B. 1/4 der Breite
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            
            # Logo ins Zentrum einfügen
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
            
        self.qr_pil_image = qr_img.resize((200, 200))
        self.qr_image = ImageTk.PhotoImage(self.qr_pil_image)
        self.qr_canvas.config(image=self.qr_image)

    def choose_logo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Bilder", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.logo_path = file_path
            messagebox.showinfo("Logo ausgewählt", f"Logo:\n{file_path}")



    def save_qr(self):
        if hasattr(self, 'qr_image'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Dateien", "*.png")])
            if file_path:
                data = self.input_text.get()
                qr = qrcode.make(data)
                qr.save(file_path)
                messagebox.showinfo("Erfolg", f"QR-Code gespeichert als:\n{file_path}")
        else:
            messagebox.showwarning("Hinweis", "Bitte zuerst einen QR-Code generieren.")
        if hasattr(self, 'qr_pil_image'):
            self.qr_pil_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = QRApp(root)
    root.mainloop()