import re

# open with fallback encodings (Windows-safe)
encodings = ["utf-8", "utf-16", "latin-1"]
for enc in encodings:
    try:
        with open("requirements.in", encoding=enc) as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        break
    except UnicodeDecodeError:
        continue
else:
    raise RuntimeError("Could not decode requirements.in — please save as UTF-8")

def to_range(spec):
    m = re.match(r"^([A-Za-z0-9_.\-\[\]]+)==(\d+)\.(\d+)\.(\d+).*?$", spec)
    if not m:
        return spec  # leave non-standard specs as-is
    name, major, minor, patch = m.groups()
    return f"{name}>={major}.{minor}"

deps = [to_range(line) for line in lines]

print("[project]\ndependencies = [")
for dep in deps:
    print(f'  "{dep}",')
print("]")
