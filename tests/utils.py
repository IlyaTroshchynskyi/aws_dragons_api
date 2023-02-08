from pathlib import Path


def create_invoke_command(base_dir: Path, func_name: str, event_file: str) -> str:
    """
    Create invoke command for lambda functions for tests
    """
    command = f'sam local invoke "{func_name}" -e {base_dir}/events/{event_file}.json ' \
              f'--template-file {base_dir}/template.yaml ' \
              f'--env-vars {base_dir}/env_test.json ' \
              f'--docker-network dragons'
    return command