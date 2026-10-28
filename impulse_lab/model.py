"""Deterministic, bounded queue model; ticks are logical, not wall-clock time."""

SCENARIOS = ("baseline", "congestion", "rate-limit")
MAX_TICKS = 100
CAPACITY = 12
SERVICE_PER_TICK = 3


def simulate(scenario="baseline", ticks=20):
    """Return synthetic events and a summary; never send or receive traffic.

    Arrivals are admitted before service. The optional admission limit rejects
    excess arrivals before the bounded queue. Remaining work is not drained.
    """
    if scenario not in SCENARIOS:
        raise ValueError("unknown scenario")
    if type(ticks) is not int or not 1 <= ticks <= MAX_TICKS:
        raise ValueError("ticks must be an integer between 1 and 100")
    queue = []
    events = []
    waits = []
    offered = completed = rejected = dropped = peak = 0
    for tick in range(ticks):
        arrivals = 2 if scenario == "baseline" else 6
        limited = max(0, arrivals - SERVICE_PER_TICK) if scenario == "rate-limit" else 0
        eligible = arrivals - limited
        admitted = min(eligible, CAPACITY - len(queue))
        overflow = eligible - admitted
        queue.extend([tick] * admitted)
        peak = max(peak, len(queue))
        served = min(SERVICE_PER_TICK, len(queue))
        waits.extend(tick - entered for entered in queue[:served])
        del queue[:served]
        offered += arrivals
        completed += served
        rejected += limited
        dropped += overflow
        events.append({
            "type": "tick", "synthetic": True, "tick": tick,
            "offered": arrivals, "admitted": admitted, "rate_limited": limited,
            "queue_dropped": overflow, "completed": served,
            "queue_depth": len(queue),
        })
    summary = {
        "type": "summary", "synthetic": True, "schema_version": 1,
        "scenario": scenario, "ticks": ticks, "offered": offered,
        "completed": completed, "rate_limited": rejected,
        "queue_dropped": dropped, "remaining": len(queue),
        "queue_capacity": CAPACITY, "peak_queue_depth": peak,
        "mean_wait_ticks": round(sum(waits) / len(waits), 3) if waits else 0,
    }
    return events, summary
