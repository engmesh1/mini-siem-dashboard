from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.api.v1.routes import router as v1_router

# Disable default docs so we can inject a custom credit badge in Swagger UI.
app = FastAPI(title=settings.app_name, docs_url=None, redoc_url=None)

# CORS (front-end later). Safe defaults for local dev.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix=settings.api_prefix)


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html() -> HTMLResponse:
    """Swagger UI with a bottom-right credit badge."""
    html = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{settings.app_name} - Swagger UI",
    ).body.decode("utf-8")

    credit_html = """
<div class="credit-badge">
  <div class="credit-badge__ar">إنشاء، تصميم، وتنفيذ: المهندس مشاري الخليفة</div>
  <div class="credit-badge__en">Created, Designed, and Implemented by: Engineer Meshari Al-Khalifah</div>
</div>
<style>
.credit-badge{position:fixed;bottom:12px;right:12px;z-index:99999;padding:10px 12px;border-radius:12px;background:rgba(255,255,255,.85);backdrop-filter:blur(6px);font-size:12px;line-height:1.25;opacity:.9;text-align:right;pointer-events:none;user-select:none;}
.credit-badge__ar{direction:rtl;unicode-bidi:plaintext;font-weight:600;}
.credit-badge__en{direction:ltr;unicode-bidi:plaintext;margin-top:4px;font-weight:500;}
</style>
"""

    # Inject before closing body tag.
    if "</body>" in html:
        html = html.replace("</body>", credit_html + "</body>")
    else:
        html += credit_html

    return HTMLResponse(html)


@app.get("/healthz")
def root_healthz() -> dict[str, str]:
    return {"status": "ok"}
