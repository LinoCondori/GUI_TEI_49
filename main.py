# gui.py
import tkinter as tk
from tkinter import filedialog

import pandas as pd

from manager import InstrumentManager
import json
from datetime import datetime, timedelta
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure




class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI TEI 49")

        import tkinter as tk

        menubar = tk.Menu(self.root)

        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Guardar", command=self.save_config)
        menu_archivo.add_command(label="Guardar como...", command=self.save_config_as)
        menu_archivo.add_command(label="Abrir", command=self.load_config)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit)

        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        self.root.config(menu=menubar)

        self.manager = InstrumentManager()

        # Frame superior
        top_frame = tk.Frame(root)
        top_frame.pack(side="top", anchor="nw", pady=10)
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

        self.inst_frame = {}

        try:
            self.load_config("last_config.json")
        except Exception as e:
            print("Error cargando config:", e)

        # Frame para gráficos
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack(fill="both", expand=True)

        self.figure = Figure(figsize=(8, 6), dpi=100)

        self.ax_hour = self.figure.add_subplot(121)  # izq
        self.ax_24h = self.figure.add_subplot(122)  # der

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        self.update_loop()
        self.update_graph()

        self.update_minute_file()


    def add_instrument(self):
        name = self.entry_name.get()
        port = self.entry_port.get()
        instrument_id = self.entry_instrument_id.get()
        if name:
            instrument = self.manager.add_instrument(name, port, instrument_id)
            if instrument is None:
                print("Ya existe un instrumento con ese nombre")
                return
            self.create_instrument_ui(instrument, enabled=True)


            self.entry_name.delete(0, tk.END)
            self.entry_port.delete(0, tk.END)
            self.entry_instrument_id.delete(0, tk.END)
    def create_instrument_ui(self, instrument, enabled=True):

        frame = tk.Frame(self.instruments_frame)
        frame.pack(side="left")

        btn_delete = tk.Button(
            frame,
            text="X",
            fg="red",
            command=lambda inst=instrument: self.remove_instrument(inst)
        )
        btn_delete.pack(anchor="ne", side="right")

        tk.Label(frame, text=instrument.name).pack()
        tk.Label(frame, text=instrument.port).pack()
        tk.Label(frame, text=instrument.instrument_id).pack()

        label_value = tk.Label(frame, text="--")
        label_value.pack()

        var_enabled = tk.BooleanVar(value=enabled)

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
            "enable": var_enabled,
        }

        if enabled:
            instrument.start()

    def update_loop(self):
        for instrument in self.manager.get_instruments():
            #value = instrument.read_value()
            if instrument in self.inst_frame:
                #if self.inst_frame[instrument.name]["enable"].get():
                #    self.inst_frame[instrument.name]["label_value"].config(text=f'{value}')
                #else:
                #    self.inst_frame[instrument.name]["label_value"].config(text=f'------')
                if instrument.value  is not None:
                    if instrument.communication.port.startswith("COM"):
                        pass

                    elif "." in instrument.communication.host:
                        #print("Mostrando Datos TCP")
                        self.inst_frame[instrument]["label_value"].config(text=f'{instrument.value.split()[
                            instrument.communication.header.split().index('Concentration_(ppb_or_ug/m3)')]}')
                    else:
                        self.inst_frame[instrument]["label_value"].config(text=f'{instrument.value.split(',')[0]}')
        self.root.after(20000, self.update_loop)  # actualiza cada 2 segundos los instrumentos

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

    # esta funcion es para obtener la configuracion actual
    def get_config_data(self):
        return {
            "instrumentos": [
                {
                    "name": inst.name,
                    "port": inst.port,
                    "instrument_id": inst.instrument_id,
                    "enabled": inst.running
                }
                for inst in self.manager.get_instruments()
            ]
        }



    def save_config(self, filename="last_config.json"):
        data = self.get_config_data()
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)



    def save_config_as(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if file:
            self.save_config(file)

    def load_config(self, filename=None):

        if not filename:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json")]
            )

        if not filename:
            return

        with open(filename, "r") as f:
            data = json.load(f)

        #  Primero limpiar todo
        for inst in list(self.manager.get_instruments()):
            self.remove_instrument(inst)

        #  Crear instrumentos nuevos
        for item in data["instrumentos"]:
            instrument = self.manager.add_instrument(
                item["name"],
                item["port"],
                item["instrument_id"]
            )

            enabled = item.get("enabled", False)
            self.create_instrument_ui(instrument, enabled=enabled)


    def create_path_raw(self, fechaHora, instrument):
        year = fechaHora.strftime("%Y")
        date_str = fechaHora.strftime("%Y-%m-%d")

        base_path = os.path.join("data", instrument, "crudo", year)
        return os.path.join(base_path, f"{date_str}.csv")

    def create_path_avg(self, fechaHora, instrument):
        year = fechaHora.strftime("%Y")
        date_str = fechaHora.strftime("%Y-%m-%d")

        base_path = os.path.join("data", instrument, year)
        return os.path.join(base_path, f"{date_str}.csv")

    def update_graph(self):
        now = datetime.now()
        yesterday = now - timedelta(hours=24)


        self.ax_hour.clear()
        self.ax_24h.clear()

        for instrument in self.manager.get_instruments():
            file_path_now = self.create_path_raw(now, instrument.name)
            file_path_yesterday = self.create_path_raw(yesterday, instrument.name)
            df_full = pd.concat([instrument.load_data_from_file(file_path_now) , instrument.load_data_from_file(file_path_yesterday)], axis=0)
            try:
                filter_1H = df_full["FechaHora"] >= pd.to_datetime(now) - pd.to_timedelta(1, "hour")
                df = df_full.loc[filter_1H]
                if df is not None and not df.empty:
                    self.ax_hour.plot(df["FechaHora"], df["dato1"], label=instrument.name)

                filter_24H = df_full["FechaHora"] >= pd.to_datetime(now) - pd.to_timedelta(24, "hour")
                df = df_full.loc[filter_24H]
                if df is not None and not df.empty:
                    self.ax_24h.plot(df["FechaHora"], df["dato1"], label=instrument.name)
            except:
                self.root.after(10000, self.update_graph)  # cada 10 segundos
                return
        self.ax_hour.legend()
        self.ax_hour.set_title("Última hora")
        self.ax_hour.tick_params(axis='x', rotation=45)

        self.ax_24h.legend()
        self.ax_24h.set_title("Última 24 Horas")
        self.ax_24h.tick_params(axis='x', rotation=45)


        self.canvas.draw()

        self.root.after(20000, self.update_graph)  # cada 10 segundos


    def update_minute_file(self):
        now = datetime.now() - timedelta(minutes=5)
        for instrument in self.manager.get_instruments():
            file_path_now = self.create_path_raw(now, instrument.name)
            df_avg = instrument.minute_average(file_path_now)
            file_path_avg = self.create_path_avg(now, instrument.name)
            base_path = os.path.join(os.path.dirname(file_path_avg))
            os.makedirs(base_path, exist_ok=True)
            if df_avg.empty:
                return
            df_avg.to_csv(file_path_avg)
        self.root.after(60000, self.update_minute_file)  # cada 10 segundos



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
