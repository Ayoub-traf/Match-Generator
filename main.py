import argparse
from match_gen import gen_match


def main(args):

    if args.time <= 0.0 or args.time > 120:
        print("The match duration (time) must be greater than 0 and less than or equal to 120.")
        return

    match = gen_match(args.time, args.style)
    match.to_json(args.output, orient="records")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a synthetic football match dataset.")
    parser.add_argument("--time", type=float, required=True, help="Duration of the football match in minutes.")
    parser.add_argument("--style", type=str, required=True, choices=["attacking", "defending", "balanced"],
                        help="Playing style of the match (attacking, defending, or balanced).")
    parser.add_argument("--output", type=str, required=False, default="generated_match.json")

    args = parser.parse_args()
    main(args)



