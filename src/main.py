"""
NHL Game Predictor - Main GUI Application
Single-click .exe for Windows desktop
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os
from datetime import datetime

# Import our modules
from predictor import NHLPredictor
from file_handler import FileHandler
from pdf_generator import PDFGenerator


class NHLPredictorGUI:
    """Main GUI Application"""

    def __init__(self, root):
        self.root = root
        self.root.title("NHL Game Predictor")
        self.root.geometry("1200x900")
        self.root.configure(bg='#f0f0f0')

        # Initialize backend
        self.predictor = NHLPredictor()
        self.file_handler = FileHandler()
        self.pdf_generator = PDFGenerator()

        # Variables for form inputs
        self.init_variables()

        # Create UI
        self.create_ui()

        # Imported data storage
        self.imported_data = None

    def init_variables(self):
        """Initialize all form variables"""
        # Team names
        self.home_team = tk.StringVar()
        self.away_team = tk.StringVar()

        # Massey ratings
        self.home_massey = tk.DoubleVar(value=50.0)
        self.away_massey = tk.DoubleVar(value=50.0)

        # Natural Stat Trick - Advanced metrics
        self.home_xg_pct = tk.DoubleVar(value=50.0)
        self.away_xg_pct = tk.DoubleVar(value=50.0)
        self.home_hd_pct = tk.DoubleVar(value=50.0)
        self.away_hd_pct = tk.DoubleVar(value=50.0)
        self.home_corsi_pct = tk.DoubleVar(value=50.0)
        self.away_corsi_pct = tk.DoubleVar(value=50.0)
        self.home_fenwick_pct = tk.DoubleVar(value=50.0)
        self.away_fenwick_pct = tk.DoubleVar(value=50.0)

        # Recent form (last 10 games)
        self.home_last10_wins = tk.IntVar(value=5)
        self.home_last10_losses = tk.IntVar(value=5)
        self.away_last10_wins = tk.IntVar(value=5)
        self.away_last10_losses = tk.IntVar(value=5)

        # Goalie stats
        self.home_goalie_sv_pct = tk.DoubleVar(value=0.910)
        self.home_goalie_gaa = tk.DoubleVar(value=2.75)
        self.away_goalie_sv_pct = tk.DoubleVar(value=0.910)
        self.away_goalie_gaa = tk.DoubleVar(value=2.75)

        # Special teams
        self.home_pp_pct = tk.DoubleVar(value=20.0)
        self.home_pk_pct = tk.DoubleVar(value=80.0)
        self.away_pp_pct = tk.DoubleVar(value=20.0)
        self.away_pk_pct = tk.DoubleVar(value=80.0)

        # Other factors
        self.home_days_rest = tk.IntVar(value=1)
        self.away_days_rest = tk.IntVar(value=1)
        self.home_injury_impact = tk.IntVar(value=0)
        self.away_injury_impact = tk.IntVar(value=0)

    def create_ui(self):
        """Create the main user interface"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = tk.Label(
            main_frame,
            text="NHL Game Predictor",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#003366'
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Left panel - Input form
        left_panel = ttk.LabelFrame(main_frame, text="Game Input", padding="10")
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        # Right panel - File viewer and results
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        # Create scrollable form
        self.create_input_form(left_panel)

        # Create file viewer
        self.create_file_viewer(right_panel)

        # Create results display
        self.create_results_display(right_panel)

        # Action buttons at bottom
        self.create_action_buttons(main_frame)

        # Configure grid weights
        main_frame.rowconfigure(1, weight=1)

    def create_input_form(self, parent):
        """Create the input form with all fields"""
        # Create canvas with scrollbar
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        row = 0

        # Team Names Section
        self.create_section_header(scrollable_frame, "Teams", row)
        row += 1

        ttk.Label(scrollable_frame, text="Home Team:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_team, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away Team:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_team, width=25).grid(row=row, column=1, pady=5)
        row += 1

        # Massey Ratings
        self.create_section_header(scrollable_frame, "Massey Ratings", row)
        row += 1

        ttk.Label(scrollable_frame, text="Home Massey:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_massey, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away Massey:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_massey, width=25).grid(row=row, column=1, pady=5)
        row += 1

        # Natural Stat Trick metrics
        self.create_section_header(scrollable_frame, "Natural Stat Trick - Advanced Stats", row)
        row += 1

        # Expected Goals %
        ttk.Label(scrollable_frame, text="Home xG %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_xg_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away xG %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_xg_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        # High-Danger %
        ttk.Label(scrollable_frame, text="Home HD Chances %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_hd_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away HD Chances %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_hd_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        # Corsi %
        ttk.Label(scrollable_frame, text="Home Corsi %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_corsi_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away Corsi %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_corsi_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        # Fenwick %
        ttk.Label(scrollable_frame, text="Home Fenwick %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_fenwick_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away Fenwick %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_fenwick_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        # Recent Form
        self.create_section_header(scrollable_frame, "Recent Form (Last 10 Games)", row)
        row += 1

        ttk.Label(scrollable_frame, text="Home Wins:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_last10_wins, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Home Losses:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_last10_losses, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away Wins:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_last10_wins, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away Losses:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_last10_losses, width=25).grid(row=row, column=1, pady=5)
        row += 1

        # Goalie Stats
        self.create_section_header(scrollable_frame, "Goalie Statistics", row)
        row += 1

        ttk.Label(scrollable_frame, text="Home Goalie Sv%:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_goalie_sv_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Home Goalie GAA:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_goalie_gaa, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away Goalie Sv%:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_goalie_sv_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away Goalie GAA:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_goalie_gaa, width=25).grid(row=row, column=1, pady=5)
        row += 1

        # Special Teams
        self.create_section_header(scrollable_frame, "Special Teams", row)
        row += 1

        ttk.Label(scrollable_frame, text="Home PP %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_pp_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Home PK %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_pk_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away PP %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_pp_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away PK %:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_pk_pct, width=25).grid(row=row, column=1, pady=5)
        row += 1

        # Other Factors
        self.create_section_header(scrollable_frame, "Other Factors", row)
        row += 1

        ttk.Label(scrollable_frame, text="Home Days Rest:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_days_rest, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away Days Rest:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_days_rest, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Home Injury Impact (0-10):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.home_injury_impact, width=25).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Away Injury Impact (0-10):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.away_injury_impact, width=25).grid(row=row, column=1, pady=5)
        row += 1

    def create_section_header(self, parent, text, row):
        """Create a section header"""
        header = tk.Label(
            parent,
            text=text,
            font=('Arial', 11, 'bold'),
            bg='#003366',
            fg='white',
            pady=5
        )
        header.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 5))

    def create_file_viewer(self, parent):
        """Create file import viewer"""
        viewer_frame = ttk.LabelFrame(parent, text="File Viewer", padding="10")
        viewer_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Import button
        import_btn = ttk.Button(
            viewer_frame,
            text="Import Excel/CSV",
            command=self.import_file
        )
        import_btn.pack(pady=(0, 10))

        # Text widget for displaying file contents
        self.file_viewer_text = scrolledtext.ScrolledText(
            viewer_frame,
            height=15,
            wrap=tk.WORD,
            font=('Courier', 9)
        )
        self.file_viewer_text.pack(fill=tk.BOTH, expand=True)
        self.file_viewer_text.insert(tk.END, "No file imported yet.\n\nClick 'Import Excel/CSV' to view file contents.")
        self.file_viewer_text.config(state=tk.DISABLED)

    def create_results_display(self, parent):
        """Create prediction results display"""
        results_frame = ttk.LabelFrame(parent, text="Prediction Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)

        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.insert(tk.END, "Prediction results will appear here after you click 'Generate Prediction'.")
        self.results_text.config(state=tk.DISABLED)

    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        # Predict button
        predict_btn = tk.Button(
            button_frame,
            text="Generate Prediction",
            command=self.generate_prediction,
            bg='#003366',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        )
        predict_btn.pack(side=tk.LEFT, padx=10)

        # Export PDF button
        export_btn = ttk.Button(
            button_frame,
            text="Export to PDF",
            command=self.export_to_pdf
        )
        export_btn.pack(side=tk.LEFT, padx=10)

        # Clear button
        clear_btn = ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form
        )
        clear_btn.pack(side=tk.LEFT, padx=10)

    def import_file(self):
        """Import Excel or CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                df = self.file_handler.import_file(file_path)
                self.imported_data = df

                # Display in viewer
                self.file_viewer_text.config(state=tk.NORMAL)
                self.file_viewer_text.delete(1.0, tk.END)
                self.file_viewer_text.insert(tk.END, f"File: {os.path.basename(file_path)}\n")
                self.file_viewer_text.insert(tk.END, "=" * 60 + "\n\n")
                self.file_viewer_text.insert(tk.END, df.to_string())
                self.file_viewer_text.config(state=tk.DISABLED)

                messagebox.showinfo("Success", "File imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import file:\n{str(e)}")

    def generate_prediction(self):
        """Generate prediction based on form inputs"""
        try:
            # Validate inputs
            if not self.home_team.get() or not self.away_team.get():
                messagebox.showwarning("Missing Data", "Please enter both team names.")
                return

            # Gather all game data
            game_data = {
                'home_team': self.home_team.get(),
                'away_team': self.away_team.get(),
                'home_massey': self.home_massey.get(),
                'away_massey': self.away_massey.get(),
                'home_xg_pct': self.home_xg_pct.get(),
                'away_xg_pct': self.away_xg_pct.get(),
                'home_hd_pct': self.home_hd_pct.get(),
                'away_hd_pct': self.away_hd_pct.get(),
                'home_corsi_pct': self.home_corsi_pct.get(),
                'away_corsi_pct': self.away_corsi_pct.get(),
                'home_fenwick_pct': self.home_fenwick_pct.get(),
                'away_fenwick_pct': self.away_fenwick_pct.get(),
                'home_last10_wins': self.home_last10_wins.get(),
                'home_last10_losses': self.home_last10_losses.get(),
                'away_last10_wins': self.away_last10_wins.get(),
                'away_last10_losses': self.away_last10_losses.get(),
                'home_goalie_sv_pct': self.home_goalie_sv_pct.get(),
                'home_goalie_gaa': self.home_goalie_gaa.get(),
                'away_goalie_sv_pct': self.away_goalie_sv_pct.get(),
                'away_goalie_gaa': self.away_goalie_gaa.get(),
                'home_pp_pct': self.home_pp_pct.get(),
                'home_pk_pct': self.home_pk_pct.get(),
                'away_pp_pct': self.away_pp_pct.get(),
                'away_pk_pct': self.away_pk_pct.get(),
                'home_days_rest': self.home_days_rest.get(),
                'away_days_rest': self.away_days_rest.get(),
                'home_injury_impact': self.home_injury_impact.get(),
                'away_injury_impact': self.away_injury_impact.get(),
            }

            # Generate prediction
            prediction = self.predictor.predict_game(game_data)

            # Store for export
            self.current_prediction = prediction
            self.current_game_data = game_data

            # Save to file
            self.file_handler.save_prediction(prediction)

            # Display results
            self.display_results(prediction)

            messagebox.showinfo("Success", "Prediction generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate prediction:\n{str(e)}")

    def display_results(self, prediction):
        """Display prediction results"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        # Header
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, f"  {prediction['home_team']} vs {prediction['away_team']}\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")

        # Prediction
        self.results_text.insert(tk.END, "PREDICTED WINNER:\n", "header")
        self.results_text.insert(tk.END, f"  {prediction['predicted_winner']}\n\n", "winner")

        # Probabilities
        self.results_text.insert(tk.END, "WIN PROBABILITIES:\n", "header")
        self.results_text.insert(tk.END, f"  {prediction['home_team']}: {prediction['home_probability']:.1f}%\n")
        self.results_text.insert(tk.END, f"  {prediction['away_team']}: {prediction['away_probability']:.1f}%\n\n")

        # Confidence
        self.results_text.insert(tk.END, "CONFIDENCE:\n", "header")
        self.results_text.insert(tk.END, f"  {prediction['confidence']:.1f}% ({prediction['confidence_level']})\n\n")

        # Explanation
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, "Model Weights:\n")
        self.results_text.insert(tk.END, "  • Massey Ratings: 25%\n")
        self.results_text.insert(tk.END, "  • Expected Goals: 20%\n")
        self.results_text.insert(tk.END, "  • High-Danger Chances: 15%\n")
        self.results_text.insert(tk.END, "  • Goalie Matchup: 15%\n")
        self.results_text.insert(tk.END, "  • Recent Form: 10%\n")
        self.results_text.insert(tk.END, "  • Home Ice: 5%\n")
        self.results_text.insert(tk.END, "  • Special Teams: 5%\n")
        self.results_text.insert(tk.END, "  • Rest Factor: 3%\n")
        self.results_text.insert(tk.END, "  • Injuries: 2%\n")

        # Configure tags
        self.results_text.tag_config("header", font=('Arial', 11, 'bold'))
        self.results_text.tag_config("winner", font=('Arial', 14, 'bold'), foreground='#003366')

        self.results_text.config(state=tk.DISABLED)

    def export_to_pdf(self):
        """Export current prediction to PDF"""
        if not hasattr(self, 'current_prediction'):
            messagebox.showwarning("No Prediction", "Please generate a prediction first.")
            return

        try:
            pdf_path = self.pdf_generator.generate_prediction_pdf(
                self.current_prediction,
                self.current_game_data
            )
            messagebox.showinfo(
                "Success",
                f"PDF exported successfully!\n\nSaved to:\n{pdf_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF:\n{str(e)}")

    def clear_form(self):
        """Clear all form inputs"""
        response = messagebox.askyesno("Clear Form", "Are you sure you want to clear all inputs?")
        if response:
            self.init_variables()
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Form cleared. Enter new game data.")
            self.results_text.config(state=tk.DISABLED)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = NHLPredictorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
