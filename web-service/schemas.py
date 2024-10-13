from marshmallow import Schema, fields

class MessageSchema(Schema):

    id = fields.String(dump_only=True)
    author_id = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    text = fields.String(required=True)
    processed = fields.Boolean(required=True)
    sentiment_score = fields.Float()
    sentiment_magnitude = fields.Float()
    sentiment_text = fields.String()
    sentiment_classification = fields.String()
    magnitude_classification = fields.String()
    
class JobSchema(Schema):
    id = fields.String(dump_only=True)
    service_name = fields.Str(required=True)
    job_start_date = fields.DateTime(required=True)
    job_end_date = fields.DateTime()
    rows_processed = fields.Int()
    rows_failed = fields.Int()
    runtime = fields.Float()
    messages = fields.List(fields.Nested(MessageSchema(), dump_only=True))

class MetricSchema(Schema):
    total_messages = fields.Int()
    total_jobs = fields.Int()
    jobs_with_failed_rows = fields.Int()
    avg_messages_per_job = fields.Float()
    avg_job_runtime = fields.Float()
    last_job_run_date = fields.DateTime()

