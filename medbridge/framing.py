from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class FrameResult:
    frame_number: int
    payload: str
    checksum: str
    is_valid: bool
    is_intermediate: bool  # True if ended with ETB, False if ETX


class ASTMFrameValidator:
    """
    Handles low-level ASTM E1381 framing, Modulo 256 checksum computation,
    and frame validation.
    """

    STX = "\x02"
    ETX = "\x03"
    ETB = "\x17"
    CR = "\r"
    LF = "\n"

    @staticmethod
    def compute_checksum(data: str) -> str:
        """
        Calculates ASTM Modulo 256 checksum in uppercase 2-digit HEX.
        Checksum sums ASCII byte values from <STX> (exclusive) through <ETX>/<ETB> (inclusive).
        """
        total = sum(ord(char) for char in data) % 256
        return f"{total:02X}"

    @classmethod
    def validate_and_extract(cls, raw_frame: str) -> FrameResult:
        """
        Parses a raw ASTM E1381 frame string: <STX>[FN][Payload][ETX/ETB][CS]<CR><LF>
        """
        clean_frame = raw_frame.strip("\r\n")

        if not clean_frame.startswith(cls.STX):
            raise ValueError("Invalid frame: Missing STX start byte.")

        if cls.ETX in clean_frame:
            end_char = cls.ETX
            is_intermediate = False
        elif cls.ETB in clean_frame:
            end_char = cls.ETB
            is_intermediate = True
        else:
            raise ValueError("Invalid frame: Missing ETX or ETB terminator.")

        end_idx = clean_frame.find(end_char)
        content_with_end = clean_frame[1 : end_idx + 1]
        received_checksum = clean_frame[end_idx + 1 : end_idx + 3].upper()

        computed_checksum = cls.compute_checksum(content_with_end)
        is_valid = computed_checksum == received_checksum

        frame_number = int(content_with_end[0]) if content_with_end[0].isdigit() else 0
        payload = content_with_end[1:-1]

        return FrameResult(
            frame_number=frame_number,
            payload=payload,
            checksum=received_checksum,
            is_valid=is_valid,
            is_intermediate=is_intermediate,
        )

    @classmethod
    def assemble_session(cls, frames: List[str]) -> str:
        """
        Validates all frames in a transmission block and merges their payloads.
        """
        combined_payload = []
        for raw in frames:
            if not raw.strip():
                continue
            res = cls.validate_and_extract(raw)
            if not res.is_valid:
                raise ValueError(
                    f"Checksum mismatch on frame {res.frame_number}! "
                    f"Received: {res.checksum}, Computed: {cls.compute_checksum(res.payload)}"
                )
            combined_payload.append(res.payload)

        return "".join(combined_payload)
