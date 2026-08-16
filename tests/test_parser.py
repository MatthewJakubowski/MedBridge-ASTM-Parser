import pytest
from medbridge.framing import ASTMFrameValidator
from medbridge.parser import ASTM1394Parser


def test_checksum_calculation():
    payload_with_end = "1H|\\^&|||Analyzer_01|||||||P|1\r\x03"
    expected_cs = ASTMFrameValidator.compute_checksum(payload_with_end)
    assert len(expected_cs) == 2
    assert expected_cs.isupper()


def test_frame_validator_success():
    content = "1H|\\^&|||Cobas_Pure|||||||P|1\r\x03"
    cs = ASTMFrameValidator.compute_checksum(content)
    raw_frame = f"\x02{content}{cs}\r\n"

    result = ASTMFrameValidator.validate_and_extract(raw_frame)
    assert result.is_valid is True
    assert result.frame_number == 1
    assert result.is_intermediate is False


def test_checksum_corruption_detection():
    raw_frame = "\x021H|\\^&|||Cobas_Pure|||||||P|1\r\x03FF\r\n"
    result = ASTMFrameValidator.validate_and_extract(raw_frame)
    assert result.is_valid is False


def test_astm_e1394_parsing_to_dataframe():
    raw_astm_transmission = (
        "H|\\^&|||ARCHITECT_c8000|||||||P|1|20260816080000\r"
        "P|1||PAT_98421^^^||DOE^JOHN||19850612|M\r"
        "O|1|SMP_2026_001|||R||||||A\r"
        "R|1|^^^GLU^Glucose|104.5|mg/dL|70-99|H||F||||20260816075500\r"
        "R|2|^^^CREA^Creatinine|0.92|mg/dL|0.70-1.20|N||F||||20260816075500\r"
        "L|1|N\r"
    )

    parser = ASTM1394Parser()
    patients = parser.parse_text(raw_astm_transmission)

    assert len(patients) == 1
    patient = patients[0]
    assert patient.patient_id == "PAT_98421"
    assert patient.sample_id == "SMP_2026_001"
    assert len(patient.results) == 2

    glu = patient.results[0]
    assert glu.test_name == "Glucose"
    assert glu.value_numeric == 104.5
    assert glu.abnormal_flag == "H"

    df = parser.to_dataframe(patients)
    assert len(df) == 2
    assert "patient_id" in df.columns
    assert "value_numeric" in df.columns
