import threading
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

from .crm_api_generator import send_ticket_generation_requests
from .fota_batch_generator import generate_fota_batch_csv
from .institutional_sales_generator import generate_institutional_sales
from .sample_file_generators import generate_all_sample_files
from .settings import SETTINGS
from .sim_batch_generator import generate_sim_batch_csv
from .ticket_data_csv_generator import generate_ticket_data_csv
from .ticket_json_generator import generate_ticket_json


class VDGDesktopApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Vehicle Data Generator")
        self.geometry("880x650")
        self.minsize(820, 620)

        self.output_dir_var = tk.StringVar(value=SETTINGS.default_output_dir)
        self.records_var = tk.StringVar(value="10")
        self.fota_file_var = tk.StringVar(value="fota_batch.csv")
        self.fota_ufw_var = tk.StringVar(value=SETTINGS.default_fota_ufw)
        self.fota_model_var = tk.StringVar(value=SETTINGS.default_fota_model)
        self.ticket_csv_file_var = tk.StringVar(value="generated_records.csv")
        self.vin_start_var = tk.StringVar(value="40")
        self.vin_end_var = tk.StringVar(value="45")
        self.vin_prefix_var = tk.StringVar(value="SURAJ07082025_")

        self._build_ui()

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=12)
        root.pack(fill=tk.BOTH, expand=True)

        settings_frame = ttk.LabelFrame(root, text="General Settings", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(settings_frame, text="Output Directory").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(settings_frame, textvariable=self.output_dir_var, width=70).grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Button(settings_frame, text="Browse", command=self._browse_output).grid(row=0, column=2, padx=(8, 0), pady=4)

        ttk.Label(settings_frame, text="Record Count").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(settings_frame, textvariable=self.records_var, width=14).grid(row=1, column=1, sticky="w", pady=4)
        settings_frame.columnconfigure(1, weight=1)

        generation_frame = ttk.LabelFrame(root, text="Data Generation", padding=10)
        generation_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            generation_frame,
            text="Generate SIM Batch CSV",
            command=lambda: self._run_async(self._action_sim_batch),
        ).grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        ttk.Button(
            generation_frame,
            text="Generate Ticket JSON",
            command=lambda: self._run_async(self._action_ticket_json),
        ).grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        ttk.Button(
            generation_frame,
            text="Generate Institutional Sales XLSX",
            command=lambda: self._run_async(self._action_institutional_sales),
        ).grid(row=0, column=2, sticky="ew", padx=4, pady=4)
        ttk.Button(
            generation_frame,
            text="Generate Sample Files",
            command=lambda: self._run_async(self._action_sample_files),
        ).grid(row=0, column=3, sticky="ew", padx=4, pady=4)

        ttk.Label(generation_frame, text="FOTA Filename").grid(row=1, column=0, sticky="w", padx=4, pady=(10, 4))
        ttk.Entry(generation_frame, textvariable=self.fota_file_var, width=24).grid(row=1, column=1, sticky="ew", padx=4, pady=(10, 4))
        ttk.Label(generation_frame, text="UFW Version").grid(row=1, column=2, sticky="w", padx=4, pady=(10, 4))
        ttk.Entry(generation_frame, textvariable=self.fota_ufw_var, width=24).grid(row=1, column=3, sticky="ew", padx=4, pady=(10, 4))

        ttk.Label(generation_frame, text="FOTA Model").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(generation_frame, textvariable=self.fota_model_var, width=24).grid(row=2, column=1, sticky="ew", padx=4, pady=4)
        ttk.Label(generation_frame, text="Ticket CSV Filename").grid(row=2, column=2, sticky="w", padx=4, pady=4)
        ttk.Entry(generation_frame, textvariable=self.ticket_csv_file_var, width=24).grid(row=2, column=3, sticky="ew", padx=4, pady=4)

        ttk.Button(
            generation_frame,
            text="Generate FOTA Batch CSV",
            command=lambda: self._run_async(self._action_fota_batch),
        ).grid(row=3, column=2, sticky="ew", padx=4, pady=(10, 4))
        ttk.Button(
            generation_frame,
            text="Generate Ticket CSV",
            command=lambda: self._run_async(self._action_ticket_csv),
        ).grid(row=3, column=3, sticky="ew", padx=4, pady=(10, 4))

        for index in range(4):
            generation_frame.columnconfigure(index, weight=1)

        crm_frame = ttk.LabelFrame(root, text="CRM API", padding=10)
        crm_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(crm_frame, text="VIN Start").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(crm_frame, textvariable=self.vin_start_var, width=12).grid(row=0, column=1, sticky="w", padx=4, pady=4)
        ttk.Label(crm_frame, text="VIN End").grid(row=0, column=2, sticky="w", padx=4, pady=4)
        ttk.Entry(crm_frame, textvariable=self.vin_end_var, width=12).grid(row=0, column=3, sticky="w", padx=4, pady=4)
        ttk.Label(crm_frame, text="VIN Prefix").grid(row=0, column=4, sticky="w", padx=4, pady=4)
        ttk.Entry(crm_frame, textvariable=self.vin_prefix_var, width=26).grid(row=0, column=5, sticky="ew", padx=4, pady=4)
        ttk.Button(
            crm_frame,
            text="Send CRM Requests",
            command=lambda: self._run_async(self._action_crm),
        ).grid(row=0, column=6, sticky="ew", padx=4, pady=4)
        crm_frame.columnconfigure(5, weight=1)

        log_frame = ttk.LabelFrame(root, text="Execution Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_text = tk.Text(log_frame, height=14, wrap="word", state=tk.DISABLED)
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
        vin_start = self._get_positive_int(self.vin_start_var.get(), "VIN Start")
        vin_end = self._get_positive_int(self.vin_end_var.get(), "VIN End")
        if vin_end < vin_start:
            raise ValueError("VIN End must be greater than or equal to VIN Start.")
        responses = send_ticket_generation_requests(
            vin_start=vin_start,
            vin_end=vin_end,
            vin_prefix=self.vin_prefix_var.get().strip() or "SURAJ07082025_",
        )
        return f"CRM calls completed: {len(responses)} requests."


def main() -> int:
    app = VDGDesktopApp()
    app.mainloop()
    return 0
