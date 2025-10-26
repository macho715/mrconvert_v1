#!/usr/bin/env python3
"""
파일명 단순화 및 정리
"""

from pathlib import Path

# 파일명 매핑
FILENAME_MAP = {
    "2_EXT-08A-hvdc-material-handling-hvdc-material-handling-overview.md": "2_EXT-08A-hvdc-material-handling-overview.md",
    "2_EXT-08B-hvdc-material-handling-hvdc-material-handling-customs.md": "2_EXT-08B-hvdc-material-handling-customs.md",
    "2_EXT-08C-hvdc-material-handling-hvdc-material-handling-storage.md": "2_EXT-08C-hvdc-material-handling-storage.md",
    "2_EXT-08D-hvdc-material-handling-hvdc-material-handling-offshore.md": "2_EXT-08D-hvdc-material-handling-offshore.md",
    "2_EXT-08E-hvdc-material-handling-hvdc-material-handling-site-receiving.md": "2_EXT-08E-hvdc-material-handling-site-receiving.md",
    "2_EXT-08F-hvdc-material-handling-hvdc-material-handling-transformer.md": "2_EXT-08F-hvdc-material-handling-transformer.md",
}


def main():
    output_dir = Path("docs/ontology/extended")

    for old_name, new_name in FILENAME_MAP.items():
        old_file = output_dir / old_name
        new_file = output_dir / new_name

        if old_file.exists():
            print(f"Renaming: {old_name} → {new_name}")
            old_file.rename(new_file)

    print("파일명 정리 완료!")


if __name__ == "__main__":
    main()
