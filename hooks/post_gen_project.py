import pathlib
import subprocess

project_directory = pathlib.Path.cwd().resolve().absolute()


if __name__ == "__main__":
    # run git init
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