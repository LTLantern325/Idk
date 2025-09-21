"""
Python conversion of Supercell.Laser.Titan.Json.LogicJSONParser.cs
JSON parser for Logic JSON system
"""

import re
from typing import Optional, Union
from .logic_json_node import LogicJSONNode, LogicJSONNodeType
from .logic_json_array import LogicJSONArray
from .logic_json_boolean import LogicJSONBoolean
from .logic_json_null import LogicJSONNull
from .logic_json_number import LogicJSONNumber
from .logic_json_object import LogicJSONObject
from .logic_json_string import LogicJSONString

class CharStream:
    """Character stream for JSON parsing"""

    def __init__(self, text: str):
        """Initialize with text"""
        self._text = text
        self._offset = 0

    def read(self) -> str:
        """Read next character"""
        if self._offset >= len(self._text):
            return '\0'
        char = self._text[self._offset]
        self._offset += 1
        return char

    def read_string(self, length: int) -> Optional[str]:
        """Read string of specified length"""
        if self._offset + length > len(self._text):
            return None

        result = self._text[self._offset:self._offset + length]
        self._offset += length
        return result

    def next_char(self) -> str:
        """Peek at next character without advancing"""
        if self._offset >= len(self._text):
            return '\0'
        return self._text[self._offset]

    def skip_whitespace(self) -> None:
        """Skip whitespace characters"""
        while self._offset < len(self._text):
            char = self._text[self._offset]
            if char in ' \t\n\r':
                self._offset += 1
            else:
                break

class LogicJSONParser:
    """JSON parser for Logic JSON system"""

    @staticmethod
    def create_json_string(root: LogicJSONNode, ensure_capacity: int = 20) -> str:
        """Create JSON string from node"""
        builder = []
        root.write_to_string(builder)
        return ''.join(builder)

    @staticmethod
    def write_string(value: str, builder: list) -> None:
        """Write properly escaped string"""
        builder.append('"')

        if value:
            for char in value:
                if char == '\b':
                    builder.append('\\b')
                elif char == '\t':
                    builder.append('\\t')
                elif char == '\n':
                    builder.append('\\n')
                elif char == '\f':
                    builder.append('\\f')
                elif char == '\r':
                    builder.append('\\r')
                elif char == '"':
                    builder.append('\\"')
                elif char == '/':
                    builder.append('\\/')
                elif char == '\\':
                    builder.append('\\\\')
                else:
                    builder.append(char)

        builder.append('"')

    @staticmethod
    def parse_error(error: str) -> None:
        """Handle parse error"""
        from .debugger import Debugger
        Debugger.warning(f"JSON Parse error: {error}")

    @staticmethod
    def parse(json_text: str) -> Optional[LogicJSONNode]:
        """Parse JSON text"""
        try:
            stream = CharStream(json_text)
            return LogicJSONParser._parse_value(stream)
        except Exception as e:
            LogicJSONParser.parse_error(f"Parse failed: {str(e)}")
            return None

    @staticmethod
    def _parse_value(stream: CharStream) -> Optional[LogicJSONNode]:
        """Parse JSON value"""
        stream.skip_whitespace()
        char = stream.next_char()

        if char == '{':
            return LogicJSONParser._parse_object(stream)
        elif char == '[':
            return LogicJSONParser._parse_array(stream)
        elif char == 'n':
            return LogicJSONParser._parse_null(stream)
        elif char in 'ft':
            return LogicJSONParser._parse_boolean(stream)
        elif char == '"':
            return LogicJSONParser._parse_string(stream)
        elif char == '-' or char.isdigit():
            return LogicJSONParser._parse_number(stream)
        else:
            LogicJSONParser.parse_error(f"Unexpected character: {char}")
            return None

    @staticmethod
    def parse_array(json_text: str) -> Optional[LogicJSONArray]:
        """Parse JSON array"""
        return LogicJSONParser._parse_array(CharStream(json_text))

    @staticmethod
    def _parse_array(stream: CharStream) -> Optional[LogicJSONArray]:
        """Parse JSON array from stream"""
        stream.skip_whitespace()

        if stream.read() != '[':
            LogicJSONParser.parse_error("Not an array")
            return None

        array = LogicJSONArray()
        stream.skip_whitespace()

        # Check for empty array
        if stream.next_char() == ']':
            stream.read()
            return array

        while True:
            value = LogicJSONParser._parse_value(stream)
            if not value:
                break

            array.add(value)
            stream.skip_whitespace()

            next_char = stream.read()
            if next_char == ']':
                return array
            elif next_char != ',':
                LogicJSONParser.parse_error("Expected ',' or ']' in array")
                break

        LogicJSONParser.parse_error("Invalid array")
        return None

    @staticmethod
    def parse_object(json_text: str) -> Optional[LogicJSONObject]:
        """Parse JSON object"""
        return LogicJSONParser._parse_object(CharStream(json_text))

    @staticmethod
    def _parse_object(stream: CharStream) -> Optional[LogicJSONObject]:
        """Parse JSON object from stream"""
        stream.skip_whitespace()

        if stream.read() != '{':
            LogicJSONParser.parse_error("Not an object")
            return None

        obj = LogicJSONObject()
        stream.skip_whitespace()

        # Check for empty object
        if stream.next_char() == '}':
            stream.read()
            return obj

        while True:
            # Parse key
            key_node = LogicJSONParser._parse_string(stream)
            if not key_node:
                break

            key = key_node.get_string_value()
            stream.skip_whitespace()

            # Expect colon
            if stream.read() != ':':
                LogicJSONParser.parse_error("Expected ':' after key")
                break

            # Parse value
            value = LogicJSONParser._parse_value(stream)
            if not value:
                break

            obj.put(key, value)
            stream.skip_whitespace()

            next_char = stream.read()
            if next_char == '}':
                return obj
            elif next_char != ',':
                LogicJSONParser.parse_error("Expected ',' or '}' in object")
                break

        LogicJSONParser.parse_error("Invalid object")
        return None

    @staticmethod
    def _parse_string(stream: CharStream) -> Optional[LogicJSONString]:
        """Parse JSON string"""
        stream.skip_whitespace()

        if stream.read() != '"':
            LogicJSONParser.parse_error("Not a string")
            return None

        result = []

        while True:
            char = stream.read()
            if char == '\0':
                LogicJSONParser.parse_error("Unterminated string")
                return None
            elif char == '"':
                break
            elif char == '\\':
                # Handle escape sequences
                escape_char = stream.read()
                if escape_char == 'n':
                    result.append('\n')
                elif escape_char == 'r':
                    result.append('\r')
                elif escape_char == 't':
                    result.append('\t')
                elif escape_char == 'b':
                    result.append('\b')
                elif escape_char == 'f':
                    result.append('\f')
                elif escape_char == 'u':
                    # Unicode escape
                    hex_chars = stream.read_string(4)
                    if hex_chars and len(hex_chars) == 4:
                        try:
                            code_point = int(hex_chars, 16)
                            result.append(chr(code_point))
                        except ValueError:
                            result.append('?')
                    else:
                        result.append('?')
                elif escape_char == '\0':
                    LogicJSONParser.parse_error("Unterminated escape sequence")
                    return None
                else:
                    result.append(escape_char)
            else:
                result.append(char)

        return LogicJSONString(''.join(result))

    @staticmethod
    def _parse_boolean(stream: CharStream) -> Optional[LogicJSONBoolean]:
        """Parse JSON boolean"""
        stream.skip_whitespace()
        char = stream.read()

        if char == 'f':
            if (stream.read() == 'a' and stream.read() == 'l' and 
                stream.read() == 's' and stream.read() == 'e'):
                return LogicJSONBoolean(False)
        elif char == 't':
            if (stream.read() == 'r' and stream.read() == 'u' and 
                stream.read() == 'e'):
                return LogicJSONBoolean(True)

        LogicJSONParser.parse_error("Invalid boolean")
        return None

    @staticmethod
    def _parse_null(stream: CharStream) -> Optional[LogicJSONNull]:
        """Parse JSON null"""
        stream.skip_whitespace()
        char = stream.read()

        if (char == 'n' and stream.read() == 'u' and 
            stream.read() == 'l' and stream.read() == 'l'):
            return LogicJSONNull()

        LogicJSONParser.parse_error("Invalid null")
        return None

    @staticmethod
    def _parse_number(stream: CharStream) -> Optional[LogicJSONNumber]:
        """Parse JSON number"""
        stream.skip_whitespace()

        number_str = []
        char = stream.next_char()

        # Handle negative sign
        if char == '-':
            number_str.append(stream.read())
            char = stream.next_char()

        # Read digits
        if not char.isdigit():
            LogicJSONParser.parse_error("Invalid number")
            return None

        while char.isdigit():
            number_str.append(stream.read())
            char = stream.next_char()

        # Check for unsupported float notation
        if char in '.eE':
            LogicJSONParser.parse_error("JSON floats not supported")
            return None

        try:
            value = int(''.join(number_str))
            return LogicJSONNumber(value)
        except ValueError:
            LogicJSONParser.parse_error("Invalid number format")
            return None
