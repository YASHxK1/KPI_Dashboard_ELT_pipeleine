"""
Web module – Flask routes and application factory.

Keeps the web layer thin: it only handles request parsing and
template rendering, delegating all business logic to metrics.py.
"""

import json
import logging

from flask import Flask, render_template, request

from metrics import calculate_kpis, get_filter_options

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Application factory – returns a configured Flask app."""
    app = Flask(__name__)

    @app.route("/")
    def dashboard():
        """Main dashboard view with optional query-string filters."""
        category = request.args.get("category") or None
        region = request.args.get("region") or None
        date_from = request.args.get("date_from") or None
        date_to = request.args.get("date_to") or None

        kpis = calculate_kpis(
            category=category,
            region=region,
            date_from=date_from,
            date_to=date_to,
        )
        filters = get_filter_options()

        # Serialise DataFrames → JSON for Chart.js
        trend_json = kpis["monthly_trend"].to_json(orient="records")
        category_json = kpis["sales_by_category"].to_json(orient="records")

        return render_template(
            "dashboard.html",
            kpis=kpis,
            filters=filters,
            selected={
                "category": category,
                "region": region,
                "date_from": date_from,
                "date_to": date_to,
            },
            trend_json=trend_json,
            category_json=category_json,
        )

    @app.route("/health")
    def health():
        """Lightweight health-check endpoint."""
        return {"status": "ok"}, 200

    return app
