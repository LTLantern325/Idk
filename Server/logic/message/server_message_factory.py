# Server/logic/message/server_message_factory.py
class ServerMessageFactory:
    """Dummy message factory (original C# did not have this)"""
    
    @staticmethod
    def initialize():
        from titan.debugger.debugger import Debugger
        Debugger.info("Dummy ServerMessageFactory initialized")