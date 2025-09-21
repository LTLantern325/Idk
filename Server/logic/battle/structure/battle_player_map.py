"""
Python conversion of Supercell.Laser.Logic.Battle.Structures.BattlePlayerMap.cs
Battle player map for managing players in battle
"""

from typing import Dict, List, Optional, Set
from .battle_player import BattlePlayer

class BattlePlayerMap:
    """Battle player map for managing players in battle"""

    def __init__(self):
        """Initialize battle player map"""
        self.players: Dict[int, BattlePlayer] = {}  # player_id -> BattlePlayer
        self.players_by_team: Dict[int, List[BattlePlayer]] = {}  # team_id -> List[BattlePlayer]
        self.players_by_account: Dict[int, BattlePlayer] = {}  # account_id -> BattlePlayer

        # Team management
        self.max_team_size = 3
        self.team_count = 2

        # Statistics
        self.total_kills = 0
        self.total_damage = 0

    def add_player(self, player: BattlePlayer) -> bool:
        """Add player to map"""
        if not player or player.player_id in self.players:
            return False

        # Add to main collection
        self.players[player.player_id] = player
        self.players_by_account[player.account_id] = player

        # Add to team collection
        team_id = player.team_id
        if team_id not in self.players_by_team:
            self.players_by_team[team_id] = []

        # Check team size
        if len(self.players_by_team[team_id]) >= self.max_team_size:
            return False

        self.players_by_team[team_id].append(player)
        return True

    def remove_player(self, player_id: int) -> bool:
        """Remove player from map"""
        if player_id not in self.players:
            return False

        player = self.players[player_id]

        # Remove from team collection
        if player.team_id in self.players_by_team:
            team_players = self.players_by_team[player.team_id]
            if player in team_players:
                team_players.remove(player)

                # Remove empty team
                if not team_players:
                    del self.players_by_team[player.team_id]

        # Remove from main collections
        del self.players[player_id]
        if player.account_id in self.players_by_account:
            del self.players_by_account[player.account_id]

        return True

    def get_player(self, player_id: int) -> Optional[BattlePlayer]:
        """Get player by ID"""
        return self.players.get(player_id)

    def get_player_by_account(self, account_id: int) -> Optional[BattlePlayer]:
        """Get player by account ID"""
        return self.players_by_account.get(account_id)

    def get_team_players(self, team_id: int) -> List[BattlePlayer]:
        """Get all players on team"""
        return self.players_by_team.get(team_id, [])

    def get_all_players(self) -> List[BattlePlayer]:
        """Get all players"""
        return list(self.players.values())

    def get_alive_players(self) -> List[BattlePlayer]:
        """Get all alive players"""
        return [player for player in self.players.values() if player.is_alive()]

    def get_dead_players(self) -> List[BattlePlayer]:
        """Get all dead players"""
        return [player for player in self.players.values() if player.is_dead()]

    def get_connected_players(self) -> List[BattlePlayer]:
        """Get all connected players"""
        return [player for player in self.players.values() if player.is_connected()]

    def get_player_count(self) -> int:
        """Get total player count"""
        return len(self.players)

    def get_team_count(self) -> int:
        """Get number of teams"""
        return len(self.players_by_team)

    def get_team_alive_count(self, team_id: int) -> int:
        """Get number of alive players on team"""
        team_players = self.get_team_players(team_id)
        return sum(1 for player in team_players if player.is_alive())

    def is_team_eliminated(self, team_id: int) -> bool:
        """Check if team is eliminated"""
        return self.get_team_alive_count(team_id) == 0

    def get_winning_team(self) -> Optional[int]:
        """Get winning team ID (if only one team has alive players)"""
        alive_teams = []
        for team_id in self.players_by_team.keys():
            if not self.is_team_eliminated(team_id):
                alive_teams.append(team_id)

        return alive_teams[0] if len(alive_teams) == 1 else None

    def get_mvp_player(self) -> Optional[BattlePlayer]:
        """Get MVP player (highest score)"""
        if not self.players:
            return None

        mvp = max(self.players.values(), key=lambda p: p.get_score())
        mvp.mvp = True
        return mvp

    def get_star_player(self, team_id: int) -> Optional[BattlePlayer]:
        """Get star player for team"""
        team_players = self.get_team_players(team_id)
        if not team_players:
            return None

        star_player = max(team_players, key=lambda p: p.get_score())
        star_player.star_player = True
        return star_player

    def get_leaderboard(self) -> List[BattlePlayer]:
        """Get players sorted by score"""
        return sorted(self.players.values(), key=lambda p: p.get_score(), reverse=True)

    def get_team_leaderboard(self, team_id: int) -> List[BattlePlayer]:
        """Get team players sorted by score"""
        team_players = self.get_team_players(team_id)
        return sorted(team_players, key=lambda p: p.get_score(), reverse=True)

    def get_battle_statistics(self) -> Dict[str, any]:
        """Get overall battle statistics"""
        total_kills = sum(player.kills for player in self.players.values())
        total_damage = sum(player.damage_dealt for player in self.players.values())
        total_healing = sum(player.healing_done for player in self.players.values())

        return {
            'player_count': len(self.players),
            'team_count': len(self.players_by_team),
            'total_kills': total_kills,
            'total_damage': total_damage,
            'total_healing': total_healing,
            'alive_players': len(self.get_alive_players()),
            'connected_players': len(self.get_connected_players())
        }

    def get_team_statistics(self, team_id: int) -> Dict[str, any]:
        """Get team statistics"""
        team_players = self.get_team_players(team_id)
        if not team_players:
            return {}

        total_kills = sum(player.kills for player in team_players)
        total_deaths = sum(player.deaths for player in team_players)
        total_damage = sum(player.damage_dealt for player in team_players)
        total_healing = sum(player.healing_done for player in team_players)
        alive_count = sum(1 for player in team_players if player.is_alive())

        return {
            'team_id': team_id,
            'player_count': len(team_players),
            'alive_count': alive_count,
            'total_kills': total_kills,
            'total_deaths': total_deaths,
            'total_damage': total_damage,
            'total_healing': total_healing,
            'eliminated': self.is_team_eliminated(team_id)
        }

    def balance_teams(self) -> bool:
        """Balance teams by moving players"""
        if len(self.players_by_team) != 2:
            return False  # Only works for 2-team battles

        team_ids = list(self.players_by_team.keys())
        team1_size = len(self.players_by_team[team_ids[0]])
        team2_size = len(self.players_by_team[team_ids[1]])

        # Move players if teams are unbalanced
        if abs(team1_size - team2_size) > 1:
            larger_team = team_ids[0] if team1_size > team2_size else team_ids[1]
            smaller_team = team_ids[1] if larger_team == team_ids[0] else team_ids[0]

            # Move last player from larger team
            player_to_move = self.players_by_team[larger_team][-1]
            self.players_by_team[larger_team].remove(player_to_move)
            self.players_by_team[smaller_team].append(player_to_move)
            player_to_move.team_id = smaller_team

            return True

        return False

    def update(self, delta_time: float) -> None:
        """Update all players"""
        for player in self.players.values():
            player.update(delta_time)

    def clear(self) -> None:
        """Clear all players"""
        self.players.clear()
        self.players_by_team.clear()
        self.players_by_account.clear()
        self.total_kills = 0
        self.total_damage = 0

    def encode(self, stream) -> None:
        """Encode battle player map to stream"""
        stream.write_v_int(len(self.players))
        for player in self.players.values():
            player.encode(stream)

        stream.write_v_int(len(self.players_by_team))
        for team_id, team_players in self.players_by_team.items():
            stream.write_v_int(team_id)
            stream.write_v_int(len(team_players))
            for player in team_players:
                stream.write_v_int(player.player_id)

    def decode(self, stream) -> None:
        """Decode battle player map from stream"""
        player_count = stream.read_v_int()
        for i in range(player_count):
            player = BattlePlayer()
            player.decode(stream)
            self.players[player.player_id] = player
            self.players_by_account[player.account_id] = player

        team_count = stream.read_v_int()
        for i in range(team_count):
            team_id = stream.read_v_int()
            team_player_count = stream.read_v_int()
            team_players = []

            for j in range(team_player_count):
                player_id = stream.read_v_int()
                if player_id in self.players:
                    team_players.append(self.players[player_id])

            self.players_by_team[team_id] = team_players

    def __str__(self) -> str:
        """String representation"""
        return f"BattlePlayerMap({len(self.players)} players, {len(self.players_by_team)} teams)"
