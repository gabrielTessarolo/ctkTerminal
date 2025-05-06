# 💻 ctkTerminal

**ctkTerminal** is a custom terminal-like widget built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — a modern and beautiful UI library for Python's `tkinter`.

**ctkTerminal** é um widget estilo terminal personalizado, construído com base no [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — uma biblioteca moderna e bonita para interfaces com `tkinter` em Python.

---

## Features / Recursos

Its main purpose is to make it easy to insert to a custom CTkTextbox various colors and styles using ANSI characters, just like you were using the VSCode integrated terminal, for example.

- Easy to integrate into any CustomTkinter application  
- Fully customizable styles and layout  
- Lightweight and responsive design  
- Ready for future improvements like input/output simulation

---

## Class CTkTerminal

```py
class CTkTerminal(
    root: Any | None = None,
    line_span:      int = 5,
    column_span:    int = 1,
    width:          int = 100,
    height:         int = 20,
    font:           str = "Courier",
    size:           int = 12,
    text_color:     str = "white",
    bg_color:       str = "gray12"
) 
```

When an instance of CTkTerminal is initialized, it creates an instance of CTkTextbox and assigns the custom values passeds to it.
It provides a huge set of colors, beyond the classic ANSI codes supported natively by Python:

```txt
Color Documentation (ANSI Codes and Hexadecimal Values)

31 - red          - #FF0000
32 - green        - #00FF00
33 - yellow       - #FFFF00
34 - blue         - #0000FF
35 - purple       - #800080
36 - cyan         - #00FFFF
37 - white        - #FFFFFF
38 - dark_blue    - #00008B
39 - orange       - #FFA500
40 - gold         - #FFD700
41 - dark_red     - #8B0000
42 - dark_green   - #006400
43 - gray         - #808080
44 - dark_gray    - #A9A9A9
45 - light_gray   - #D3D3D3
46 - dark_purple  - #4B0082
47 - teal         - #008080
48 - pink         - #FFC0CB
49 - lime         - #00FF40
50 - beige        - #F5F5DC
```

You can pass your string (the line that is going to be added) and its formatting to your textbox using the function *addText*.
You can either define the color and style via its parameters or using the ANSI characters.

```py
(method) def addText(
    self: Self@CTkTerminal,
    text: Any,
    style: str = "auto",
    color: str = "auto",
    font: str = "Courier",
    size: int = 12,
    justify: str = "left"
) -> None
```

For example, if you want to add a golden text formatted with bold and underline, you can use:
```py
my_terminal = CTkTerminal()
my_terminal.addText('Check out my text!\n', color="gold", style="bold underline") # via parameters
my_terminal.addText('\033[14;40mCheck out my text!\033[3;47m\nAnd now comes another one!') # via ANSI
```

Result:
<p align="center"><img src="assets/demo.png" alt="CTkTerminal demo" width="600"/></p>

---

## 📦 Installation / Instalação

```bash
pip install git+https://github.com/gabrielTessarolo/ctkTerminal.git
