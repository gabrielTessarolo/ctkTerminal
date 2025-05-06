import customtkinter as ctk
import tkinter as tk
import re

class CtkTerminal:
    def __init__(self, root=None, line_span=5, column_span=1, width=100, height=20, font="Courier", size=12, text_color="black", bg_color="white"):
        self.master = root if root else ctk.CTk()
        self.textbox = ctk.CTkTextbox(self.master, width=width, height=height, text_color=text_color, bg_color=bg_color)
        
        self.line_span = line_span
        self.column_span = column_span
        self.font = font
        self.size = size
        self.text_color = text_color
        self.bg_color = bg_color

        # Configura as cores a serem adicinadas
        self.textbox.tag_config("red", foreground="#FF0000")
        self.textbox.tag_config("green", foreground="#00FF00")
        self.textbox.tag_config("blue", foreground="#0000FF")
        self.textbox.tag_config("yellow", foreground="#FFFF00")
        self.textbox.tag_config("white", foreground="#FFFFFF")
        self.textbox.tag_config("black", foreground="#000000")
        self.textbox.tag_config("purple", foreground="#FF00FF")
        self.textbox.tag_config("cyan", foreground="#00FFFF")

        boldFont = ctk.CTkFont(self.font, self.size, weight="bold")
        italicFont = ctk.CTkFont(self.font, self.size, slant="italic")
        underlineFont = ctk.CTkFont(self.font, self.size, underline=True)

        # Mais tags úteis
        # Tags de estilo
        self.textbox.tag_config("bold", cnf={"font": boldFont})
        self.textbox.tag_config("italic", cnf={"font": italicFont})
        self.textbox.tag_config("underline", cnf={"font": underlineFont})

    def recognizeColors(self, text):
        splitted_text = [x for x in re.sub(r'\033\[([\d;]*)m', r'\\FORMAT\\', text).split("\\FORMAT\\") if x]
        identifiedColors = re.findall(r'\033\[([\d;]*)m', text)
        print("Identified Colors:", identifiedColors)
        print("Splitted Text:", splitted_text)
        segments = [[part, identifiedColors[c]] for c, part in enumerate(splitted_text) if part]

        finalLine = []

        for i in segments:
            segFormat = {'style': [], 'color': ''}
            if i[1]=='' or i[1]=='\n': 
                finalLine.append([i[0], segFormat])
            
            if ';' in i[1]:
                styleID = i[1].split(';')[0]
                if '1' in styleID:
                    segFormat["style"].append("bold")
                if '3' in styleID:
                    segFormat["style"].append("italic")
                if '4' in styleID:
                    segFormat["style"].append("underline")
                else:
                    pass

            colorID = i[1].split(';')[-1]
            if colorID == "31" or colorID == "91":
                segFormat["color"] = "red"
            elif colorID == "32" or colorID == "92":
                segFormat["color"] = "green"
            elif colorID == "33" or colorID == "93":
                segFormat["color"] = "yellow"
            elif colorID == "34" or colorID == "94":
                segFormat["color"] = "blue"
            elif colorID == "35" or colorID == "95":
                segFormat["color"] = "purple"
            elif colorID == "36" or colorID == "96":
                segFormat["color"] = "cyan"
            elif colorID == "37" or colorID == "97":
                segFormat["color"] = "white"
            else:
                segFormat["color"] = "black"

            finalLine.append([i[0], segFormat])

        return finalLine

    def addText(self, text, font="Courier", size=12, style="normal"):
        fontFormat = ctk.CTkFont()

        # Define fonte e tamanho customizados. Se der erro ou for igual, usa o padrão
        try:
            if not (font == self.font and size == self.size):
                fontFormat.configure(family=font, size=size)
        except:
            fontFormat.configure(family=self.font, size=self.size)
            
        recognizedText = self.recognizeColors(text)
        for segment in recognizedText:
            color = segment[1]["color"]
            style = segment[1]["style"]
            textPart = segment[0]

            print(f"\033[1;35m{style}\033[m")
            segFont = fontFormat
            if "bold" in style:
                segFont.configure(weight="bold")
            if "italic" in style:
                segFont.configure(slant="italic")
            if "underline" in style:
                segFont.configure(underline=True)

            self.textbox.tag_config("actFont", cnf={"font": segFont})

            print(f"Adding text: {textPart} with font: {segFont.cget('weight')} and color: {color} and style: {style}")
            self.textbox.insert("end", textPart, tags=("actFont", color))
            
if __name__ == "__main__":
    root = ctk.CTk()
    terminal = CtkTerminal(root=root, line_span=5, column_span=1, width=500, height=500, font="Courier", size=30, text_color="black", bg_color="black")
    terminal.textbox.pack()
    terminal.addText("\033[1;32mHello World!\033[m\n\033[1;31mThis is a test.\033[m\n\033[4;34mThis is underlined.\033[m\n\033[3;35mThis is italic.\033[m\n\033[1;33mThis is bold.\033[m\n\033[0;36mThis is normal.\033[m", size=20, font='Arial')
    root.mainloop()