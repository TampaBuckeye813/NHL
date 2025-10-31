# NHL Game Predictor

A Windows desktop application that predicts NHL game outcomes using advanced statistical analysis. Input Massey ratings, Natural Stat Trick data, and other key metrics to get probability-based predictions with confidence scores.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## Features

- **Comprehensive Statistical Model**: Weighted prediction algorithm using 9 key factors
- **User-Friendly GUI**: Clean interface with organized form inputs
- **File Import**: View Excel/CSV files containing your stats
- **PDF Export**: Professional PDF reports of your predictions
- **Local Storage**: Automatically saves all predictions
- **Single-Click Executable**: No installation required - just run the .exe

## Prediction Factors & Weights

The prediction model uses the following weighted factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Massey Ratings** | 25% | Comprehensive power rankings |
| **Expected Goals (xG%)** | 20% | Quality scoring chances from Natural Stat Trick |
| **High-Danger Chances** | 15% | Premium scoring opportunities |
| **Goalie Matchup** | 15% | Save percentage and GAA comparison |
| **Recent Form** | 10% | Last 10 games performance |
| **Home Ice Advantage** | 5% | Historical home team advantage |
| **Special Teams** | 5% | Power Play and Penalty Kill efficiency |
| **Rest Factor** | 3% | Days since last game (fatigue) |
| **Injury Impact** | 2% | Key player availability |

## Installation & Setup

### Option 1: Use Pre-Built Executable (Easiest)

1. Download `NHL_Game_Predictor.exe` from the releases
2. Double-click to run - no installation needed!
3. The app will create necessary folders automatically

### Option 2: Build From Source

**Requirements:**
- Windows 10/11
- Python 3.8 or higher
- pip (Python package manager)

**Steps:**

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/yourusername/NHL.git
   cd NHL
   ```

2. **Run the build script**
   ```bash
   python build.py
   ```
   Or on Windows:
   ```bash
   build.bat
   ```

3. **Find your executable**
   - Look in the `dist` folder
   - Copy `NHL_Game_Predictor.exe` anywhere you want
   - Double-click to run!

## How to Use

### 1. Enter Team Information

Fill out the form with data for both teams:

- **Team Names**: Home and away team
- **Massey Ratings**: Get from Massey Ratings website
- **Natural Stat Trick Stats**:
  - xG% (Expected Goals %)
  - HD% (High-Danger Chances %)
  - Corsi%
  - Fenwick%
- **Recent Form**: W-L record from last 10 games
- **Goalie Stats**: Save % and GAA for starting goalies
- **Special Teams**: Power Play % and Penalty Kill %
- **Rest**: Days since each team's last game
- **Injuries**: Rate impact from 0 (no injuries) to 10 (severe)

### 2. Optional: Import Reference Data

- Click **"Import Excel/CSV"** to view spreadsheets
- File contents appear in the viewer panel
- Use this to reference your stats while filling the form
- The import does NOT auto-fill the form (by design)

### 3. Generate Prediction

- Click **"Generate Prediction"**
- Results appear instantly in the results panel
- Shows:
  - Predicted winner
  - Win probability for each team
  - Confidence level (Very High, High, Moderate, Low, Very Low)

### 4. Export to PDF

- Click **"Export to PDF"** after generating a prediction
- Professional report is saved to `predictions` folder
- Includes all input data and prediction results

### 5. Make Another Prediction

- Click **"Clear Form"** to reset all fields
- Enter new game data
- Repeat!

## Data Sources

### Recommended Sources

1. **Massey Ratings**: [https://www.masseyratings.com/nhl/games](https://www.masseyratings.com/nhl/games)
2. **Natural Stat Trick**: [https://www.naturalstattrick.com](https://www.naturalstattrick.com)
   - Team stats for current season
   - Filter by "5v5" or "All Situations"
3. **NHL.com**: Official stats for goalies, special teams, standings
4. **ESPN/The Athletic**: Injury reports and lineup updates

### Tips for Data Entry

- Use **season-to-date** percentages for most accurate predictions
- For recent form, use the **last 10 games** only
- Update goalie stats before each prediction (they change frequently)
- Injury impact: Consider both quantity and quality of missing players
  - 0-2: Minor injuries (depth players)
  - 3-5: Notable injuries (middle-six forwards, bottom-pair D)
  - 6-8: Significant injuries (top-6 forwards, top-4 D)
  - 9-10: Star players out (elite forwards, #1 D, starting goalie)

## Output Files

The application creates these folders automatically:

```
NHL_Game_Predictor.exe
├── data/
│   └── predictions.json       # All predictions saved here
└── predictions/
    └── [Team]_vs_[Team]_[timestamp].pdf  # Exported PDFs
```

## Understanding Predictions

### Confidence Levels

- **Very High (20%+ difference)**: Strong pick
- **High (15-20% difference)**: Solid favorite
- **Moderate (10-15% difference)**: Clear edge
- **Low (5-10% difference)**: Slight favorite
- **Very Low (<5% difference)**: Toss-up game

### Example Interpretation

```
Predicted Winner: Toronto Maple Leafs
Toronto: 62.3%
Boston: 37.7%
Confidence: 24.6% (Very High)
```

This means the model strongly favors Toronto with a 62.3% chance to win. The 24.6% confidence differential indicates high certainty in the prediction.

## Troubleshooting

### The .exe won't run

- Make sure you have Windows 10 or 11
- Right-click → Properties → Unblock (if file came from internet)
- Run as Administrator if needed

### "Missing teams" warning

- Both home and away team names are required
- Enter team names before generating prediction

### PDF export fails

- Check that you've generated a prediction first
- Ensure the application has write permissions
- The `predictions` folder will be created automatically

### File import doesn't work

- Supported formats: .xlsx, .xls, .csv only
- Check that the file isn't open in Excel
- File is for viewing only - doesn't auto-fill form

## Project Structure

```
NHL/
├── src/
│   ├── main.py              # Main GUI application
│   ├── predictor.py         # Prediction engine
│   ├── file_handler.py      # File import/export
│   └── pdf_generator.py     # PDF report generation
├── data/                    # Prediction storage
├── predictions/             # PDF exports
├── requirements.txt         # Python dependencies
├── build.py                 # Build script (Python)
├── build.bat               # Build script (Windows)
└── README.md               # This file
```

## Technical Details

**Built with:**
- Python 3.x
- Tkinter (GUI framework)
- pandas (data handling)
- reportlab (PDF generation)
- PyInstaller (executable packaging)

**Model Details:**
- Point-based weighted system
- Normalized scores across all factors
- Probability conversion using relative scoring
- Confidence calculated from probability differential

## Future Enhancements

Potential features for future versions:

- [ ] Historical accuracy tracking
- [ ] Team head-to-head database
- [ ] Batch prediction mode (multiple games)
- [ ] Custom weight adjustment
- [ ] Live data fetching from APIs
- [ ] Over/under predictions
- [ ] Season-long record tracking

## Support

For issues, questions, or suggestions:

1. Check the Troubleshooting section above
2. Review the How to Use guide
3. Open an issue on GitHub

## License

This project is provided as-is for personal use. Feel free to modify and customize for your own needs.

## Acknowledgments

- Massey Ratings for power ranking system
- Natural Stat Trick for advanced analytics
- The hockey analytics community

---

**Built for hockey fans who love data-driven predictions!** 🏒📊
