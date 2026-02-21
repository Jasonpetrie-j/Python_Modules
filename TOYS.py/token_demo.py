import tkinter as tk
from tkinter import ttk
import tiktoken

# --- CONFIGURATION ---
PRICING_MAP = {
    "gpt-4o":        {"input": 2.50,  "output": 10.00},
    "gpt-4o-mini":   {"input": 0.15,  "output": 0.60}, 
    "o1-preview":    {"input": 15.00, "output": 60.00},
}

class TokenAnalyzerGUI(tk.Tk):
    def __init__(self, model_encoding="o200k_base"):
        super().__init__()
        self.title("LLM Token & Cost Analyzer")
        self.geometry("750x500")
        
        # Initialize Tokenizer
        self.encoder = tiktoken.get_encoding(model_encoding)
        
        self._build_ui()

    def _build_ui(self):
        # --- 1. Input Frame ---
        input_frame = tk.LabelFrame(self, text="Payload Input (Paste logs, JSON, or Python snippets here)", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.text_input = tk.Text(input_frame, height=8, wrap="word")
        self.text_input.pack(fill="x", expand=True)
        
        # Button Frame to keep the button centered/styled
        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        analyze_btn = tk.Button(btn_frame, text="Analyze Token Cost", command=self.analyze_text, bg="#0052cc", fg="white", font=("Arial", 10, "bold"))
        analyze_btn.pack(side="right")
        
        self.token_count_label = tk.Label(btn_frame, text="Total Tokens: 0", font=("Arial", 10, "bold"))
        self.token_count_label.pack(side="left")

        # --- 2. Results Frame (Treeview Table) ---
        results_frame = tk.LabelFrame(self, text="Cost Projection (Input Only)", padx=10, pady=10)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Define Treeview columns
        columns = ("Model", "1 Request", "1k Shift Logs", "1M Monthly Logs")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=5)
        
        # Format columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
            
        self.tree.pack(fill="both", expand=True)

    def analyze_text(self):
        # 1. Retrieve text from the Text widget
        raw_text = self.text_input.get("1.0", "end-1c")
        
        if not raw_text.strip():
            self._clear_tree()
            self.token_count_label.config(text="Total Tokens: 0")
            return
            
        # 2. Encode and count
        token_ids = self.encoder.encode(raw_text)
        count = len(token_ids)
        self.token_count_label.config(text=f"Total Tokens: {count:,}")
        
        # 3. Calculate costs and populate table
        self._update_cost_table(count)

    def _update_cost_table(self, token_count):
        self._clear_tree()
        
        volumes = [1, 1_000, 1_000_000]
        
        for model, prices in PRICING_MAP.items():
            # Cost formula: (tokens / 1,000,000) * price per 1M
            base_cost = (token_count / 1_000_000) * prices['input']
            
            row_data = [model]
            for vol in volumes:
                cost = base_cost * vol
                formatted_cost = f"${cost:,.6f}" if cost < 0.01 else f"${cost:,.2f}"
                row_data.append(formatted_cost)
                
            self.tree.insert("", "end", values=row_data)

    def _clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

if __name__ == "__main__":
    app = TokenAnalyzerGUI()
    app.mainloop()