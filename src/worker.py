import json


def handler(event, _context):
    failures = []
    for record in event.get("Records", []):
        try:
            job = json.loads(record["body"])
            job_id = str(job.get("job_id", "")).strip()
            action = str(job.get("action", "")).strip()
            if not job_id or len(job_id) > 128 or not action:
                raise ValueError("job_id and action are required")
            # Replace this log with the application's actual idempotent work.
            print(json.dumps({"event": "job_processed", "job_id": job_id, "action": action}))
        except (json.JSONDecodeError, ValueError) as error:
            print(json.dumps({"event": "job_rejected", "error": str(error)}))
            # Invalid messages are reported as failures and moved to the DLQ after retries.
            failures.append({"itemIdentifier": record["messageId"]})
    return {"batchItemFailures": failures}
