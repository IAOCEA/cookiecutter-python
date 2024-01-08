import pathlib
import subprocess

project_directory = pathlib.Path.cwd().resolve().absolute()
licenses_root = project_directory / "licenses"

package_manager_exts = {
    "conda": "yaml",
    "pip": "txt",
}


def clean_file(path):
    import yaml

    content = path.read_text()
    parsed = yaml.safe_load(content)
    dumped = yaml.safe_dump(parsed, sort_keys=False)

    path.write_text(dumped)


if __name__ == "__main__":
    # remove unused package manager files
    ci_root = project_directory.joinpath("ci/requirements")
    package_manager = "{{ cookiecutter.package_manager }}"
    to_delete = [
        ext
        for ext in package_manager_exts.values()
        if ext != package_manager_exts[package_manager]
    ]

    glob = (
        "*.{" + ",".join(to_delete) + "}"
        if len(to_delete) > 1
        else f"*.{''.join(to_delete)}"
    )
    for path in ci_root.glob(glob):
        path.unlink()

    if package_manager == "conda":
        # clean up the yaml files
        for path in ci_root.glob(f"*.{package_manager_exts[package_manager]}"):
            clean_file(path)

    # submit everything into a git repository
    result = subprocess.run(
        ["git", "init", "--initial-branch={{ cookiecutter.main_branch }}"]
    )
    if result.returncode != 0:
        raise SystemExit(
            "\n - ".join(
                [
                    "initializing git failed:",
                    f"stderr: {result.stderr.decode()}",
                    "stdout: {result.stdout.decode()}",
                ]
            )
        )

    subprocess.run(["git", "config", "user.name", "{{ cookiecutter.full_name }}"])
    subprocess.run(["git", "config", "user.email", "{{ cookiecutter.email }}"])

    subprocess.run(["git", "add", "-A"])

    subprocess.run(["pre-commit", "install"])
    subprocess.run(["pre-commit", "autoupdate"])
    subprocess.run(["pre-commit", "run", "--all-files"])

    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", "create project from cookiecutter template"])
