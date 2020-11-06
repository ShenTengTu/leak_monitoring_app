import sys
import toml
from pathlib import Path

path_here = Path(__file__).parent
path_project = path_here.parent
path_docker = path_project / "docker"


def export_py():
    with (path_project / "pyproject.toml").open("r") as fp:
        d = toml.load(fp)
    deps = d["tool"]["poetry"]["dependencies"]
    result = []
    for k, v in deps.items():
        if k == "python":
            continue
        ver = v
        extras = []
        if type(v) is not str:
            ver = v["version"]
            extras = v.get("extras", [])
        ver = ver.replace("^", ">=")
        extras = "" if len(extras) < 1 else "[{}]".format(", ".join(extras))
        result.append("{}{}{}".format(k, extras, ver))
    deps = "\n".join(result)
    with (path_docker / "requirements.txt").open("w") as fp:
        fp.write(deps)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: {} <command>".format(sys.argv[0]))
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "py":
        export_py()
