"""
NHL Game Predictor - Weighted Statistical Model
Uses multiple factors to predict game outcomes with probability scores
"""

import math
from datetime import datetime
from typing import Dict, Tuple


class NHLPredictor:
    """
    Weighted prediction model for NHL games
    """

    # Weight distribution (totals 100%)
    WEIGHTS = {
        'massey': 0.25,          # Massey ratings
        'expected_goals': 0.20,   # xG% from Natural Stat Trick
        'high_danger': 0.15,      # High-Danger Chances%
        'goalie': 0.15,           # Goalie matchup
        'recent_form': 0.10,      # Last 10 games
        'home_ice': 0.05,         # Home ice advantage
        'special_teams': 0.05,    # PP% and PK%
        'rest': 0.03,             # Days of rest
        'injuries': 0.02,         # Injury impact
    }

    def __init__(self):
        self.prediction_history = []

    def predict_game(self, game_data: Dict) -> Dict:
        """
        Main prediction function

        Args:
            game_data: Dictionary containing all game inputs

        Returns:
            Dictionary with prediction results and probabilities
        """
        home_team = game_data['home_team']
        away_team = game_data['away_team']

        # Calculate score for each factor
        home_score = 0
        away_score = 0
        factor_breakdown = {}

        # 1. Massey Ratings (25%)
        massey_home, massey_away = self._calculate_massey(
            game_data['home_massey'],
            game_data['away_massey']
        )
        home_score += massey_home * self.WEIGHTS['massey']
        away_score += massey_away * self.WEIGHTS['massey']
        factor_breakdown['massey'] = {'home': massey_home, 'away': massey_away}

        # 2. Expected Goals % (20%)
        xg_home, xg_away = self._calculate_xg(
            game_data['home_xg_pct'],
            game_data['away_xg_pct']
        )
        home_score += xg_home * self.WEIGHTS['expected_goals']
        away_score += xg_away * self.WEIGHTS['expected_goals']
        factor_breakdown['xg'] = {'home': xg_home, 'away': xg_away}

        # 3. High-Danger Chances % (15%)
        hd_home, hd_away = self._calculate_high_danger(
            game_data['home_hd_pct'],
            game_data['away_hd_pct']
        )
        home_score += hd_home * self.WEIGHTS['high_danger']
        away_score += hd_away * self.WEIGHTS['high_danger']
        factor_breakdown['high_danger'] = {'home': hd_home, 'away': hd_away}

        # 4. Goalie Matchup (15%)
        goalie_home, goalie_away = self._calculate_goalie(
            game_data['home_goalie_sv_pct'],
            game_data['home_goalie_gaa'],
            game_data['away_goalie_sv_pct'],
            game_data['away_goalie_gaa']
        )
        home_score += goalie_home * self.WEIGHTS['goalie']
        away_score += goalie_away * self.WEIGHTS['goalie']
        factor_breakdown['goalie'] = {'home': goalie_home, 'away': goalie_away}

        # 5. Recent Form (10%)
        form_home, form_away = self._calculate_recent_form(
            game_data['home_last10_wins'],
            game_data['home_last10_losses'],
            game_data['away_last10_wins'],
            game_data['away_last10_losses']
        )
        home_score += form_home * self.WEIGHTS['recent_form']
        away_score += form_away * self.WEIGHTS['recent_form']
        factor_breakdown['recent_form'] = {'home': form_home, 'away': form_away}

        # 6. Home Ice Advantage (5%)
        home_ice = self._calculate_home_ice()
        home_score += home_ice * self.WEIGHTS['home_ice']
        factor_breakdown['home_ice'] = {'home': home_ice, 'away': 0}

        # 7. Special Teams (5%)
        st_home, st_away = self._calculate_special_teams(
            game_data['home_pp_pct'],
            game_data['home_pk_pct'],
            game_data['away_pp_pct'],
            game_data['away_pk_pct']
        )
        home_score += st_home * self.WEIGHTS['special_teams']
        away_score += st_away * self.WEIGHTS['special_teams']
        factor_breakdown['special_teams'] = {'home': st_home, 'away': st_away}

        # 8. Rest Factor (3%)
        rest_home, rest_away = self._calculate_rest(
            game_data['home_days_rest'],
            game_data['away_days_rest']
        )
        home_score += rest_home * self.WEIGHTS['rest']
        away_score += rest_away * self.WEIGHTS['rest']
        factor_breakdown['rest'] = {'home': rest_home, 'away': rest_away}

        # 9. Injury Impact (2%)
        injury_home, injury_away = self._calculate_injuries(
            game_data['home_injury_impact'],
            game_data['away_injury_impact']
        )
        home_score += injury_home * self.WEIGHTS['injuries']
        away_score += injury_away * self.WEIGHTS['injuries']
        factor_breakdown['injuries'] = {'home': injury_home, 'away': injury_away}

        # Convert scores to probabilities
        total_score = home_score + away_score
        home_probability = (home_score / total_score) * 100 if total_score > 0 else 50
        away_probability = (away_score / total_score) * 100 if total_score > 0 else 50

        # Determine winner
        winner = home_team if home_probability > away_probability else away_team
        confidence = abs(home_probability - away_probability)

        # Build result
        result = {
            'timestamp': datetime.now().isoformat(),
            'home_team': home_team,
            'away_team': away_team,
            'home_probability': round(home_probability, 2),
            'away_probability': round(away_probability, 2),
            'predicted_winner': winner,
            'confidence': round(confidence, 2),
            'confidence_level': self._get_confidence_level(confidence),
            'factor_breakdown': factor_breakdown,
            'raw_scores': {'home': home_score, 'away': away_score}
        }

        return result

    # Individual calculation methods

    def _calculate_massey(self, home_rating: float, away_rating: float) -> Tuple[float, float]:
        """Calculate Massey rating advantage (0-100 scale for each team)"""
        total = home_rating + away_rating
        if total == 0:
            return 50, 50
        home_pct = (home_rating / total) * 100
        away_pct = (away_rating / total) * 100
        return home_pct, away_pct

    def _calculate_xg(self, home_xg: float, away_xg: float) -> Tuple[float, float]:
        """Calculate expected goals advantage"""
        # xG% already represents team's share of expected goals
        return home_xg, away_xg

    def _calculate_high_danger(self, home_hd: float, away_hd: float) -> Tuple[float, float]:
        """Calculate high-danger chances advantage"""
        return home_hd, away_hd

    def _calculate_goalie(self, home_sv: float, home_gaa: float,
                         away_sv: float, away_gaa: float) -> Tuple[float, float]:
        """
        Calculate goalie advantage
        Combines save % and GAA (inverse)
        """
        # Normalize save % (typically 0.900-0.930 range)
        home_sv_score = (home_sv - 0.850) * 200  # Scale to 0-100
        away_sv_score = (away_sv - 0.850) * 200

        # Normalize GAA (inverse - lower is better, typically 2.0-3.5 range)
        home_gaa_score = max(0, (4.0 - home_gaa) * 25)  # Scale to 0-100
        away_gaa_score = max(0, (4.0 - away_gaa) * 25)

        # Average the two metrics
        home_goalie = (home_sv_score + home_gaa_score) / 2
        away_goalie = (away_sv_score + away_gaa_score) / 2

        # Normalize to percentage
        total = home_goalie + away_goalie
        if total == 0:
            return 50, 50
        return (home_goalie / total) * 100, (away_goalie / total) * 100

    def _calculate_recent_form(self, home_w: int, home_l: int,
                               away_w: int, away_l: int) -> Tuple[float, float]:
        """Calculate recent form advantage (last 10 games)"""
        home_pct = (home_w / 10) * 100 if home_w + home_l > 0 else 50
        away_pct = (away_w / 10) * 100 if away_w + away_l > 0 else 50

        # Normalize
        total = home_pct + away_pct
        if total == 0:
            return 50, 50
        return (home_pct / total) * 100, (away_pct / total) * 100

    def _calculate_home_ice(self) -> float:
        """
        Home ice advantage
        NHL average is about 55% win rate at home
        """
        return 100  # Full points to home team

    def _calculate_special_teams(self, home_pp: float, home_pk: float,
                                 away_pp: float, away_pk: float) -> Tuple[float, float]:
        """
        Calculate special teams advantage
        Combines PP% and PK%
        """
        # Combine PP and PK (PK is already expressed as % success)
        home_st = (home_pp + home_pk) / 2
        away_st = (away_pp + away_pk) / 2

        # Normalize
        total = home_st + away_st
        if total == 0:
            return 50, 50
        return (home_st / total) * 100, (away_st / total) * 100

    def _calculate_rest(self, home_rest: int, away_rest: int) -> Tuple[float, float]:
        """
        Calculate rest advantage
        Teams with more rest (up to 2 days) have an advantage
        """
        # Optimal rest is 1-2 days, diminishing returns after that
        home_rest_score = min(home_rest, 3) * 25  # Max 75
        away_rest_score = min(away_rest, 3) * 25

        # Add 25 if team is more rested
        if home_rest > away_rest:
            home_rest_score += 25
        elif away_rest > home_rest:
            away_rest_score += 25
        else:
            home_rest_score += 12.5
            away_rest_score += 12.5

        # Normalize
        total = home_rest_score + away_rest_score
        if total == 0:
            return 50, 50
        return (home_rest_score / total) * 100, (away_rest_score / total) * 100

    def _calculate_injuries(self, home_impact: int, away_impact: int) -> Tuple[float, float]:
        """
        Calculate injury impact
        Scale 0-10 where 10 is most severe
        """
        # Inverse scoring - higher injury impact = lower score
        home_score = max(0, 10 - home_impact) * 10
        away_score = max(0, 10 - away_impact) * 10

        # Normalize
        total = home_score + away_score
        if total == 0:
            return 50, 50
        return (home_score / total) * 100, (away_score / total) * 100

    def _get_confidence_level(self, confidence: float) -> str:
        """Convert confidence percentage to level"""
        if confidence >= 20:
            return "Very High"
        elif confidence >= 15:
            return "High"
        elif confidence >= 10:
            return "Moderate"
        elif confidence >= 5:
            return "Low"
        else:
            return "Very Low (Toss-up)"

    def get_weights_info(self) -> Dict:
        """Return information about model weights"""
        return {
            'weights': self.WEIGHTS,
            'description': {
                'massey': 'Massey Ratings - Comprehensive power rankings',
                'expected_goals': 'Expected Goals % - Quality scoring chances',
                'high_danger': 'High-Danger Chances % - Premium scoring opportunities',
                'goalie': 'Goalie Matchup - Save % and GAA comparison',
                'recent_form': 'Recent Form - Last 10 games performance',
                'home_ice': 'Home Ice Advantage - Historical ~55% home win rate',
                'special_teams': 'Special Teams - Power Play and Penalty Kill',
                'rest': 'Rest Factor - Days since last game',
                'injuries': 'Injury Impact - Key player availability'
            }
        }
