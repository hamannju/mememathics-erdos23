#!/usr/bin/env python3
from pathlib import Path
import base64
import io
import tarfile

root = Path(__file__).resolve().parents[1]
chunks = sorted((root / ".bootstrap").glob("chunk*"))
if not chunks:
    raise RuntimeError("no payload chunks found")

encoded = "".join(path.read_text(encoding="ascii") for path in chunks)
payload = base64.b64decode(encoded, validate=True)

with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
    root_resolved = root.resolve()
    for member in archive.getmembers():
        target = (root / member.name).resolve()
        if target != root_resolved and root_resolved not in target.parents:
            raise RuntimeError(f"unsafe archive member: {member.name}")
    archive.extractall(root)
