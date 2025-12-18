import threading
import customtkinter as ctk
from api_handler import GeminiHandler
from anki_handler import AnkiHandler

# --- Senior UI Design System ---
DESIGN_TOKENS = {
    "colors": {
        "bg_root": "#0F172A",        # Rich Navy
        "bg_surface": "#1E293B",     # Surface Slate
        "border": "#334155",         # Border Slate
        "primary": "#F59E0B",        # Amber Gold
        "primary_hover": "#D97706",  # Darker Amber
        "text_main": "#F1F5F9",      # Slate 100 (White-ish)
        "text_muted": "#94A3B8",     # Slate 400
        "text_on_primary": "#0F172A",# Dark text on amber
        "success": "#10B981",        # Emerald
        "error": "#EF4444",          # Red
        "close_hover": "#EF4444"
    },
    "typography": {
        "family": "Segoe UI",       # Reliable Windows fallback for Inter
        "header_size": 20,
        "main_size": 13,
        "small_size": 11
    },
    "metrics": {
        "radius": 14,
        "border_width": 1,
        "pad_x_outer": 25,
        "pad_y_outer": 20
    }
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LA")
        self.geometry("450x550")
        self.overrideredirect(True) # Frameless
        self.attributes("-topmost", True)
        self.configure(fg_color=DESIGN_TOKENS["colors"]["bg_root"])

        # Drag variables
        self.x_offset = 0
        self.y_offset = 0

        # Handlers
        try:
            self.api = GeminiHandler()
            self.anki = AnkiHandler()
        except Exception as e:
            print(f"Init Error: {e}")
            self.api = None
            self.anki = None

        self.current_data = None
        self.create_widgets()
        self.check_initial_connection()

    def create_widgets(self):
        # Grid Setup
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Preview takes available space

        # --- 1. Custom Title Bar ---
        self.title_bar = ctk.CTkFrame(
            self, 
            fg_color="transparent", 
            corner_radius=0, 
            height=44
        )
        self.title_bar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.title_bar.grid_columnconfigure(1, weight=1)

        self.title_bar.bind("<Button-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.do_drag)

        # Brand Logo
        logo_label = ctk.CTkLabel(
            self.title_bar,
            text="LA",
            # Increased letter spacing simulated by font choice/sizing context if possible,
            # but standard Tkinter font tuple handles size/weight mainly.
            font=(DESIGN_TOKENS["typography"]["family"], DESIGN_TOKENS["typography"]["header_size"], "bold"),
            text_color=DESIGN_TOKENS["colors"]["primary"]
        )
        logo_label.grid(row=0, column=0, padx=20) # Increased padding
        logo_label.bind("<Button-1>", self.start_drag)

        # Drag Handle (spacer)
        drag_handle = ctk.CTkLabel(self.title_bar, text="", cursor="fleur")
        drag_handle.grid(row=0, column=1, sticky="ew")
        drag_handle.bind("<Button-1>", self.start_drag)
        drag_handle.bind("<B1-Motion>", self.do_drag)

        # Close Button
        close_btn = ctk.CTkButton(
            self.title_bar,
            text="✕",
            width=32,
            height=32,
            fg_color="transparent",
            text_color=DESIGN_TOKENS["colors"]["text_muted"],
            hover_color=DESIGN_TOKENS["colors"]["close_hover"],
            command=self.destroy,
            font=("Arial", 14),
            corner_radius=8
        )
        close_btn.grid(row=0, column=2, padx=20)

        # --- 2. Input Field ---
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Kelimeyi giriniz...",
            placeholder_text_color=DESIGN_TOKENS["colors"]["text_muted"],
            font=(DESIGN_TOKENS["typography"]["family"], DESIGN_TOKENS["typography"]["main_size"]),
            fg_color=DESIGN_TOKENS["colors"]["bg_surface"],
            text_color=DESIGN_TOKENS["colors"]["text_main"],
            border_color=DESIGN_TOKENS["colors"]["border"],
            border_width=DESIGN_TOKENS["metrics"]["border_width"],
            corner_radius=DESIGN_TOKENS["metrics"]["radius"],
            height=48
        )
        self.entry.grid(
            row=1, 
            column=0, 
            padx=DESIGN_TOKENS["metrics"]["pad_x_outer"], 
            pady=(10, 16), 
            sticky="ew"
        )
        self.entry.bind("<Return>", lambda event: self.start_search())

        # --- 3. Preview Area (Glass-like Depth) ---
        self.preview_text = ctk.CTkTextbox(
            self,
            wrap="word",
            font=(DESIGN_TOKENS["typography"]["family"], DESIGN_TOKENS["typography"]["main_size"]),
            fg_color=DESIGN_TOKENS["colors"]["bg_surface"],
            text_color=DESIGN_TOKENS["colors"]["text_main"],
            border_color=DESIGN_TOKENS["colors"]["border"],
            border_width=DESIGN_TOKENS["metrics"]["border_width"],
            corner_radius=DESIGN_TOKENS["metrics"]["radius"]
        )
        self.preview_text.grid(
            row=3, 
            column=0, 
            padx=DESIGN_TOKENS["metrics"]["pad_x_outer"], 
            pady=0, 
            sticky="nsew"
        )
        self.preview_text.configure(state="disabled")

        # --- 4. Status Bar ---
        self.status_label = ctk.CTkLabel(
            self,
            text="Hazır",
            font=(DESIGN_TOKENS["typography"]["family"], DESIGN_TOKENS["typography"]["small_size"]),
            text_color=DESIGN_TOKENS["colors"]["text_muted"]
        )
        self.status_label.grid(
            row=4, 
            column=0, 
            padx=DESIGN_TOKENS["metrics"]["pad_x_outer"], 
            pady=(12, 4), 
            sticky="w"
        )

        # --- 5. Action Buttons (Primary vs Ghost) ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(
            row=5, 
            column=0, 
            padx=DESIGN_TOKENS["metrics"]["pad_x_outer"], 
            pady=(10, 30), 
            sticky="ew"
        )
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        # Primary Button: Search
        self.search_btn = ctk.CTkButton(
            self.button_frame,
            text="Kelimeyi Ara",
            command=self.start_search,
            font=(DESIGN_TOKENS["typography"]["family"], DESIGN_TOKENS["typography"]["main_size"], "bold"),
            fg_color=DESIGN_TOKENS["colors"]["primary"],
            text_color=DESIGN_TOKENS["colors"]["text_on_primary"],
            hover_color=DESIGN_TOKENS["colors"]["primary_hover"],
            corner_radius=DESIGN_TOKENS["metrics"]["radius"],
            height=44
        )
        self.search_btn.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        # Secondary (Ghost) Button: Anki
        self.add_btn = ctk.CTkButton(
            self.button_frame,
            text="Anki'ye Kaydet",
            command=self.add_to_anki,
            font=(DESIGN_TOKENS["typography"]["family"], DESIGN_TOKENS["typography"]["main_size"], "bold"),
            fg_color="transparent",
            text_color=DESIGN_TOKENS["colors"]["primary"],
            border_color=DESIGN_TOKENS["colors"]["primary"],
            border_width=1,
            hover_color=DESIGN_TOKENS["colors"]["bg_surface"], # Slight highlight
            corner_radius=DESIGN_TOKENS["metrics"]["radius"],
            height=44,
            state="disabled"
        )
        self.add_btn.grid(row=0, column=1, padx=(8, 0), sticky="ew")

    # --- Logic ---
    def start_drag(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_drag(self, event):
        x = self.winfo_x() + (event.x - self.x_offset)
        y = self.winfo_y() + (event.y - self.y_offset)
        self.geometry(f"+{x}+{y}")

    def check_initial_connection(self):
        if self.anki and not self.anki.check_connection():
             self.status_label.configure(text="Uyarı: Anki bağlantısı yok.", text_color=DESIGN_TOKENS["colors"]["error"])

    def start_search(self):
        word = self.entry.get().strip()
        if not word: return

        if not self.api:
            self.status_label.configure(text="API anahtarı eksik.", text_color=DESIGN_TOKENS["colors"]["error"])
            return

        self.search_btn.configure(state="disabled")
        self.add_btn.configure(state="disabled")
        self.status_label.configure(text="Aranıyor...", text_color=DESIGN_TOKENS["colors"]["primary"])
        
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.configure(state="disabled")

        threading.Thread(target=self.perform_search, args=(word,), daemon=True).start()

    def perform_search(self, word):
        result = self.api.generate_card_content(word)
        self.after(0, self.update_ui_after_search, result)

    def update_ui_after_search(self, result):
        self.search_btn.configure(state="normal")
        
        if result and "error" in result:
             self.current_data = None
             self.preview_text.configure(state="normal", text_color=DESIGN_TOKENS["colors"]["error"])
             self.preview_text.delete("1.0", "end")
             self.preview_text.insert("1.0", result["error"])
             self.preview_text.configure(state="disabled")
             self.status_label.configure(text="Hata oluştu.", text_color=DESIGN_TOKENS["colors"]["error"])
             self.add_btn.configure(state="disabled")
        elif result:
            self.current_data = result
            text_to_show = f"{result['preview_tr']}"
            
            self.preview_text.configure(state="normal", text_color=DESIGN_TOKENS["colors"]["text_main"])
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", text_to_show)
            self.preview_text.configure(state="disabled")
            
            self.status_label.configure(text="Başarılı.", text_color=DESIGN_TOKENS["colors"]["success"])
            self.add_btn.configure(state="normal")
        else:
            self.current_data = None
            self.status_label.configure(text="Sonuç yok.", text_color=DESIGN_TOKENS["colors"]["error"])

    def add_to_anki(self):
        if not self.current_data or not self.anki: return
        word = self.entry.get().strip()
        
        if not self.anki.check_connection():
            self.status_label.configure(text="Anki kapalı.", text_color=DESIGN_TOKENS["colors"]["error"])
            return
            
        # Re-check deck
        self.anki.create_deck_if_not_exists()
        
        success, msg = self.anki.add_card(
            word=word,
            preview_tr=self.current_data["preview_tr"],
            definition=self.current_data["english_definition"],
            example=self.current_data["example_sentence"],
            synonyms=self.current_data["synonyms"]
        )
        
        if success:
            self.status_label.configure(text="Kaydedildi!", text_color=DESIGN_TOKENS["colors"]["success"])
            self.entry.delete(0, "end")
            self.preview_text.configure(state="normal")
            self.preview_text.delete("1.0", "end")
            self.preview_text.configure(state="disabled")
            self.add_btn.configure(state="disabled")
            self.current_data = None
        else:
            self.status_label.configure(text=f"Anki Hatası: {msg}", text_color=DESIGN_TOKENS["colors"]["error"])

if __name__ == "__main__":
    app = App()
    app.mainloop()
