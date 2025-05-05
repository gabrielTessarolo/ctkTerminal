import customtkinter as ctk
import tkinter as tk
import re

class CtkTerminal:
    def __init__(self, root=None, line_span=5, column_span=1, width=100, height=20, font="Courier", size=12, text_color="black", fg_color="white"):
        self.master = root if root else ctk.CTk()
        self.textbox = ctk.CTkTextbox(self.master, width=width, height=height)
        self.line_span = line_span
        self.column_span = column_span
        self.font = font
        self.text_color = text_color
        self.fg_color = fg_color

        # Configura as cores a serem adicinadas
        self.textbox.tag_config("red", foreground="#FF0000")
        self.textbox.tag_config("green", foreground="#00FF00")
        self.textbox.tag_config("blue", foreground="#0000FF")
        self.textbox.tag_config("yellow", foreground="#FFFF00")
        self.textbox.tag_config("white", foreground="#FFFFFF")
        self.textbox.tag_config("black", foreground="#000000")
        self.textbox.tag_config("gray", foreground="#808080")
        self.textbox.tag_config("purple", foreground="#FF00FF")
        self.textbox.tag_config("cyan", foreground="#00FFFF")

    @staticmethod
    def recognizeColors(text):
        splitted_text = [x for x in re.sub(r'\033\[([\d;]*)m', r'\\COLOR\\', text).split("\\COLOR\\") if x]
        identifiedColors = re.findall(r'\033\[([\d;]*)m', text)
        print("Identified Colors:", identifiedColors)
        print("Splitted Text:", splitted_text)
        segments = [[part, identifiedColors[c]] for c, part in enumerate(splitted_text) if part]

        finalLine = []
        for i in segments:
            colorID = i[1][-2:]
            if colorID == "31" or colorID == "91":
                finalLine.append([i[0], "red"])
            elif colorID == "32" or colorID == "92":
                finalLine.append([i[0], "green"])
            elif colorID == "33" or colorID == "93":
                finalLine.append([i[0], "yellow"])
            elif colorID == "34" or colorID == "94":
                finalLine.append([i[0], "blue"])
            elif colorID == "35" or colorID == "95":
                finalLine.append([i[0], "purple"])
            elif colorID == "36" or colorID == "96":
                finalLine.append([i[0], "cyan"])
            elif colorID == "37" or colorID == "97":
                finalLine.append([i[0], "white"])
        
        return finalLine

    # AQUI TA DANDO ERRADO HEIN, SÓ DEFINE FONTE E TAMANHO DIRETO NA TEXTBOX
    def addText(self, text, font="Courier", size=12, style="normal"):
        recognizedText = self.recognizeColors(text)
        for i in recognizedText:
            color = i[1]
            textPart = i[0]
            self.textbox.insert("end", textPart, color, font=(font, size, style))
            
if __name__ == "__main__":
    root = ctk.CTk()
    terminal = CtkTerminal(root=root, line_span=5, column_span=1, width=100, height=20, font="Courier", size=12, text_color="black", fg_color="white")
    terminal.textbox.pack()
    terminal.addText("\033[1;32mHello World!\033[m")
    root.mainloop()