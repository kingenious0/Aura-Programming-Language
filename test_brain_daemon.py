"""
Test script for Aura Brain Daemon
"""

import time
from transpiler.brain_client import AuraBrainClient


def test_daemon():
    print("=" * 60)
    print("AURA BRAIN DAEMON TEST")
    print("=" * 60)

    client = AuraBrainClient()

    print("\n[1/4] Starting daemon...")
    start_time = time.time()

    if not client.start_daemon():
        print("❌ Failed to start daemon")
        return

    startup_time = time.time() - start_time
    print(f"✓ Daemon started in {startup_time:.2f}s")

    print("\n[2/4] Testing ping...")
    if client.ping():
        print("✓ Daemon is alive")
    else:
        print("❌ Daemon not responding")
        return

    print("\n[3/4] Testing corrections...")

    test_cases = [
        "crete a button with text 'Click'",
        "create is card with title 'Hello'",
        "create card is title 'God' and description 'God is here'",
        "Use dark theme",
        "make button red",
        "when clicked show card",
        "Create a heading with the text 'Already Correct'"
    ]

    total_time = 0
    corrections_made = 0

    for i, test_line in enumerate(test_cases, 1):
        print(f"\n  Test {i}/{len(test_cases)}")
        print(f"  Input:  {test_line}")

        result = client.correct(test_line)

        if "error" in result:
            print(f"  ❌ Error: {result['error']}")
            continue

        print(f"  Output: {result['corrected']}")
        print(f"  Time:   {result['time_ms']:.1f}ms")

        if result['changed']:
            print(f"  ✓ Corrected")
            corrections_made += 1
        else:
            print(f"  - No change needed")

        total_time += result['time_ms']

    avg_time = total_time / len(test_cases)

    print("\n[4/4] Performance Summary")
    print(f"  Total tests:       {len(test_cases)}")
    print(f"  Corrections made:  {corrections_made}")
    print(f"  Average time:      {avg_time:.1f}ms")
    print(f"  Total time:        {total_time:.1f}ms")

    print("\n[Cleanup] Stopping daemon...")
    client.stop_daemon()
    print("✓ Daemon stopped")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_daemon()
