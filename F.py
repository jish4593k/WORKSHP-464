import io
import requests
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
from scipy.stats import mode
import torch
from pdfminer.high_level import extract_text

class ExtractText:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Text Extractor")

        self.text_display = tk.Text(self.master, wrap="word", height=20, width=60)
        self.text_display.pack(padx=10, pady=10)

        self.btn_open_file = tk.Button(self.master, text="Open PDF File", command=self.open_pdf_file)
        self.btn_open_file.pack(pady=10)

    def open_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            text_content = self.extract_text_from_pdf(file_path)
            self.display_text(text_content)

    def extract_text_from_pdf(self, file_path):
        
           
            response = requests.get(file_path)

           
            if response.status_code == 200:
                pdf_content = response.content
            else:
                return f"Failed to retrieve the PDF. Status code: {response.status_code}"

        else:
            # Read local PDF file
            with open(file_path, "rb") as file:
                pdf_content = file.read()

      
        tensor_pdf_content = torch.tensor(list(pdf_content), dtype=torch.uint8)

       s
        pdf_content_back = bytes(tensor_pdf_content.numpy().tobytes())

        
        assert pdf_content == pdf_content_back

  
        most_common_byte = mode(tensor_pdf_content).mode.item()
  
        tensor_pdf_content_mode = tensor_pdf_content.new_full(tensor_pdf_content.shape, most_common_byte)
        
        pdf_content_mode = bytes(tensor_pdf_content_mode.numpy().tobytes())

        assert pdf_content_mode == bytes([most_common_byte] * len(pdf_content))

        pdf_reader = PdfReader(io.BytesIO(pdf_content_mode))

        text_from_pdfminer = extract_text(io.BytesIO(pdf_content_mode))

        return text_from_pdfminer

    def display_text(self, text_content):
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, text_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExtractText(root)
    root.mainloop()
