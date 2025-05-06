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
        self.colors = {
            31: {"name": "red", "hex": "#FF0000"},
            32: {"name": "green", "hex": "#00FF00"},
            33: {"name": "yellow", "hex": "#FFFF00"},
            34: {"name": "blue", "hex": "#0000FF"},
            35: {"name": "purple", "hex": "#800080"},
            36: {"name": "cyan", "hex": "#00FFFF"},
            37: {"name": "white", "hex": "#FFFFFF"},
            38: {"name": "dark_blue", "hex": "#00008B"},
            39: {"name": "orange", "hex": "#FFA500"},
            40: {"name": "gold", "hex": "#FFD700"},
            41: {"name": "dark_red", "hex": "#8B0000"},
            42: {"name": "dark_green", "hex": "#006400"},
            43: {"name": "gray", "hex": "#808080"},
            44: {"name": "dark_gray", "hex": "#A9A9A9"},
            45: {"name": "light_gray", "hex": "#D3D3D3"},
            46: {"name": "dark_purple", "hex": "#4B0082"},
            47: {"name": "teal", "hex": "#008080"},
            48: {"name": "pink", "hex": "#FFC0CB"},
            49: {"name": "lime", "hex": "#00FF40"},
            50: {"name": "beige", "hex": "#F5F5DC"},
        }
        
        # Configura a tag das cores
        for i in self.colors.keys():
            color = self.colors[i]
            self.textbox.tag_config(color["name"], foreground=color["hex"])

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

            try:
                colorID = int(i[1].split(';')[-1])
            except:
                colorID = 30
            segFormat["color"] = self.colors[colorID]["name"] if colorID in self.colors.keys() else "black"
            
            finalLine.append([i[0], segFormat])

        return finalLine

    # Função para adicionar uma linha de texto formatada em ANSI ao terminal
    def addText(self, text, font="Courier", size=12, style="normal", color="auto"):
        fontFormat = ctk.CTkFont()

        # Define fonte e tamanho customizados. Se der erro ou for igual, usa o padrão
        try:
            fontFormat.configure(family=font, size=size)
        except:
            fontFormat.configure(family=self.font, size=self.size)
            
        recognizedText = self.recognizeColors(text)
        for segment in recognizedText:
            if color == "auto":
                segColor = segment[1]["color"]
            else:
                segColor = color
            style = segment[1]["style"]
            textPart = segment[0]

            print(f"\033[1;35m{style}, {type(style)}, {"bold" in style}\033[m")
            segFont = ctk.CTkFont(fontFormat.cget("family"), fontFormat.cget("size"),
                weight="bold" if "bold" in style else "normal",
                slant="italic" if "italic" in style else "roman",
                underline=True if "underline" in style else False
            )

            tag_name = f"font_{id(segFont)}"
            try:
                if not self.textbox.tag_cget(tag_name, "font"):
                    self.textbox.tag_config(tag_name, cnf={"font": segFont})
            except:
                self.textbox.tag_config(tag_name, cnf={"font": segFont})    
                
            print(f"Adding text: {textPart} with font: {segFont.cget('weight')} and color: {color} and style: {style}")
            self.textbox.insert("end", textPart, tags=(tag_name, segColor))
            
if __name__ == "__main__":
    root = ctk.CTk()
    terminal = CtkTerminal(root=root, line_span=5, column_span=1, width=500, height=500, font="Courier", size=30, text_color="black", bg_color="black")
    terminal.textbox.pack()
    terminal.addText("\033[1;49mHello World!\033[m\n\033[13;31mThis is a test.\033[m\n\033[4;34mThis is underlined.\033[m\n\033[3;35mThis is italic.\033[m\n\033[1;33mThis is bold.\033[m\n\033[0;36mThis is normal.\033[m", font='Arial')
    root.mainloop()