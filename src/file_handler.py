"""
File handling for NHL Predictor
Imports Excel/CSV files and exports predictions to PDF
"""

import json
import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime
import os


class FileHandler:
    """Handles file imports and exports"""

    def __init__(self, predictions_file: str = "data/predictions.json"):
        self.predictions_file = predictions_file
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.predictions_file), exist_ok=True)

    def import_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Import Excel or CSV file

        Args:
            file_path: Path to the file

        Returns:
            DataFrame with file contents or None if error
        """
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Use CSV or Excel files.")

            return df
        except Exception as e:
            raise Exception(f"Error importing file: {str(e)}")

    def save_prediction(self, prediction: Dict) -> bool:
        """
        Save prediction to local JSON file

        Args:
            prediction: Prediction dictionary

        Returns:
            True if successful
        """
        try:
            # Load existing predictions
            predictions = self.load_all_predictions()

            # Add new prediction
            predictions.append(prediction)

            # Save back to file
            with open(self.predictions_file, 'w') as f:
                json.dump(predictions, f, indent=2)

            return True
        except Exception as e:
            raise Exception(f"Error saving prediction: {str(e)}")

    def load_all_predictions(self) -> List[Dict]:
        """
        Load all predictions from file

        Returns:
            List of prediction dictionaries
        """
        if not os.path.exists(self.predictions_file):
            return []

        try:
            with open(self.predictions_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []

    def get_latest_prediction(self) -> Optional[Dict]:
        """Get the most recent prediction"""
        predictions = self.load_all_predictions()
        return predictions[-1] if predictions else None

    def get_prediction_stats(self) -> Dict:
        """
        Get statistics about all predictions

        Returns:
            Dictionary with stats
        """
        predictions = self.load_all_predictions()

        if not predictions:
            return {
                'total_predictions': 0,
                'average_confidence': 0
            }

        confidences = [p['confidence'] for p in predictions]

        return {
            'total_predictions': len(predictions),
            'average_confidence': sum(confidences) / len(confidences),
            'high_confidence_picks': len([c for c in confidences if c >= 15]),
            'toss_ups': len([c for c in confidences if c < 5])
        }
