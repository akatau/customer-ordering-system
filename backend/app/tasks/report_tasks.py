from datetime import datetime, timedelta
from ..core.celery_app import celery_app
from ..database import SessionLocal
from ..services.reporting_service import ReportingService


@celery_app.task(name="tasks.generate_daily_sales_report")
def generate_daily_sales_report():
    """Generate the daily sales report."""
    now = datetime.utcnow()
    start_date = now - timedelta(days=1)
    end_date = now

    with SessionLocal() as db:
        report = ReportingService.sales_report(db, start_date=start_date, end_date=end_date)
        # In a real implementation, we would store or send the report.
        return report


@celery_app.task(name="tasks.generate_inventory_report")
def generate_inventory_report():
    """Generate the inventory report."""
    with SessionLocal() as db:
        return ReportingService.inventory_report(db)


@celery_app.task(name="tasks.generate_customer_analytics_report")
def generate_customer_analytics_report():
    """Generate the customer analytics report."""
    now = datetime.utcnow()
    start_date = now - timedelta(days=30)
    end_date = now

    with SessionLocal() as db:
        return ReportingService.customer_analytics(db, start_date=start_date, end_date=end_date)
