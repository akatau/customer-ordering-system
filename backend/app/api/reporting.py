"""Reporting API endpoints for admin analytics."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from ..database import get_db
from ..services.reporting_service import ReportingService
from ..schemas.support import (
    SalesReport,
    InventoryReport,
    CustomerAnalytics,
    ReportExportRequest,
    ReportExportResponse,
)
from .deps import require_admin

router = APIRouter(prefix="/admin/reports", tags=["reports"])


@router.get("/sales", response_model=SalesReport)
def get_sales_report(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_admin = Depends(require_admin),
):
    """Get sales analytics report."""
    return ReportingService.sales_report(db, start_date, end_date)


@router.get("/inventory", response_model=InventoryReport)
def get_inventory_report(
    db: Session = Depends(get_db),
    current_admin = Depends(require_admin),
):
    """Get inventory status report."""
    return ReportingService.inventory_report(db)


@router.get("/customers", response_model=CustomerAnalytics)
def get_customer_analytics(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_admin = Depends(require_admin),
):
    """Get customer analytics report."""
    return ReportingService.customer_analytics(db, start_date, end_date)


@router.post("/export", response_model=ReportExportResponse)
def export_report(
    request: ReportExportRequest,
    db: Session = Depends(get_db),
    current_admin = Depends(require_admin),
):
    """Export a report in CSV or JSON format."""
    try:
        export_data = ReportingService.export_report(
            db,
            request.report_type,
            request.start_date,
            request.end_date,
            request.format,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ReportExportResponse(format=export_data["format"], content=export_data["content"])
