import tkinter as tk
from typing import Union


class Gui(tk.Tk):
    def __init__(self,
                 size: Union[tuple[int, int], tuple[int, int, int, int]] = None,
                 title: str = None,
                 icon: str = None,
                 **configurations):
        if size is None: size = (500, 400)
        if title is None: title = "Gui"

        assert isinstance(size, tuple) and (len(size) in (2, 4)) and all([isinstance(s, int) for s in size]), \
            "size must be a tuple of 'int' of length 2 or 4"

        super(Gui, self).__init__(**configurations)
        x, y = ((self.winfo_screenwidth() - size[0]) // 2, (self.winfo_screenheight() - size[1]) // 4) \
            if len(size) == 2 else size[2:]
        w, h = size[:2]
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.title(title)
        if icon is not None: self.iconbitmap(icon)

        self.minsize(*size)

        self.mainFrame = tk.Frame(self, bg="white smoke")
        # write your ui build here
        self.mainFrame.pack(expand=True, fill="both")


Gui().mainloop()
