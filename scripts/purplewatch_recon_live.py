#!/usr/bin/env python3
"""Turn an ordered Wazuh reconnaissance sequence into one JSON log line.

Feed new alerts.json records on stdin. Run with unbuffered Python and append
stdout to a JSONL file monitored by Wazuh. Starts with empty history.
"""
import json
import sys
from collections import defaultdict, deque
from datetime import datetime

SEQUENCE = ("100104", "100105", "100106")
history = defaultdict(deque)

for line in sys.stdin:
    try:
        event = json.loads(line)
        rule = str(event["rule"]["id"])
        agent = str(event["agent"]["id"])
        when = datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
        alert_id = str(event["id"])
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        continue
    if rule not in SEQUENCE:
        continue
    q = history[agent]
    while q and (when - q[0][0]).total_seconds() > 300:
        q.popleft()
    if rule == SEQUENCE[2]:
        ps = next((v for v in reversed(q) if v[1] == SEQUENCE[1] and v[0] < when), None)
        uname = next((v for v in reversed(q) if ps and v[1] == SEQUENCE[0] and v[0] < ps[0]), None)
        if uname:
            result = {
                "event_type": "purplewatch_recon_sequence",
                "pw_source_agent_id": agent,
                "pw_source_agent_name": event["agent"].get("name", ""),
                "pw_rule_ids": "100104,100105,100106",
                "pw_alert_ids": ",".join((uname[2], ps[2], alert_id)),
                "pw_first_at": uname[0].isoformat(),
                "pw_last_at": when.isoformat(),
                "pw_duration_seconds": round((when - uname[0]).total_seconds(), 3),
            }
            print(json.dumps(result, ensure_ascii=False), flush=True)
    q.append((when, rule, alert_id))
