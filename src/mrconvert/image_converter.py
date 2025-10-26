"""이미지에서 텍스트를 추출합니다. Extract text from image files."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .utils import OCRConfig, now_iso

try:  # pragma: no cover - optional dependency
    import pytesseract
except Exception:  # pragma: no cover
    pytesseract = None  # type: ignore[assignment]

try:  # pragma: no cover - optional dependency
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None  # type: ignore[assignment]


def _ocr_single_image(image_obj, lang: str | None) -> Tuple[str, str | None]:
    """단일 이미지를 pytesseract로 OCR합니다. OCR single frame with pytesseract."""

    if pytesseract is None:
        return "", None
    try:
        conf: Dict[str, Any] = {}
        if lang:
            conf["lang"] = lang
        text = pytesseract.image_to_string(image_obj, **conf)  # type: ignore[arg-type]
        return text or "", "pytesseract"
    except Exception:
        return "", None


def _ocr_with_ocrmypdf(image_obj, lang: str | None) -> Tuple[str, str | None]:
    """ocrmypdf를 활용해 OCR합니다. Run ocrmypdf-backed OCR as fallback."""

    if shutil.which("ocrmypdf") is None:
        return "", None
    if Image is None:
        return "", None

    with tempfile.TemporaryDirectory(prefix="mrconvert_img_") as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        src_pdf = tmp_dir_path / "frame.pdf"
        dst_pdf = tmp_dir_path / "frame.ocr.pdf"
        try:
            image_obj.save(src_pdf, format="PDF")
        except Exception:
            return "", None

        cmd: List[str] = ["ocrmypdf", "--quiet", "--skip-text"]
        if lang:
            cmd += ["-l", lang]
        cmd += [str(src_pdf), str(dst_pdf)]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            return "", None

        if not dst_pdf.exists():
            return "", None

        try:
            from . import pdf_converter

            result = pdf_converter.extract_pdf(dst_pdf, keep_layout=False, ocr=OCRConfig(mode="off", lang=lang))
            return (result.get("text") or ""), "ocrmypdf"
        except Exception:
            return "", None


def extract_image(path: Path, ocr: OCRConfig | None = None) -> Dict[str, Any]:
    """이미지 파일에서 텍스트를 추출합니다. Extract text from an image file."""

    ocr = ocr or OCRConfig()
    meta: Dict[str, Any] = {
        "source": str(path),
        "type": "image",
        "pages": 0,
        "parsed_at": now_iso(),
        "ocr": {"used": False, "engine": "none", "lang": ocr.lang},
    }

    text_parts: List[str] = []
    engine_used: str | None = None

    if Image is None:
        return {"meta": meta, "text": "", "markdown": "", "tables": []}

    try:
        with Image.open(path) as img:  # type: ignore[attr-defined]
            frames = getattr(img, "n_frames", 1)
            meta["pages"] = int(frames)
            for frame_index in range(frames):
                try:
                    if frames > 1:
                        img.seek(frame_index)
                    frame = img.convert("RGB")
                except Exception:
                    continue

                text, engine = _ocr_single_image(frame, ocr.lang)
                if not text.strip():
                    text, engine = _ocr_with_ocrmypdf(frame, ocr.lang)

                if text.strip():
                    text_parts.append(text.strip())
                    engine_used = engine or engine_used
    except Exception:
        return {"meta": meta, "text": "", "markdown": "", "tables": []}

    text_content = "\n\n".join(text_parts).strip()
    if text_content and engine_used:
        meta["ocr"].update({"used": True, "engine": engine_used})

    return {
        "meta": meta,
        "text": text_content,
        "markdown": text_content,
        "tables": [],
    }
