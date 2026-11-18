import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List
from .resizer import ImageResizer


class ImageResizerApp:
    """Modern Tkinter UI for batch image resizing."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modern Image Resizer")
        self.root.geometry("680x560")
        self.root.minsize(600, 500)

        self.selected_files: List[str] = []
        self.output_dir: str = os.path.expanduser("~")

        self._configure_styles()
        self._build_ui()

    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f5f5f7")
        self.style.configure("TLabel", background="#f5f5f7", font=("Helvetica", 10))
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))
        self.style.configure("TButton", font=("Helvetica", 10), padding=6)
        self.style.configure("Accent.TButton", font=("Helvetica", 10, "bold"), background="#007aff", foreground="white")
        self.style.map("Accent.TButton", background=[("active", "#0056b3")])

    def _build_ui(self):
        main_container = ttk.Frame(self.root, padding=15)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Label(main_container, text="Batch Image Resizer", style="Header.TLabel")
        header.pack(anchor=tk.W, pady=(0, 10))

        # File Selection Frame
        file_frame = ttk.LabelFrame(main_container, text=" Files ", padding=10)
        file_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        btn_box = ttk.Frame(file_frame)
        btn_box.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(btn_box, text="Add Images", command=self._add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_box, text="Clear List", command=self._clear_files).pack(side=tk.LEFT)

        self.file_listbox = tk.Listbox(file_frame, height=5, selectmode=tk.EXTENDED, font=("Consolas", 9))
        self.file_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Settings Frame
        settings_frame = ttk.LabelFrame(main_container, text=" Resize Options ", padding=10)
        settings_frame.pack(fill=tk.X, pady=5)

        # Mode Switch
        self.mode_var = tk.StringVar(value="dimensions")
        mode_box = ttk.Frame(settings_frame)
        mode_box.pack(fill=tk.X, pady=2)
        ttk.Radiobutton(mode_box, text="Exact Dimensions", variable=self.mode_var, value="dimensions", command=self._toggle_mode).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(mode_box, text="Scale Percentage", variable=self.mode_var, value="percentage", command=self._toggle_mode).pack(side=tk.LEFT)

        # Dimension Controls
        self.dim_frame = ttk.Frame(settings_frame)
        self.dim_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.dim_frame, text="Width (px):").grid(row=0, column=0, sticky=tk.W, padx=2)
        self.width_entry = ttk.Entry(self.dim_frame, width=8)
        self.width_entry.insert(0, "800")
        self.width_entry.grid(row=0, column=1, padx=(0, 15))

        ttk.Label(self.dim_frame, text="Height (px):").grid(row=0, column=2, sticky=tk.W, padx=2)
        self.height_entry = ttk.Entry(self.dim_frame, width=8)
        self.height_entry.grid(row=0, column=3, padx=(0, 15))

        self.keep_aspect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.dim_frame, text="Keep Aspect Ratio", variable=self.keep_aspect_var).grid(row=0, column=4, padx=5)

        # Percentage Controls
        self.pct_frame = ttk.Frame(settings_frame)
        ttk.Label(self.pct_frame, text="Scale (%):").pack(side=tk.LEFT, padx=2)
        self.pct_entry = ttk.Entry(self.pct_frame, width=8)
        self.pct_entry.insert(0, "50")
        self.pct_frame.pack(fill=tk.X, pady=5)
        self.pct_frame.pack_forget()

        # Output Options
        out_opts_frame = ttk.Frame(settings_frame)
        out_opts_frame.pack(fill=tk.X, pady=5)

        ttk.Label(out_opts_frame, text="Format:").grid(row=0, column=0, sticky=tk.W)
        self.format_combo = ttk.Combobox(out_opts_frame, values=["ORIGINAL", "JPEG", "PNG", "WEBP", "BMP"], state="readonly", width=10)
        self.format_combo.current(0)
        self.format_combo.grid(row=0, column=1, padx=(5, 15))

        ttk.Label(out_opts_frame, text="Quality (1-100):").grid(row=0, column=2, sticky=tk.W)
        self.quality_spin = ttk.Spinbox(out_opts_frame, from_=1, to=100, width=5)
        self.quality_spin.set(85)
        self.quality_spin.grid(row=0, column=3, padx=5)

        # Destination Frame
        dest_frame = ttk.Frame(main_container)
        dest_frame.pack(fill=tk.X, pady=5)
        ttk.Label(dest_frame, text="Output Directory:").pack(anchor=tk.W)
        
        dest_box = ttk.Frame(dest_frame)
        dest_box.pack(fill=tk.X, pady=2)
        self.dest_entry = ttk.Entry(dest_box)
        self.dest_entry.insert(0, self.output_dir)
        self.dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(dest_box, text="Browse...", command=self._browse_output_dir).pack(side=tk.RIGHT)

        # Action Frame
        action_frame = ttk.Frame(main_container)
        action_frame.pack(fill=tk.X, pady=10)

        self.progress_bar = ttk.Progressbar(action_frame, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        self.run_btn = ttk.Button(action_frame, text="Start Resizing", style="Accent.TButton", command=self._start_processing)
        self.run_btn.pack(fill=tk.X)

    def _toggle_mode(self):
        if self.mode_var.get() == "dimensions":
            self.pct_frame.pack_forget()
            self.dim_frame.pack(fill=tk.X, pady=5)
        else:
            self.dim_frame.pack_forget()
            self.pct_frame.pack(fill=tk.X, pady=5)

    def _add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff")]
        )
        for f in files:
            if f not in self.selected_files:
                self.selected_files.append(f)
                self.file_listbox.insert(tk.END, os.path.basename(f))

    def _clear_files(self):
        self.selected_files.clear()
        self.file_listbox.delete(0, tk.END)

    def _browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory", initialdir=self.output_dir)
        if directory:
            self.output_dir = directory
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, self.output_dir)

    def _start_processing(self):
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please add at least one image file.")
            return

        output_dir = self.dest_entry.get().strip()
        if not output_dir:
            messagebox.showwarning("Warning", "Please select a valid output directory.")
            return

        mode = self.mode_var.get()
        target_w, target_h, scale_pct = None, None, None

        try:
            if mode == "dimensions":
                w_str = self.width_entry.get().strip()
                h_str = self.height_entry.get().strip()
                target_w = int(w_str) if w_str else None
                target_h = int(h_str) if h_str else None
                if not target_w and not target_h:
                    raise ValueError("Provide at least Width or Height.")
            else:
                scale_pct = float(self.pct_entry.get().strip())
                if scale_pct <= 0:
                    raise ValueError("Scale percentage must be greater than 0.")
            
            quality = int(self.quality_spin.get())
        except ValueError as err:
            messagebox.showerror("Input Error", f"Invalid parameter: {err}")
            return

        fmt = self.format_combo.get()
        keep_aspect = self.keep_aspect_var.get()

        self.run_btn.config(state=tk.DISABLED)
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = len(self.selected_files)

        def worker():
            def progress_cb(current, total, filepath):
                self.root.after(0, lambda: self._update_progress(current, total))

            try:
                ImageResizer.batch_resize(
                    file_paths=self.selected_files,
                    output_dir=output_dir,
                    target_width=target_w,
                    target_height=target_h,
                    scale_percent=scale_pct,
                    keep_aspect_ratio=keep_aspect,
                    output_format=fmt,
                    quality=quality,
                    progress_callback=progress_cb
                )
                self.root.after(0, lambda: messagebox.showinfo("Success", f"Successfully resized {len(self.selected_files)} images!"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {e}"))
            finally:
                self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))

        threading.Thread(target=worker, daemon=True).start()

    def _update_progress(self, current, total):
        self.progress_bar["value"] = current

    def run(self):
        self.root.mainloop()
