import threading
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
import tkinter.font as tkfont
import os
import sys

try:
    from .crm_api_generator import send_ticket_generation_requests
    from .fota_batch_generator import generate_fota_batch_csv
    from .institutional_sales_generator import generate_institutional_sales
    from .sample_file_generators import generate_all_sample_files
    from .settings import SETTINGS
    from .sim_batch_generator import generate_sim_batch_csv
    from .ticket_data_csv_generator import generate_ticket_data_csv
    from .ticket_json_generator import generate_ticket_json
except ImportError:  # Allows running app.py directly.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    package_root = os.path.dirname(current_dir)
    if package_root not in sys.path:
        sys.path.insert(0, package_root)
    from vehicle_data_generator.crm_api_generator import send_ticket_generation_requests
    from vehicle_data_generator.fota_batch_generator import generate_fota_batch_csv
    from vehicle_data_generator.institutional_sales_generator import generate_institutional_sales
    from vehicle_data_generator.sample_file_generators import generate_all_sample_files
    from vehicle_data_generator.settings import SETTINGS
    from vehicle_data_generator.sim_batch_generator import generate_sim_batch_csv
    from vehicle_data_generator.ticket_data_csv_generator import generate_ticket_data_csv
    from vehicle_data_generator.ticket_json_generator import generate_ticket_json


class VDGDesktopApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Vehicle Data Generator")
        self.geometry("980x720")
        self.minsize(900, 680)

        self.output_dir_var = tk.StringVar(value=SETTINGS.default_output_dir)
        self.records_var = tk.StringVar(value="10")
        self.fota_file_var = tk.StringVar(value="fota_batch.csv")
        self.fota_ufw_var = tk.StringVar(value=SETTINGS.default_fota_ufw)
        self.fota_model_var = tk.StringVar(value=SETTINGS.default_fota_model)
        self.ticket_csv_file_var = tk.StringVar(value="generated_records.csv")
        self.vin_start_var = tk.StringVar(value="40")
        self.vin_end_var = tk.StringVar(value="45")
        self.vin_prefix_var = tk.StringVar(value="SURAJ07082025_")

        self._configure_style()
        self._build_ui()

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        base_font = tkfont.nametofont("TkDefaultFont")
        base_font.configure(size=10)
        heading_font = base_font.copy()
        heading_font.configure(size=14, weight="bold")
        subheading_font = base_font.copy()
        subheading_font.configure(size=9)

        self._heading_font = heading_font
        self._subheading_font = subheading_font

        bg = "#f6f7fb"
        panel = "#ffffff"
        border = "#d9dbe7"
        accent = "#1e40af"
        soft = "#eef2ff"

        self.configure(bg=bg)

        style.configure("App.TFrame", background=bg)
        style.configure("Panel.TFrame", background=panel, relief="solid", borderwidth=1)
        style.configure("Header.TFrame", background=panel)
        style.configure("App.TLabel", background=panel, foreground="#111827")
        style.configure("Header.TLabel", background=panel, foreground="#0f172a")
        style.configure("SubHeader.TLabel", background=panel, foreground="#475569")
        style.configure("Section.TLabelframe", background=panel, foreground="#0f172a", bordercolor=border)
        style.configure("Section.TLabelframe.Label", background=panel, foreground="#0f172a")
        style.configure("TEntry", padding=6)
        style.configure("TButton", padding=(10, 6))
        style.configure("Primary.TButton", background=accent, foreground="#ffffff", bordercolor=accent)
        style.map("Primary.TButton",
                  background=[("active", "#1d4ed8"), ("disabled", "#93c5fd")],
                  foreground=[("disabled", "#e0e7ff")])
        style.configure("Ghost.TButton", background=soft, foreground=accent, bordercolor="#c7d2fe")
        style.map("Ghost.TButton", background=[("active", "#e0e7ff")])

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=16, style="App.TFrame")
        root.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(root, padding=(16, 14), style="Header.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Vehicle Data Generator", font=self._heading_font, style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Generate CSV, JSON, and CRM data with clear configuration blocks.",
            font=self._subheading_font,
            style="SubHeader.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        content = ttk.Frame(root, style="App.TFrame")
        content.grid(row=1, column=0, sticky="nsew")
        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)

        settings_frame = ttk.LabelFrame(content, text="General Settings", padding=12, style="Section.TLabelframe")
        settings_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        ttk.Label(settings_frame, text="Output Directory", style="App.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)
        ttk.Entry(settings_frame, textvariable=self.output_dir_var, width=60).grid(row=0, column=1, sticky="ew", pady=6)
        ttk.Button(settings_frame, text="Browse", command=self._browse_output, style="Ghost.TButton").grid(row=0, column=2, padx=(8, 0), pady=6)

        ttk.Label(settings_frame, text="Record Count", style="App.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)
        ttk.Entry(settings_frame, textvariable=self.records_var, width=14).grid(row=1, column=1, sticky="w", pady=6)
        settings_frame.columnconfigure(1, weight=1)

        generation_frame = ttk.LabelFrame(content, text="Data Generation", padding=12, style="Section.TLabelframe")
        generation_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        generation_frame.columnconfigure(0, weight=1)
        generation_frame.columnconfigure(1, weight=1)

        actions_frame = ttk.Frame(generation_frame, style="Panel.TFrame", padding=10)
        actions_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        actions_frame.columnconfigure(0, weight=1)
        ttk.Label(actions_frame, text="Quick Actions", style="App.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))

        ttk.Button(
            actions_frame,
            text="Generate SIM Batch CSV",
            command=lambda: self._run_async(self._action_sim_batch),
            style="Primary.TButton",
        ).grid(row=1, column=0, sticky="ew", pady=4)
        ttk.Button(
            actions_frame,
            text="Generate Ticket JSON",
            command=lambda: self._run_async(self._action_ticket_json),
        ).grid(row=2, column=0, sticky="ew", pady=4)
        ttk.Button(
            actions_frame,
            text="Generate Institutional Sales XLSX",
            command=lambda: self._run_async(self._action_institutional_sales),
        ).grid(row=3, column=0, sticky="ew", pady=4)
        ttk.Button(
            actions_frame,
            text="Generate Sample Files",
            command=lambda: self._run_async(self._action_sample_files),
        ).grid(row=4, column=0, sticky="ew", pady=4)

        config_frame = ttk.Frame(generation_frame, style="Panel.TFrame", padding=10)
        config_frame.grid(row=0, column=1, sticky="nsew")
        config_frame.columnconfigure(1, weight=1)
        config_frame.columnconfigure(3, weight=1)
        ttk.Label(config_frame, text="Configuration", style="App.TLabel").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

        ttk.Label(config_frame, text="FOTA Filename", style="App.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(config_frame, textvariable=self.fota_file_var, width=26).grid(row=1, column=1, sticky="ew", pady=6)
        ttk.Label(config_frame, text="UFW Version", style="App.TLabel").grid(row=1, column=2, sticky="w", padx=(12, 8), pady=6)
        ttk.Entry(config_frame, textvariable=self.fota_ufw_var, width=22).grid(row=1, column=3, sticky="ew", pady=6)

        ttk.Label(config_frame, text="FOTA Model", style="App.TLabel").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(config_frame, textvariable=self.fota_model_var, width=22).grid(row=2, column=1, sticky="ew", pady=6)
        ttk.Label(config_frame, text="Ticket CSV Filename", style="App.TLabel").grid(row=2, column=2, sticky="w", padx=(12, 8), pady=6)
        ttk.Entry(config_frame, textvariable=self.ticket_csv_file_var, width=22).grid(row=2, column=3, sticky="ew", pady=6)

        ttk.Button(
            config_frame,
            text="Generate FOTA Batch CSV",
            command=lambda: self._run_async(self._action_fota_batch),
            style="Ghost.TButton",
        ).grid(row=3, column=2, sticky="ew", pady=(8, 0))
        ttk.Button(
            config_frame,
            text="Generate Ticket CSV",
            command=lambda: self._run_async(self._action_ticket_csv),
            style="Ghost.TButton",
        ).grid(row=3, column=3, sticky="ew", pady=(8, 0))

        crm_frame = ttk.LabelFrame(content, text="CRM API", padding=12, style="Section.TLabelframe")
        crm_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(crm_frame, text="VIN Start", style="App.TLabel").grid(row=0, column=0, sticky="w", padx=4, pady=6)
        ttk.Entry(crm_frame, textvariable=self.vin_start_var, width=10).grid(row=0, column=1, sticky="w", padx=4, pady=6)
        ttk.Label(crm_frame, text="VIN End", style="App.TLabel").grid(row=0, column=2, sticky="w", padx=4, pady=6)
        ttk.Entry(crm_frame, textvariable=self.vin_end_var, width=10).grid(row=0, column=3, sticky="w", padx=4, pady=6)
        ttk.Label(crm_frame, text="VIN Prefix", style="App.TLabel").grid(row=0, column=4, sticky="w", padx=4, pady=6)
        ttk.Entry(crm_frame, textvariable=self.vin_prefix_var, width=30).grid(row=0, column=5, sticky="ew", padx=4, pady=6)
        ttk.Button(
            crm_frame,
            text="Send CRM Requests",
            command=lambda: self._run_async(self._action_crm),
            style="Primary.TButton",
        ).grid(row=0, column=6, sticky="ew", padx=4, pady=6)
        crm_frame.columnconfigure(5, weight=1)

        log_frame = ttk.LabelFrame(content, text="Execution Log", padding=12, style="Section.TLabelframe")
        log_frame.grid(row=3, column=0, sticky="nsew")
        content.rowconfigure(3, weight=1)
        self.log_text = tk.Text(
            log_frame,
            height=14,
            wrap="word",
            state=tk.DISABLED,
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            relief="flat",
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def _browse_output(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.output_dir_var.get() or ".")
        if selected:
            self.output_dir_var.set(selected)

    def _get_positive_int(self, value: str, field_name: str) -> int:
        parsed = int(value)
        if parsed <= 0:
            raise ValueError(f"{field_name} must be greater than zero.")
        return parsed

    def _log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _run_async(self, action) -> None:
        thread = threading.Thread(target=self._run_action, args=(action,), daemon=True)
        thread.start()

    def _run_action(self, action) -> None:
        try:
            result = action()
            if isinstance(result, dict):
                self.after(0, lambda: self._log(f"Success: {result}"))
            elif result:
                self.after(0, lambda: self._log(f"Success: {result}"))
            else:
                self.after(0, lambda: self._log("Completed successfully."))
        except Exception as exc:  # noqa: BLE001
            self.after(0, lambda: self._log(f"Error: {exc}"))
            self.after(0, lambda: messagebox.showerror("Execution Error", str(exc)))

    def _action_sim_batch(self):
        return generate_sim_batch_csv(
            num_records=self._get_positive_int(self.records_var.get(), "Record Count"),
            output_dir=self.output_dir_var.get() or None,
        )

    def _action_ticket_json(self):
        return generate_ticket_json(
            num_records=self._get_positive_int(self.records_var.get(), "Record Count"),
            output_dir=self.output_dir_var.get() or None,
        )

    def _action_fota_batch(self):
        return generate_fota_batch_csv(
            output_file=self.fota_file_var.get().strip() or "fota_batch.csv",
            number_of_records=self._get_positive_int(self.records_var.get(), "Record Count"),
            ufw_version=self.fota_ufw_var.get().strip() or None,
            model=self.fota_model_var.get().strip() or None,
            output_dir=self.output_dir_var.get() or None,
        )

    def _action_institutional_sales(self):
        return generate_institutional_sales(
            number_of_records=self._get_positive_int(self.records_var.get(), "Record Count"),
            output_dir=self.output_dir_var.get() or None,
        )

    def _action_sample_files(self):
        return generate_all_sample_files(
            num_records=self._get_positive_int(self.records_var.get(), "Record Count"),
            output_dir=self.output_dir_var.get() or None,
        )

    def _action_ticket_csv(self):
        return generate_ticket_data_csv(
            number_of_records=self._get_positive_int(self.records_var.get(), "Record Count"),
            output_file=self.ticket_csv_file_var.get().strip() or "generated_records.csv",
            output_dir=self.output_dir_var.get() or None,
        )

    def _action_crm(self):
        responses = send_ticket_generation_requests(
            vin_start=self._get_positive_int(self.vin_start_var.get(), "VIN Start"),
            vin_end=self._get_positive_int(self.vin_end_var.get(), "VIN End"),
            vin_prefix=self.vin_prefix_var.get().strip() or "SURAJ07082025_",
        )
        return f"CRM calls completed: {len(responses)} requests."


def main() -> int:
    app = VDGDesktopApp()
    app.mainloop()
    return 0
