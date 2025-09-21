"""
Python conversion of ZLib block state enumeration
Deflate block processing states
"""

from enum import IntEnum

class BlockState(IntEnum):
    """Deflate block processing states"""

    NEED_MORE = 0      # Block not completed, need more input or more output
    BLOCK_DONE = 1     # Block flush performed 
    FINISH_STARTED = 2 # Finish started, need only more output at next deflate
    FINISH_DONE = 3    # Finish done, accept no more input or output

    def __str__(self) -> str:
        """String representation"""
        state_names = {
            0: "NeedMore",
            1: "BlockDone",
            2: "FinishStarted", 
            3: "FinishDone"
        }
        return state_names.get(self.value, f"State{self.value}")

    def is_finished(self) -> bool:
        """Check if processing is finished"""
        return self == BlockState.FINISH_DONE

    def needs_input(self) -> bool:
        """Check if more input is needed"""
        return self == BlockState.NEED_MORE

    def needs_output(self) -> bool:
        """Check if more output space is needed"""
        return self in (BlockState.NEED_MORE, BlockState.FINISH_STARTED)
