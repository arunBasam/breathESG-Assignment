from django.urls import path

from .views import (

save_record,

get_records,

approve_record,
reject_record,

get_stats,
get_audit_logs,
get_audit_summary,
get_record_history,
get_quality_score,
health,
api_docs

)

urlpatterns=[

path(
"",
save_record
),

path(
"list/",
get_records
),

path(
"<int:id>/approve/",
approve_record
),

path(
"<int:id>/reject/",
reject_record
),

path(
"stats/",
get_stats
),

path(
"audit/",
get_audit_logs
),

path(
"audit/summary/",
get_audit_summary
),
path(
"<int:id>/history/",
get_record_history
),
path(
"quality/",
get_quality_score
),
path(
"health/",
health
),
path(
"docs/",
api_docs
)

]