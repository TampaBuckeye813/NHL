# Quick Start Guide - NHL Game Predictor

## First Time Setup

### If You Have the .exe File:
1. Copy `NHL_Game_Predictor.exe` to your desktop or any folder
2. Double-click to run
3. That's it! The app creates all necessary folders automatically

### If You're Building From Source:
1. Make sure Python 3.8+ is installed
2. Open Command Prompt in the project folder
3. Run: `python build.py`
4. Find the .exe in the `dist` folder
5. Copy it anywhere and run!

## Making Your First Prediction

### Step 1: Gather Your Data
Before opening the app, collect these stats from your sources:

**From Massey Ratings** (masseyratings.com/nhl):
- Power ratings for both teams

**From Natural Stat Trick** (naturalstattrick.com):
- Expected Goals % (xG%)
- High-Danger Chances % (HD%)
- Corsi %
- Fenwick %

**From NHL.com or ESPN**:
- Last 10 games record (W-L)
- Starting goalie Save % and GAA
- Power Play %
- Penalty Kill %
- Days since last game
- Injury information

### Step 2: Open the App
Double-click `NHL_Game_Predictor.exe`

### Step 3: Fill Out the Form

**Teams Section:**
- Home Team: Enter the home team name
- Away Team: Enter the away team name

**Massey Ratings:**
- Enter the numerical ratings for each team

**Natural Stat Trick Stats:**
- Enter percentages as numbers (e.g., 52.5 for 52.5%)
- xG%, HD%, Corsi%, Fenwick% for both teams

**Recent Form:**
- Wins and losses from last 10 games for each team
- Must add up to 10 (e.g., 6 wins + 4 losses = 10 games)

**Goalie Statistics:**
- Save %: Enter as decimal (e.g., 0.915 for 91.5%)
- GAA: Enter as decimal (e.g., 2.45)

**Special Teams:**
- Enter as percentages (e.g., 22.5 for 22.5%)

**Other Factors:**
- Days Rest: Number of days since last game (0, 1, 2, etc.)
- Injury Impact: Rate from 0-10
  - 0 = No key injuries
  - 5 = Some important players out
  - 10 = Multiple star players out

### Step 4: Generate Prediction
Click the big blue **"Generate Prediction"** button

### Step 5: View Results
The prediction appears in the right panel showing:
- Predicted winner
- Win probability for each team
- Confidence level

### Step 6: Export to PDF (Optional)
Click **"Export to PDF"** to save a professional report

### Step 7: Make Another Prediction
Click **"Clear Form"** and repeat!

## Example: A Real Prediction

Let's predict: **Toronto Maple Leafs (Home) vs. Boston Bruins (Away)**

**Input Example:**
```
Teams:
- Home: Toronto Maple Leafs
- Away: Boston Bruins

Massey Ratings:
- Home: 85.2
- Away: 83.7

Natural Stat Trick (Season stats):
- Home xG%: 52.3
- Away xG%: 47.7
- Home HD%: 51.8
- Away HD%: 48.2
- Home Corsi%: 53.1
- Away Corsi%: 46.9
- Home Fenwick%: 52.8
- Away Fenwick%: 47.2

Recent Form (Last 10):
- Home: 7 wins, 3 losses
- Away: 5 wins, 5 losses

Goalies:
- Home Sv%: 0.918, GAA: 2.35
- Away Sv%: 0.912, GAA: 2.68

Special Teams:
- Home PP%: 24.5, PK%: 82.3
- Away PP%: 21.2, PK%: 79.8

Other:
- Home Rest: 2 days
- Away Rest: 1 day
- Home Injuries: 2
- Away Injuries: 4
```

**Result:**
```
Predicted Winner: Toronto Maple Leafs
Toronto: 58.7%
Boston: 41.3%
Confidence: 17.4% (High)
```

## Tips for Best Results

### Data Quality
- Use **current season** stats whenever possible
- Update goalie stats frequently (they change game-to-game)
- Check injury reports before each prediction

### Percentage Formats
- Most percentages are entered as numbers (52.5, not 0.525)
- Exception: Save % is decimal (0.915, not 91.5)
- When in doubt, check the example in the field

### Understanding Confidence
- **Very High (20%+)**: Strong indicator
- **High (15-20%)**: Solid pick
- **Moderate (10-15%)**: Decent edge
- **Low (5-10%)**: Slight favorite
- **Very Low (<5%)**: True toss-up

### Common Mistakes
❌ Forgetting to enter team names (required!)
❌ Using old/outdated goalie stats
❌ Last 10 games not adding up to 10
❌ Entering Save % as percentage instead of decimal

✅ Current data from reliable sources
✅ Fresh goalie numbers
✅ Recent form = exactly last 10 games
✅ Save % as decimal (0.915)

## File Import Feature

The file viewer is for **reference only**:
1. Click "Import Excel/CSV"
2. Select your stats spreadsheet
3. View the contents in the panel
4. Manually fill the form using those numbers

**Note:** Import does NOT auto-fill the form. This gives you control over what data to use.

## Where Files Are Saved

```
[Location of your .exe]
├── NHL_Game_Predictor.exe
├── data/
│   └── predictions.json         <- All predictions saved here
└── predictions/
    └── Toronto_vs_Boston_20241031_143022.pdf  <- PDF exports
```

## Troubleshooting

**App won't start:**
- Right-click .exe → Properties → Unblock
- Run as Administrator

**Can't export PDF:**
- Make sure you generated a prediction first
- App needs write permissions in its folder

**Import not working:**
- Only .xlsx, .xls, and .csv files supported
- Make sure file isn't open in Excel

## Need More Help?

See the full README.md for:
- Complete feature documentation
- Technical details
- Advanced troubleshooting
- Links to data sources

---

**You're ready to start predicting! Good luck with your picks! 🏒**
