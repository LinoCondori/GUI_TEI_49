# gui.py
import tkinter as tk
from manager import InstrumentManager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI TEI 49")

        import tkinter as tk

        menubar = tk.Menu(self.root)

        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Abrir configuración")
        menu_archivo.add_command(label="Guardar configuración")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=root.quit)

        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        self.root.config(menu=menubar)


        self.manager = InstrumentManager()

        # Frame superior
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)
        new_inst_frame = tk.Frame(top_frame)
        new_inst_frame.pack(side=tk.LEFT, pady=10)
        self.entry_name = tk.Entry(new_inst_frame)
        self.entry_name.pack()
        self.entry_port = tk.Entry(new_inst_frame)
        self.entry_port.pack()
        self.entry_instrument_id = tk.Entry(new_inst_frame)
        self.entry_instrument_id.pack()

        add_button = tk.Button(top_frame, text="Agregar\nInstrumento", command=self.add_instrument)
        add_button.pack(side=tk.LEFT, padx=5)

        # Frame de instrumentos
        self.instruments_frame = tk.Frame(top_frame)
        self.instruments_frame.pack(pady=10, side="left")

        self.labels = {}
        self.inst_frame = {}


        self.update_loop()

    def add_instrument(self):
        name = self.entry_name.get()
        port = self.entry_port.get()
        instrument_id = self.entry_instrument_id.get()
        if name:
            instrument = self.manager.add_instrument(name, port, instrument_id)
            if instrument is None:
                print("Ya existe un instrumento con ese nombre")
                return
            frame = tk.Frame(self.instruments_frame)
            frame.pack(side="left")

            self.entry_name.delete(0, tk.END)
            self.entry_port.delete(0, tk.END)
            self.entry_instrument_id.delete(0, tk.END)
            btn_delete = tk.Button(
                frame,
                text="X",
                fg="red",
                command=lambda inst=instrument: self.remove_instrument(inst)
            )
            btn_delete.pack(anchor="ne",side="right")
            label_name = tk.Label(frame, text=name)
            label_name.pack()
            label_port = tk.Label(frame, text=port)
            label_port.pack()
            label_instrument_id = tk.Label(frame, text=instrument_id)
            label_instrument_id.pack()
            label_value = tk.Label(frame, text=f"--")
            label_value.pack()
            var_enabled = tk.BooleanVar(value=True)
            check = tk.Checkbutton(
                frame,
                text="Habilitado",
                variable=var_enabled,
                command=lambda inst=instrument, var=var_enabled: self.toggle_instrument(inst, var),
            )
            check.pack()

            self.inst_frame[instrument] = {
                "frame": frame,
                "label_value": label_value,
                "enable":var_enabled,
            }

            instrument.start()
            #label = tk.Label(self.instruments_frame, text=f"{name}: --")
            #label.pack(side="left")
            #self.labels[name] = label
            #self.entry_name.delete(0, tk.END)

    def update_loop(self):
        for instrument in self.manager.get_instruments():
            #value = instrument.read_value()
            if instrument in self.inst_frame:
                #if self.inst_frame[instrument.name]["enable"].get():
                #    self.inst_frame[instrument.name]["label_value"].config(text=f'{value}')
                #else:
                #    self.inst_frame[instrument.name]["label_value"].config(text=f'------')
                self.inst_frame[instrument]["label_value"].config(text=f'{instrument.value}')
        self.root.after(200, self.update_loop)  # actualiza cada 2 segundos

    def toggle_instrument(self, instrument, var):
        if var.get():
            instrument.start()
        else:
            instrument.stop()

    def remove_instrument(self, instrument):

        instrument.stop()

        self.manager.remove_instrument(instrument)

        if instrument in self.inst_frame:
            self.inst_frame[instrument]["frame"].destroy()

            del self.inst_frame[instrument]

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
