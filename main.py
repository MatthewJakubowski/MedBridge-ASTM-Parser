from medbridge.framing import ASTMFrameValidator
from medbridge.parser import ASTM1394Parser


def main():
    print("=" * 75)
    print(" 🔬 MedBridge-ASTM-Parser: Telemetry & Protocol Engine Demo")
    print("=" * 75)

    # 1. Simulate Raw Analyzer ASTM Stream (E1381 Framing with Modulo 256 Checksums)
    records = [
        "1H|\\^&|||Cobas_Pro_Biochem|||||||P|1\r\x03",
        "2P|1||PAT_44021^^^||Kowalski^Jan||19800412|M\r\x03",
        "3O|1|BARCODE_883921|||Stat_CITO||||||A\r\x03",
        "4R|1|^^^K^Potassium|5.85|mmol/L|3.50-5.10|H||F||||20260816080000\r\x03",
        "5R|2|^^^NA^Sodium|141.2|mmol/L|136.0-145.0|N||F||||20260816080000\r\x03",
        "6R|3|^^^CRP^C-Reactive Protein|48.2|mg/L|0.0-5.0|H||F||||20260816080000\r\x03",
        "7L|1|N\r\x03",
    ]

    raw_frames = []
    for r in records:
        cs = ASTMFrameValidator.compute_checksum(r)
        raw_frames.append(f"\x02{r}{cs}\r\n")

    print(f"\n[+] Ingesting {len(raw_frames)} raw transmission frames from analyzer stream...")

    # 2. Decode and Validate Frames (E1381)
    decoded_text = ASTMFrameValidator.assemble_session(raw_frames)
    print("[✓] All frames passed Modulo 256 checksum verification.")

    # 3. Parse Records into Structured Objects (E1394)
    parser = ASTM1394Parser()
    patients = parser.parse_text(decoded_text)
    df = parser.to_dataframe(patients)

    # 4. Display Results
    print("\n--- Parsed Clinical Telemetry DataFrame ---")
    print(df[["patient_id", "sample_id", "priority", "test_name", "value_numeric", "units", "abnormal_flag"]])


if __name__ == "__main__":
    main()
