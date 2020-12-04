import sys
import toml
import shutil
from pathlib import Path
from configparser import ConfigParser

path_here = Path(__file__).parent
path_project = path_here.parent
path_docker = path_project / "docker"


def export_py(dev_set=set()):
    def _parse(k, v, result=list()):
        ver = v
        extras = []
        if type(v) is not str:
            ver = v["version"]
            extras = v.get("extras", [])
        ver = ver.replace("^", "~=")
        extras = "" if len(extras) < 1 else "[{}]".format(", ".join(extras))
        result.append("{}{}{}".format(k, extras, ver))
        return result

    with (path_project / "pyproject.toml").open("r") as fp:
        d = toml.load(fp)
    d_poetry = d["tool"]["poetry"]
    deps = d_poetry["dependencies"]
    result = None
    for k, v in deps.items():
        if k == "python":
            continue
        result = _parse(k, v)
    dev_deps = d_poetry["dev-dependencies"]
    for k, v in dev_deps.items():
        if k not in dev_set:
            continue
        result = _parse(k, v)
    req = "\n".join(result)
    with (path_docker / "requirements.txt").open("w") as fp:
        fp.write(req)


def export_ufw_profile():
    path_out = path_project / "config" / "ufw" / "ndlm_leak_monitoring_app"
    config = ConfigParser()
    config["ndlm_leak_monitoring_app"] = dict(
        title="Nephrology Dialysis Leak Monitoring App",
        description="HTTP,HTTPS,MQTT,MQTTS",
        ports="|".join(["80,443,1883,8883/tcp"]),
    )
    with path_out.open("w") as fp:
        config.write(fp)


def export_static_files():
    path_node_modules = path_project / "node_modules"
    path_static = path_docker / "src" / "static"

    module = path_node_modules / "uikit" / "dist"
    ps = (*module.glob("css/*.min.css"), *module.glob("js/*.min.js"))
    for p in ps:
        target: Path = path_static / "uikit" / p.relative_to(module)
        if not target.parent.exists():
            target.parent.mkdir(parents=True)
        shutil.copyfile(p, target)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: {} <command>".format(sys.argv[0]))
        sys.exit(0)
    local_objs = locals()
    action = "export_{}".format(sys.argv[1])
    fn = local_objs.get(action, None)
    if callable(fn):
        if action == "export_py":
            fn(dev_set={"debugpy"})
        else:
            fn()
