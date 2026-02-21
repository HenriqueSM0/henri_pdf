import os, pypdf
from pathlib import Path
import tkinter as tk
from tkinter import scrolledtext, messagebox
from agno.models.groq import Groq
from agno.models.message import Message  
from dotenv import load_dotenv

load_dotenv()


model = Groq(id="llama-3.3-70b-versatile") # Model : Change if you want


pdfs_path = "pdfs"
all_files = os.listdir(pdfs_path)
pdf_files = [file for file in all_files if file.lower().endswith('.pdf')]
pdf_files.sort()
n_pdfs = len(pdf_files)

window = tk.Tk()
window.title('HenriPDF')
Fm = tk.Frame(window)
Fleft = tk.Frame(Fm)
Fleft.grid(column=0, row=0, padx=(0, 15))
Fright = tk.Frame(Fm)
Fright.grid(column=1, row=0)

def pdf_name (index) :
    if index in range (0, n_pdfs) : return pdf_files[index].replace('.pdf', '')
    else : return 'empty'

class File_view_frame (tk.Frame) :
    def __init__ (self, master) :
        super().__init__(master)
        self.pdf_but_list = []
        self.itv = [0, 4]
        self.active = False
        for i in range(5) : 
           self.pdf_but_list.append(tk.Button(self, text=f'{pdf_name(i)}', bg='#ffffff', 
                                              command=lambda x = i: self.select(x)))
           self.pdf_but_list[i].grid(column=0, row=i+2)
        self.up_button = tk.Button(self, text='^', command=lambda:self.load(-1))
        self.up_button.grid(column=0, row=1)
        self.dw_button = tk.Button(self, text='v', command=lambda:self.load(1))
        self.dw_button.grid(column=0, row=7)
        self.concatenate_button = tk.Button(self, text='Concatenate', command=self.concatenate)
        self.concatenate_button.grid(column=0, row=8, pady=(30, 0))
        self.active = True
    
    def load(self, dir) :
       if ((self.itv[0] == 0 and dir == -1) or (self.itv[1] >= n_pdfs - 1 and dir == 1)) : return
       for but in self.pdf_but_list : 
          if (but['bg'] == "#00ebef") : but['bg'] = "#ffffff"
       if (self.active == False) : return
       for i in range(5) :
            index = self.itv[0] + i + 5 * dir
            self.pdf_but_list[i]['text'] = f'{pdf_name(index)}'
            self.pdf_but_list[i]['command'] = lambda x = index: self.select(x)
       self.itv[0] += 5 * dir
       self.itv[1] += 5 * dir
    
    def select(self, index) :
        if index not in range (0, n_pdfs) : return 
        for but in self.pdf_but_list : 
            if (but['bg'] == "#00ebef") : but['bg'] = "#ffffff"
        self.pdf_but_list[index % 5]['bg'] = "#00ebef"
        path = Path('pdfs') / f'{pdf_files[index]}'  
        pdf = [page for page in pypdf.PdfReader(path).pages]
        text = ''
        for page in pdf : text += (page.extract_text() + '\n')
        Tvf.resume_text(text)
    
    def concatenate (self) :
        paths = [Path('pdfs') / f'{pdf_file}' for pdf_file in pdf_files]
        writer = pypdf.PdfWriter()
        pdfs = [pdf for pdf in [pypdf.PdfReader(path) for path in paths]]
        pages_of_each = [pdf.pages for pdf in pdfs]
        for pages in pages_of_each :
            for page in pages : 
                writer.add_page(page)
        writer.write('output/concatenated_doc.pdf')

class Text_view_frame (tk.Frame) :
    def __init__ (self, master) :
        super().__init__(master)
        self.res_txt = scrolledtext.ScrolledText(
            self,
            wrap='word',
            width=80,
            height=25,
            state = 'disabled'
            )
        self.res_txt.grid(column=0, row=0)
        self.error = False

    def resume_text (self, text) :
        self.res_txt['state'] = 'normal'
        user_msg = Message(
            role="user",
            content= text + '\n(Tente resumir o texto acima, mesmo que tenha sido tirado de um pdf e que sua vizualização esteja complicada.)'
        )
        try : self.res_txt.insert('end', model.invoke(messages=[user_msg], assistant_message=Message(role="assistant", content='')).content) 
        except : 
            if (self.error == False) : 
                self.res_txt.insert('end', 'ocorreu um erro!')
                self.error = True
        self.res_txt['state'] = 'disabled'
        

Tvf = Text_view_frame(Fright)
Tvf.grid(column=0, row=0, padx=(0, 15), pady=(0, 15))

Fvf = File_view_frame(Fleft)
Fvf.grid(column=0, row=0, padx=(15, 0), pady=(0, 15))

Fm.pack()
messagebox.showinfo('Good Tip', 'Concatenation uses alphabetical order :\n' +
                    'Ex:\n' + 
                    '1_file\n2_file\n...\nn_file')
window.mainloop()
