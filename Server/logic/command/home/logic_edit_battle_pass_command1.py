"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicEditBattlePassCommand1.cs
Alternative command for editing battle pass (command variation)
"""

from ..command import Command

class LogicEditBattlePassCommand1(Command):
    """Alternative command for editing battle pass (command variation)"""

    def __init__(self):
        """Initialize edit battle pass command 1"""
        super().__init__()
        self.season_id = 0
        self.operation_type = 0  # 0=add_tokens, 1=set_tier, 2=claim_reward
        self.parameter_value = 0
        self.auto_claim = False

    def get_season_id(self) -> int:
        """Get season ID"""
        return self.season_id

    def set_season_id(self, season_id: int) -> None:
        """Set season ID"""
        self.season_id = season_id

    def get_operation_type(self) -> int:
        """Get operation type"""
        return self.operation_type

    def set_operation_type(self, operation_type: int) -> None:
        """Set operation type"""
        self.operation_type = operation_type

    def get_parameter_value(self) -> int:
        """Get parameter value"""
        return self.parameter_value

    def set_parameter_value(self, value: int) -> None:
        """Set parameter value"""
        self.parameter_value = value

    def execute(self, avatar: any) -> int:
        """Execute edit battle pass command 1"""
        # Get battle pass data
        if not hasattr(avatar, 'battle_pass_data'):
            avatar.battle_pass_data = {}

        battle_pass = avatar.battle_pass_data.get(self.season_id, {
            'tokens': 0,
            'tier': 0,
            'claimed_rewards': []
        })

        if self.operation_type == 0:  # Add tokens
            battle_pass['tokens'] += self.parameter_value
            # Calculate new tier
            tokens_per_tier = 100
            battle_pass['tier'] = min(30, battle_pass['tokens'] // tokens_per_tier)
        elif self.operation_type == 1:  # Set tier
            battle_pass['tier'] = min(30, max(0, self.parameter_value))
            # Set minimum required tokens
            battle_pass['tokens'] = max(battle_pass['tokens'], battle_pass['tier'] * 100)
        elif self.operation_type == 2:  # Claim reward
            reward_tier = self.parameter_value
            if reward_tier not in battle_pass['claimed_rewards'] and reward_tier <= battle_pass['tier']:
                battle_pass['claimed_rewards'].append(reward_tier)

        avatar.battle_pass_data[self.season_id] = battle_pass
        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.season_id)
        stream.write_v_int(self.operation_type)
        stream.write_v_int(self.parameter_value)
        stream.write_boolean(self.auto_claim)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.season_id = stream.read_v_int()
        self.operation_type = stream.read_v_int()
        self.parameter_value = stream.read_v_int()
        self.auto_claim = stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        operations = ["AddTokens", "SetTier", "ClaimReward"]
        op_name = operations[self.operation_type] if self.operation_type < len(operations) else "Unknown"
        return f"EditBattlePassCommand1(season={self.season_id}, op={op_name}, value={self.parameter_value})"
