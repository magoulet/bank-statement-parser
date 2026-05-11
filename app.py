import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.resolve()


def run_step(title: str, command: list[str]) -> None:
    print(f"\n== {title} ==")
    print("$ " + " ".join(command))
    try:
        completed = subprocess.run(command, cwd=ROOT)
    except FileNotFoundError as exc:
        print(f"Command failed: {exc}")
        return

    if completed.returncode == 0:
        print("Done.")
    else:
        print(f"Failed with exit code {completed.returncode}.")


def print_menu() -> None:
    print("\nBank Statement Parser")
    print("1) Sync IBKR Flex -> local database (trades + dividends)")
    print("2) Sync IBKR trades -> MariaDB (to be read by portfolio_return)")
    print("3) Generate dividend report (IBKR (sqlite) + CI Direct (CSV) + Closed, combined)")
    print("4) Exit")


def main() -> None:
    while True:
        print_menu()
        choice = input("Select an option [1-4]: ").strip()

        if choice == "1":
            run_step(
                "Sync IBKR Flex data to local database (trades + dividends)",
                [sys.executable, "scripts/flex_sync.py", "sync"],
            )
        elif choice == "2":
            confirm = input(
                "This uploads IBKR trades (buys/sells from flex + intraday queries) to MariaDB (portfolio) for the portfolio_return daily workflow. Continue? [y/N]: "
            ).strip().lower()
            if confirm == "y":
                run_step(
                    "Sync IBKR trades to MariaDB",
                    [sys.executable, "sync_transactions.py"],
                )
            else:
                print("Cancelled.")
        elif choice == "3":
            run_step(
                "Generate dividend report (IBKR + CI Direct + Closed)",
                [sys.executable, "report_dividends.py"],
            )
        elif choice == "4":
            print("Bye.")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
