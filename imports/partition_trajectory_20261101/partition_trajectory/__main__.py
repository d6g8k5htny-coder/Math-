import json
from .examples import run_all


def main():
    print(json.dumps(run_all(), indent=2, default=list))


if __name__ == "__main__":
    main()
