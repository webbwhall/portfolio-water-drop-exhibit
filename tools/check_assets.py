import os
import re

SITE = r"C:\Users\webbs\OneDrive\Desktop\Miami University\Intermed Interaction Design - IMS354 A\portfolio-water-drop-exhibit"


def main() -> None:
    html_path = os.path.join(SITE, "index.html")
    html = open(html_path, encoding="utf-8").read()
    paths = sorted(set(re.findall(r'src="(assets/images/[^"]+)"', html)))
    missing = []
    for p in paths:
        full = os.path.join(SITE, p.replace("/", os.sep))
        if not os.path.exists(full):
            missing.append(p)

    print("referenced:", len(paths))
    print("missing:", len(missing))
    for m in missing:
        print(" -", m)


if __name__ == "__main__":
    main()

