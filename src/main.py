import argparse

from src.smart.orchestrator import MediaOrchestrator


def main(bronze, silver, gold):
    orchestrator = MediaOrchestrator(
        bronze_storage=bronze, silver_storage=silver, gold_storage=gold
    )
    orchestrator.bronze_to_silver()
    orchestrator.silver_to_gold()


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Media File Orchestrator")
    parser.add_argument(
        "--bronze", required=True, help="Path to the bronze storage directory"
    )
    parser.add_argument(
        "--silver", required=True, help="Path to the silver storage directory"
    )
    parser.add_argument(
        "--gold", required=True, help="Path to the gold storage directory"
    )

    # Parse arguments
    args = parser.parse_args()

    # Run the main function with the provided arguments
    main(bronze=args.bronze, silver=args.silver, gold=args.gold)

# python src\\main.py --bronze D:\\Users\\estev\\Pictures\\dev\\bronze --silver D:\\Users\\estev\\Pictures\\dev\\silver --gold D:\\Users\\estev\\Pictures\\dev\\gold
