import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "static" / "brand_config.json"
OUTPUT_PATH = ROOT / "static" / "brand_tokens.css"


def main() -> None:
    brand = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    palette = brand["palette"]
    typography = brand["typography"]
    css = f""":root {{
  --brand-primary: {palette["primary"]};
  --brand-secondary: {palette["secondary"]};
  --brand-accent: {palette["accent"]};
  --heading-font: "{typography["heading"]}", Georgia, serif;
  --body-font: "{typography["body"]}", system-ui, sans-serif;
}}
"""
    OUTPUT_PATH.write_text(css, encoding="utf-8")
    print(f"Exported {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
