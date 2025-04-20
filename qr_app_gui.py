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

    def generate_qr(self):
        data = self.input_text.get()
        if not data:
            messagebox.showwarning("Fehler", "Bitte gib einen Link oder Text ein.")
            return

        qr = qrcode.make(data)
        qr = qr.resize((200, 200))

        self.qr_image = ImageTk.PhotoImage(qr)
        self.qr_canvas.config(image=self.qr_image)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = QRApp(root)
    root.mainloop()