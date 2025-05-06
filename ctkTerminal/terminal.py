import customtkinter as ctk
import tkinter as tk
import re

class CTkTerminal:
    def __init__(self, root=None, line_span=5, column_span=1, width=100, height=20, font="Courier", size=12, text_color="white", bg_color="gray12"):
        self.master = root if root else ctk.CTk()
        self.textbox = ctk.CTkTextbox(self.master, width=width, height=height, text_color=text_color, fg_color=bg_color)
        self.textbox.configure(state="disabled")

        self.line_span = line_span
        self.column_span = column_span
        self.font = font
        self.size = size
        self.text_color = text_color
        self.bg_color = bg_color
        
        # Configura as cores a serem adicionadas
        self.colors = {
            30: {"name": "black",           "hex": "#000000"},
            31: {"name": "red",             "hex": "#FF0000"},
            32: {"name": "green",           "hex": "#00FF00"},
            33: {"name": "yellow",          "hex": "#FFFF00"},
            34: {"name": "blue",            "hex": "#0000FF"},
            35: {"name": "purple",          "hex": "#800080"},
            36: {"name": "cyan",            "hex": "#00FFFF"},
            37: {"name": "white",           "hex": "#FFFFFF"},
            38: {"name": "dark_blue",       "hex": "#00008B"},
            39: {"name": "orange",          "hex": "#FFA500"},
            40: {"name": "gold",            "hex": "#FFD700"},
            41: {"name": "dark_red",        "hex": "#8B0000"},
            42: {"name": "dark_green",      "hex": "#006400"},
            43: {"name": "gray",            "hex": "#808080"},
            44: {"name": "dark_gray",       "hex": "#A9A9A9"},
            45: {"name": "light_gray",      "hex": "#D3D3D3"},
            46: {"name": "dark_purple",     "hex": "#4B0082"},
            47: {"name": "teal",            "hex": "#008080"},
            48: {"name": "pink",            "hex": "#FFC0CB"},
            49: {"name": "lime",            "hex": "#00FF40"},
            50: {"name": "beige",           "hex": "#F5F5DC"},
        }
        
        
        # Configura a tag das cores
        for i in self.colors.keys():
            color = self.colors[i]
            self.textbox.tag_config(color["name"], foreground=color["hex"])

        # Configurações de alinhamento
        self.textbox.tag_config("left", justify="left")
        self.textbox.tag_config("center", justify="center")
        self.textbox.tag_config("right", justify="right")

    def recognizeColors(self, text):
        splitted_text = [x for x in re.sub(r'\033\[([\d;]*)m', r'\\FORMAT\\', text).split("\\FORMAT\\") if x]
        
        # Evita que dois ou mais códigos ANSI sejam aplicados em sequência
        filteredText = re.sub(r'(\033\[[\d;]*m)(?=\033\[[\d;]*m)', '', text)
        identifiedColors = re.findall(r'\033\[([\d;]*)m', filteredText)
    
        if identifiedColors == []:
            return [[text, {}]]
        segments = [[part, identifiedColors[c]] for c, part in enumerate(splitted_text)]

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

            try:
                colorID = int(i[1].split(';')[-1])
            except:
                colorID = 30
            segFormat["color"] = self.colors[colorID]["name"] if colorID in self.colors.keys() else "black"
            
            finalLine.append([i[0], segFormat])

        return finalLine

    # Função para adicionar uma linha de texto formatada em ANSI ao terminal
    def addText(self, text, font="Courier", size=12, style="auto", color="auto", justify="left"):
        fontFormat = ctk.CTkFont()

        # Define fonte e tamanho customizados. Se der erro ou for igual, usa o padrão
        try:
            fontFormat.configure(family=font, size=size)
        except:
            fontFormat.configure(family=self.font, size=self.size)
            
        recognizedText = self.recognizeColors(text)
        for segment in recognizedText:
            try:
                if color == "auto":
                    segColor = segment[1]["color"]
                else:
                    segColor = color
                if style == "auto":
                    segStyle = segment[1]["style"]
                else:
                    segStyle = [x for x in style.split(" ") if x in ["bold", "italic", "underline"]]
            except:
                segColor = "black" if color=="auto" else color
                segStyle = "normal" if style=="auto" else style

            textPart = segment[0]

            segFont = ctk.CTkFont(fontFormat.cget("family"), fontFormat.cget("size"),
                weight="bold" if "bold" in segStyle else "normal",
                slant="italic" if "italic" in segStyle else "roman",
                underline=True if "underline" in segStyle else False
            )

            tag_name = f"font_{id(segFont)}"
            try:
                if not self.textbox.tag_cget(tag_name, "font"):
                    self.textbox.tag_config(tag_name, cnf={"font": segFont})
            except:
                self.textbox.tag_config(tag_name, cnf={"font": segFont})    
            
            self.textbox.configure(state="normal")
            self.textbox.insert("end", textPart, tags=(tag_name, segColor, justify))
            self.textbox.configure(state="disabled")    

    def clear(self, line=0, line_span=1):
        if line == 0:
            self.textbox.delete("1.0", "end")
        else:
            try:        
                self.textbox.delete(f"{line}.0", f"{line+line_span}.0")      
            except:
                self.textbox.delete(f"{line}.0", "end")
    
if __name__ == "__main__":
    root = ctk.CTk()
    terminal = CTkTerminal(root=root, line_span=5, column_span=1, width=500, height=100, font="Courier", size=30, text_color="black", bg_color="gray12")
    terminal.textbox.pack()
    terminal.addText("\033[1;49mHello World!\033[m\033[13;47mThis is a test.\033[m\n\033[4;48mThis is underlined.\033[m\n\033[3;35mThis is italic.\033[m\n\033[1;33mThis is bold.\033[m\n\033[0;36mThis is normal.\033[m", size=20, font='Arial', justify='center')
    terminal.addText("\nMy Terminal is cool", size=20, font='Impact', justify='right', color="blue")
    root.mainloop()