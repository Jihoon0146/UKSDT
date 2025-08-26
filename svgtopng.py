#!/usr/bin/env python3
"""
SVG → PNG 변환 (정확한 WxH, 투명 배경 유지, CairoSVG)

사용 예:
  python svgtopng_cairosvg.py -i logo.svg -o out.png -s 300x300
  python svgtopng_cairosvg.py -i https://example.com/icon.svg -o out.png -s 256x256
"""

import argparse
import sys
import os

def parse_size(sz: str):
    try:
        w, h = map(int, sz.lower().split("x"))
        if w <= 0 or h <= 0:
            raise ValueError
        return w, h
    except Exception:
        raise argparse.ArgumentTypeError("사이즈는 '가로x세로' 형식의 양의 정수여야 합니다. 예: 300x300")

def main():
    msys2_path = r"E:\Tools\msys2\mingw64\bin"
    if msys2_path not in os.environ.get("PATH", ""):
        os.environ["PATH"] = msys2_path + os.pathsep + os.environ.get("PATH", "")
        print(f"[INFO] PATH에 {msys2_path} 추가 완료")
        
    ap = argparse.ArgumentParser(description="SVG→PNG (CairoSVG, 정확 WxH, 투명 배경)")
    ap.add_argument("-i", "--input", required=True, help="입력 SVG 경로 또는 URL")
    ap.add_argument("-o", "--output", required=True, help="출력 PNG 파일 경로")
    ap.add_argument("-s", "--size", required=True, type=parse_size, help="WxH (예: 300x300)")
    ap.add_argument("--dpi", type=int, default=96, help="렌더 DPI (기본 96)")
    args = ap.parse_args()

    w, h = args.size

    # CairoSVG 로드 (cairo DLL 문제를 명확히 안내)
    try:
        import cairosvg
    except Exception as e:
        sys.exit(f"[ERROR] CairoSVG 모듈을 불러오지 못했습니다: {e}\n"
                 f"  pip install cairosvg")

    try:
        # background_color=None => 투명(알파) 유지
        cairosvg.svg2png(
            url=args.input if (args.input.startswith("http://") or args.input.startswith("https://")) else None,
            file_obj=None if (args.input.startswith("http://") or args.input.startswith("https://")) else open(args.input, "rb"),
            write_to=args.output,
            output_width=w,
            output_height=h,
            dpi=args.dpi,
            background_color=None  # 완전 투명 배경 유지
        )
        print(f"[OK] {args.input} -> {args.output} ({w}x{h}, dpi={args.dpi}, transparent)")
    except OSError as e:
        # Windows에서 libcairo-2.dll 미존재 시 여기로 진입하는 경우가 많음
        sys.exit("[ERROR] 네이티브 cairo 라이브러리를 불러오지 못했습니다.\n"
                 f"원인: {e}\n"
                 "해결: (택1)\n"
                 "  - MSYS2 설치 후 mingw-w64-x86_64-cairo 설치 후 PATH에 C:\\msys64\\mingw64\\bin 추가\n"
                 "  - 또는 GTK3 Runtime 설치 후 해당 bin 경로를 PATH에 추가\n")
    except Exception as e:
        sys.exit(f"[ERROR] 변환 실패: {e}")

if __name__ == "__main__":
    main()
