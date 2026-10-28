# Serverless SQS Job Worker

An AWS SAM project that sends queued JSON jobs to a Lambda worker. Amazon SQS retries failed messages and routes messages that repeatedly fail to a dead-letter queue (DLQ).

## Architecture

```text
Producer → SQS queue → Lambda worker
                  └── after 3 receives → dead-letter queue
```

## Deploy

Prerequisites: AWS CLI, Docker, and AWS SAM CLI.

```bash
sam build
sam deploy --guided
```

The stack outputs `QueueUrl` and `DeadLetterQueueUrl`. Send a sample job:

```bash
aws sqs send-message --queue-url QUEUE_URL --message-body '{"job_id":"demo-1","action":"resize-image"}'
```

View worker logs with `sam logs --stack-name STACK_NAME --tail`.

## Clean up

```bash
sam delete
```

SQS, Lambda, and CloudWatch Logs are metered AWS services. Delete the stack and its queues after the demo. The sample worker logs a validated job; replace the marked section with an idempotent business operation before using a real workload.
