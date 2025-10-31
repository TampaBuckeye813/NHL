"""
PDF Export functionality for NHL Predictor
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import Dict
import os


class PDFGenerator:
    """Generates PDF reports for predictions"""

    def __init__(self, output_dir: str = "predictions"):
        self.output_dir = output_dir
        self._ensure_output_directory()

    def _ensure_output_directory(self):
        """Ensure output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_prediction_pdf(self, prediction: Dict, game_data: Dict) -> str:
        """
        Generate a PDF report for a prediction

        Args:
            prediction: Prediction results
            game_data: Original game input data

        Returns:
            Path to generated PDF file
        """
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prediction['home_team']}_vs_{prediction['away_team']}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12
        )
        normal_style = styles['Normal']

        # Title
        title = Paragraph(f"NHL Game Prediction Report", title_style)
        story.append(title)

        # Matchup
        matchup = Paragraph(
            f"<b>{prediction['home_team']}</b> vs <b>{prediction['away_team']}</b>",
            heading_style
        )
        story.append(matchup)
        story.append(Spacer(1, 0.2 * inch))

        # Prediction Result Box
        winner = prediction['predicted_winner']
        home_prob = prediction['home_probability']
        away_prob = prediction['away_probability']
        confidence = prediction['confidence']
        confidence_level = prediction['confidence_level']

        result_data = [
            ['PREDICTION', ''],
            ['Predicted Winner:', winner],
            ['Win Probability:', f"{max(home_prob, away_prob):.1f}%"],
            ['Confidence:', f"{confidence:.1f}% ({confidence_level})"],
            ['', ''],
            [prediction['home_team'], f"{home_prob:.1f}%"],
            [prediction['away_team'], f"{away_prob:.1f}%"]
        ]

        result_table = Table(result_data, colWidths=[3 * inch, 2 * inch])
        result_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('FONTNAME', (0, 1), (0, 3), 'Helvetica-Bold'),
            ('FONTNAME', (0, 5), (0, 6), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 5), (0, 6), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 5), (-1, 6), colors.HexColor('#f0f0f0')),
        ]))

        story.append(result_table)
        story.append(Spacer(1, 0.3 * inch))

        # Input Data Section
        story.append(Paragraph("Game Data Summary", heading_style))

        input_data = [
            ['TEAM STATISTICS', prediction['home_team'], prediction['away_team']],
            ['Massey Rating', f"{game_data['home_massey']}", f"{game_data['away_massey']}"],
            ['Expected Goals %', f"{game_data['home_xg_pct']:.1f}%", f"{game_data['away_xg_pct']:.1f}%"],
            ['High-Danger %', f"{game_data['home_hd_pct']:.1f}%", f"{game_data['away_hd_pct']:.1f}%"],
            ['Corsi %', f"{game_data.get('home_corsi_pct', 0):.1f}%", f"{game_data.get('away_corsi_pct', 0):.1f}%"],
            ['Recent Form (W-L)', f"{game_data['home_last10_wins']}-{game_data['home_last10_losses']}",
             f"{game_data['away_last10_wins']}-{game_data['away_last10_losses']}"],
            ['', '', ''],
            ['GOALIE STATISTICS', '', ''],
            ['Save %', f"{game_data['home_goalie_sv_pct']:.3f}", f"{game_data['away_goalie_sv_pct']:.3f}"],
            ['GAA', f"{game_data['home_goalie_gaa']:.2f}", f"{game_data['away_goalie_gaa']:.2f}"],
            ['', '', ''],
            ['SPECIAL TEAMS', '', ''],
            ['Power Play %', f"{game_data['home_pp_pct']:.1f}%", f"{game_data['away_pp_pct']:.1f}%"],
            ['Penalty Kill %', f"{game_data['home_pk_pct']:.1f}%", f"{game_data['away_pk_pct']:.1f}%"],
            ['', '', ''],
            ['OTHER FACTORS', '', ''],
            ['Days of Rest', f"{game_data['home_days_rest']}", f"{game_data['away_days_rest']}"],
            ['Injury Impact (0-10)', f"{game_data['home_injury_impact']}", f"{game_data['away_injury_impact']}"],
        ]

        input_table = Table(input_data, colWidths=[2.5 * inch, 1.5 * inch, 1.5 * inch])
        input_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 7), (-1, 7), colors.HexColor('#e6f2ff')),
            ('BACKGROUND', (0, 11), (-1, 11), colors.HexColor('#e6f2ff')),
            ('BACKGROUND', (0, 15), (-1, 15), colors.HexColor('#e6f2ff')),
            ('FONTNAME', (0, 7), (0, 7), 'Helvetica-Bold'),
            ('FONTNAME', (0, 11), (0, 11), 'Helvetica-Bold'),
            ('FONTNAME', (0, 15), (0, 15), 'Helvetica-Bold'),
        ]))

        story.append(input_table)
        story.append(Spacer(1, 0.3 * inch))

        # Model Weights Section
        story.append(Paragraph("Prediction Model Weights", heading_style))

        weights_text = """
        This prediction uses a weighted statistical model combining multiple factors:
        <br/><br/>
        <b>• Massey Ratings (25%):</b> Comprehensive power rankings<br/>
        <b>• Expected Goals (20%):</b> Quality scoring chances<br/>
        <b>• High-Danger Chances (15%):</b> Premium scoring opportunities<br/>
        <b>• Goalie Matchup (15%):</b> Save % and GAA comparison<br/>
        <b>• Recent Form (10%):</b> Last 10 games performance<br/>
        <b>• Home Ice (5%):</b> Historical home advantage<br/>
        <b>• Special Teams (5%):</b> PP and PK efficiency<br/>
        <b>• Rest Factor (3%):</b> Days since last game<br/>
        <b>• Injuries (2%):</b> Impact of key player availability<br/>
        """

        story.append(Paragraph(weights_text, normal_style))
        story.append(Spacer(1, 0.2 * inch))

        # Footer
        footer_text = f"<i>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i>"
        story.append(Paragraph(footer_text, normal_style))

        # Build PDF
        doc.build(story)

        return filepath
