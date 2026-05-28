from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from audit.models import AuditLog

from .models import (
    RawRecord,
    DataSource,
    AuditLog,
    Tenant,
    NormalizedRecord
)


@api_view(["POST"])
def save_record(request):

    source = request.data.get(
        "source"
    )
    allowed = [

"SAP",

"UTILITY",

"TRAVEL"

]    
    if not source:
        return Response(

        {

            "error":

            "source required"

        },

        status=400

    )

    if source not in allowed:
        return Response(

        {

            "error":

            "invalid source"

        },

        status=400

    )


    suspicious = (
        source == "SAP"
    )

    tenant,_ = Tenant.objects.get_or_create(
        name="Demo Company"

)   
    
    existing = (

DataSource.objects

.filter(

tenant=tenant,

source_type=source

)

.order_by(
"-uploaded_at"
)

.first()

)
    if existing:
        return Response(

{

"error":

"Source already uploaded for this tenant"

},

status=409

)





    datasource = DataSource.objects.create(

tenant=tenant,

source_type=source

)

    record = RawRecord.objects.create(

    source=datasource,

    raw_data={

        "source": source,

        "suspicious": suspicious

    },

    status="PENDING"

)   
    
    scope = (

"Scope 1"

if source=="SAP"

else

"Scope 2"

if source=="UTILITY"

else

"Scope 3"

)
    value = (

120

if source=="SAP"

else

85

if source=="UTILITY"

else

45

)

    NormalizedRecord.objects.create(

raw_record=record,

scope=scope,

normalized_value=value,

review_status="PENDING"

)
    
    
    
    return Response({

        "message":

        "saved"

    })


@api_view(["GET"])
def get_records(request):

    rows = []

    page = int(
        request.GET.get(
            "page",
1
)

)

    limit = 10

    total = (

RawRecord.objects

.count()

)

    start = (
    page-1
    )*limit

    end = start+limit

    records = (

RawRecord.objects

.select_related(
"source"
)

.order_by(
"-id"
)

[start:end]

)
    for r in records:

        source = r.raw_data.get(
            "source"
        )

        audit = (

            AuditLog.objects

            .filter(
                record=r
            )

            .order_by(
                "-created_at"
            )

            .first()

        )

        rows.append({

            "id":
            r.id,

            "source":
            source,

            "source_type":
            r.source.source_type,

            "scope":

            "Scope 1"

            if source=="SAP"

            else

            "Scope 2"

            if source=="UTILITY"

            else

            "Scope 3",

            "status":
            r.status,

            "suspicious":

            r.raw_data.get(
                "suspicious",
                False
            ),

            "uploaded_at":

            r.source.uploaded_at.strftime(
                "%d-%m-%Y %H:%M"
            ),

            "audit":

            audit.action

            if audit

            else

            "-",

            "audit_time":

            audit.created_at.strftime(
                "%d-%m-%Y %H:%M"
            )

            if audit

            else

            "-"

        })

    return Response({

"page":
page,

"limit":
limit,

"total":
total,

"pages":

(

total
+
limit
-
1

)

//

limit,

"data":
rows

})

@api_view(["POST"])
def approve_record(request, id):

    record = get_object_or_404(

        RawRecord,

        id=id

    )

    if record.status != "LOCKED":

        record.status = "LOCKED"
        record.save()

        normalized = (

        NormalizedRecord.objects

        .filter(
        raw_record=record
)

        .first()

)

        if normalized:
            normalized.review_status = "APPROVED"
            normalized.save()





        AuditLog.objects.create(

            record=record,

            action="APPROVED"

        )

    return Response({

        "message":

        "approved"

    })


@api_view(["POST"])
def reject_record(request, id):

    record = get_object_or_404(

        RawRecord,

        id=id

    )

    record.status = "REJECTED"

    record.save()

    normalized = (

        NormalizedRecord.objects

        .filter(
            raw_record=record
        )

        .first()

    )

    if normalized:

        normalized.review_status = "REJECTED"

        normalized.save()

    AuditLog.objects.create(

        record=record,

        action="REJECTED"

    )

    return Response({

        "message":

        "rejected"

    })

@api_view(["GET"])
def get_stats(request):

    records = RawRecord.objects.all()

    total = records.count()

    pending = (

        records

        .filter(
            status="PENDING"
        )

        .count()

    )

    approved = (

        records

        .filter(
            status="LOCKED"
        )

        .count()

    )

    suspicious = (

        sum(

            1

            for r in records

            if r.raw_data.get(
                "suspicious",
                False
            )

        )

    )

    return Response({

        "total":
        total,

        "pending":
        pending,

        "approved":
        approved,

        "suspicious":
        suspicious,

        "approval_rate":

        round(

            (
                approved
                /
                total
            )

            *

            100,

            1

        )

        if total

        else

        0

    })

@api_view(["GET"])
def get_audit_logs(request):

    rows = []

    logs = (

        AuditLog.objects

        .select_related(
            "record"
        )

        .order_by(
            "-created_at"
        )

    )

    for log in logs:

        rows.append({

            "record_id":

            log.record.id,

            "action":

            log.action,

            "created_at":

            log.created_at.strftime(
                "%d-%m-%Y %H:%M"
            )

        })

    return Response(
        rows
    )

@api_view(["GET"])
def get_audit_summary(request):

    approved = (

        AuditLog.objects

        .filter(
            action="APPROVED"
        )

        .count()

    )

    rejected = (

        AuditLog.objects

        .filter(
            action="REJECTED"
        )

        .count()

    )

    total = approved + rejected

    return Response({

        "approved":
        approved,

        "rejected":
        rejected,

        "total_reviews":
        total

    })

@api_view(["GET"])
def get_record_history(request, id):

    record = get_object_or_404(
        RawRecord,
        id=id
    )

    logs = (

        AuditLog.objects

        .filter(
            record=record
        )

        .order_by(
            "-created_at"
        )

    )

    rows = []

    for log in logs:

        rows.append({

            "action":

            log.action,

            "time":

            log.created_at.strftime(
                "%d-%m-%Y %H:%M"
            )

        })

    normalized = (

        NormalizedRecord.objects

        .filter(
            raw_record=record
        )

        .first()

    )

    return Response({

        "record_id":
        record.id,

        "status":
        record.status,

        "normalized_review":

        normalized.review_status

        if normalized

        else

        "-",

        "history":
        rows

    })

@api_view(["GET"])
def get_quality_score(request):

    total = RawRecord.objects.count()

    suspicious = (

        RawRecord.objects

        .filter(
            raw_data__suspicious=True
        )

        .count()

    )

    approved = (

        RawRecord.objects

        .filter(
            status="LOCKED"
        )

        .count()

    )

    if total == 0:

        score = 0

    else:

        score = round(

            (

                approved

                -

                suspicious

            )

            /

            total

            *

            100,

            1

        )

    return Response({

        "quality_score":

        max(
            score,
            0
        ),

        "total":
        total,

        "approved":
        approved,

        "suspicious":
        suspicious

    })

@api_view(["GET"])
def health(request):

    return Response({

        "status":
        "healthy",

        "records":

        RawRecord.objects.count(),

        "tenants":

        Tenant.objects.count(),

        "audits":

        AuditLog.objects.count()

    })



@api_view(["POST"])
def reject_record(request, id):

    record = RawRecord.objects.get(id=id)

    record.status = "REJECTED"

    record.save()

    AuditLog.objects.create(
        record=record,
        action="REJECTED"
    )

    return Response(
        {"message": "Rejected"}
    )

@api_view(["GET"])
def api_docs(request):

    return Response({

        "records":{

            "upload":
            "/api/v1/records/",

            "list":
            "/api/v1/records/list/?page=1",

            "approve":
            "/api/v1/records/<id>/approve/",

            "reject":
            "/api/v1/records/<id>/reject/"

        },

        "analytics":{

            "stats":
            "/api/v1/records/stats/",

            "quality":
            "/api/v1/records/quality/",

            "health":
            "/api/v1/records/health/"

        },

        "audit":{

            "logs":
            "/api/v1/records/audit/",

            "summary":
            "/api/v1/records/audit/summary/",

            "history":
            "/api/v1/records/<id>/history/"

        }

    })