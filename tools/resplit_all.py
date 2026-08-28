#!/usr/bin/env python3
"""Batch re-split all 20 episodes to convergence with the fixed splitter."""

import subprocess
import sys
import filecmp
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'output'
WORK = Path(sys.argv[1]) if len(sys.argv) > 1 else OUTPUT


def split_once(src: Path, dst: Path) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / 'tools' / 'split_srt.py'),
         '-i', str(src), '-o', str(dst)],
        check=True, capture_output=True, text=True, encoding='utf-8'
    )


def main():
    episodes = sorted(OUTPUT.glob('UFO-*'))
    for ep in episodes:
        src = ep / f'{ep.name}.zh-TW.srt'
        final = WORK / ep.name / f'{ep.name}.zh-TW.split.srt'
        final.parent.mkdir(parents=True, exist_ok=True)
        passes = 0
        temps = []
        cur = src
        while True:
            nxt = final.parent / f'.pass{passes + 1}.tmp.srt'
            split_once(cur, nxt)
            passes += 1
            temps.append(nxt)
            if cur != src and filecmp.cmp(str(cur), str(nxt), shallow=False):
                nxt.replace(final)
                for t in temps[:-1]:
                    t.unlink(missing_ok=True)
                break
            if passes > 12:
                for t in temps:
                    t.unlink(missing_ok=True)
                raise RuntimeError(f'{ep.name}: no convergence after {passes} passes')
            cur = nxt
        print(f'{ep.name}: {passes} passes -> {final.name}', flush=True)


if __name__ == '__main__':
    main()
