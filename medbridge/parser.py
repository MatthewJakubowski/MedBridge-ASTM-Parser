from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional
import pandas as pd


@dataclass
class ClinicalResult:
    sample_id: str
    test_code: str
    test_name: str
    value_numeric: Optional[float]
    value_raw: str
    units: str
    reference_range: str
    abnormal_flag: str
    result_status: str
    timestamp: str
    instrument_flag: str = ""


@dataclass
class PatientRecord:
    patient_id: str
    sample_id: str
    priority: str
    results: List[ClinicalResult] = field(default_factory=list)


class ASTM1394Parser:
    """
    Parses ASTM E1394 record hierarchy (H, P, O, R, C, L) into structured dataclasses and Pandas DataFrames.
    """

    def __init__(self, field_sep: str = "|", repeat_sep: str = "\\", comp_sep: str = "^", esc_sep: str = "&"):
        self.field_sep = field_sep
        self.comp_sep = comp_sep

    def parse_text(self, raw_text: str) -> List[PatientRecord]:
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        patients: List[PatientRecord] = []
        current_patient_id = "ANONYMOUS"
        current_sample_id = "UNKNOWN"
        current_priority = "Routine"
        current_results: List[ClinicalResult] = []

        for line in lines:
            if not line:
                continue

            if line.startswith("H"):
                if len(line) >= 5 and line[1] in ("|", "\\", "^"):
                    self.field_sep = line[1]
                continue

            fields = line.split(self.field_sep)
            record_type = fields[0].strip()

            if record_type == "P":
                if current_results:
                    patients.append(
                        PatientRecord(
                            patient_id=current_patient_id,
                            sample_id=current_sample_id,
                            priority=current_priority,
                            results=list(current_results),
                        )
                    )
                    current_results.clear()
                current_patient_id = fields[3].split(self.comp_sep)[0].strip() if len(fields) > 3 and fields[3] else "ANONYMOUS"

            elif record_type == "O":
                current_sample_id = fields[2].strip() if len(fields) > 2 else "UNKNOWN"
                current_priority = fields[5].strip() if len(fields) > 5 and fields[5] else "Routine"

            elif record_type == "R":
                test_raw = fields[2] if len(fields) > 2 else ""
                test_parts = test_raw.split(self.comp_sep)
                test_code = test_parts[3] if len(test_parts) > 3 else (test_parts[0] if test_parts else "N/A")
                test_name = test_parts[4] if len(test_parts) > 4 else test_code

                raw_val = fields[3].strip() if len(fields) > 3 else ""
                try:
                    num_val = float(raw_val)
                except ValueError:
                    num_val = None

                units = fields[4].strip() if len(fields) > 4 else ""
                ref_range = fields[5].strip() if len(fields) > 5 else ""
                flag = fields[6].strip() if len(fields) > 6 else "N"
                status = fields[8].strip() if len(fields) > 8 else "F"
                timestamp = fields[12].strip() if len(fields) > 12 else ""

                current_results.append(
                    ClinicalResult(
                        sample_id=current_sample_id,
                        test_code=test_code,
                        test_name=test_name,
                        value_numeric=num_val,
                        value_raw=raw_val,
                        units=units,
                        reference_range=ref_range,
                        abnormal_flag=flag,
                        result_status=status,
                        timestamp=timestamp,
                    )
                )

            elif record_type == "L":
                if current_results or current_patient_id != "ANONYMOUS":
                    patients.append(
                        PatientRecord(
                            patient_id=current_patient_id,
                            sample_id=current_sample_id,
                            priority=current_priority,
                            results=list(current_results),
                        )
                    )
                    current_results.clear()

        return patients

    def to_dataframe(self, patients: List[PatientRecord]) -> pd.DataFrame:
        flat_rows = []
        for p in patients:
            for r in p.results:
                row = asdict(r)
                row["patient_id"] = p.patient_id
                row["priority"] = p.priority
                flat_rows.append(row)
        return pd.DataFrame(flat_rows)
