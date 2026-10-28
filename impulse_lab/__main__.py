"""Run finite offline scenarios and print synthetic JSON telemetry."""
import argparse
import json

from .model import MAX_TICKS, SCENARIOS, simulate


def bounded_ticks(value):
    try:
        ticks = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("ticks must be an integer") from exc
    if not 1 <= ticks <= MAX_TICKS:
        raise argparse.ArgumentTypeError("ticks must be between 1 and 100")
    return ticks


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Impulse Defensive Lab: bounded, offline queue simulation",
        allow_abbrev=False,
    )
    parser.add_argument("--scenario", choices=SCENARIOS, default="baseline")
    parser.add_argument("--ticks", type=bounded_ticks, default=20)
    parser.add_argument("--events", action="store_true", help="print JSONL tick events")
    args = parser.parse_args(argv)
    events, summary = simulate(args.scenario, args.ticks)
    if args.events:
        for event in events:
            print(json.dumps(event, sort_keys=True))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
