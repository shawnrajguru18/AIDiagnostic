"""
SQLAlchemy 2.0 async database models for the DXC AI Readiness Diagnostic V0.
Uses AsyncSession with SQLite-compatible types (JSON stored as Text).
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import AsyncGenerator, Optional

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import settings


# ---------------------------------------------------------------------------
# Engine + Session factory
# ---------------------------------------------------------------------------

# Convert sync SQLite URL to async (aiosqlite driver)
_raw_url: str = settings.database_url
if _raw_url.startswith("sqlite:///") and not _raw_url.startswith("sqlite+aiosqlite:///"):
    _async_url = _raw_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
else:
    _async_url = _raw_url

engine = create_async_engine(
    _async_url,
    echo=settings.environment == "development",
    connect_args={"check_same_thread": False} if "sqlite" in _async_url else {},
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ---------------------------------------------------------------------------
# Declarative Base
# ---------------------------------------------------------------------------


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Helper: JSON column serialisation for SQLite
# ---------------------------------------------------------------------------

def _json_dumps(obj: Optional[object]) -> Optional[str]:
    if obj is None:
        return None
    return json.dumps(obj)


def _json_loads(raw: Optional[str]) -> Optional[object]:
    if raw is None:
        return None
    return json.loads(raw)


# ---------------------------------------------------------------------------
# Table: prospects
# ---------------------------------------------------------------------------


class ProspectORM(Base):
    __tablename__ = "prospects"

    prospect_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str] = mapped_column(String(100), nullable=False)
    size_band: Mapped[str] = mapped_column(String(50), nullable=False)
    geography: Mapped[str] = mapped_column(String(50), nullable=False)
    primary_contact_name: Mapped[Optional[str]] = mapped_column(String(255))
    primary_contact_email: Mapped[Optional[str]] = mapped_column(String(255))
    primary_contact_title: Mapped[Optional[str]] = mapped_column(String(255))
    partner_id: Mapped[Optional[str]] = mapped_column(String(100))
    partner_name: Mapped[Optional[str]] = mapped_column(String(255))
    session_token: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    processing_status: Mapped[str] = mapped_column(String(50), default="pending")
    persona: Mapped[Optional[str]] = mapped_column(String(10))
    # Nested audit metadata stored as JSON text
    audit_json: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<ProspectORM prospect_id={self.prospect_id!r} company={self.company_name!r}>"


# ---------------------------------------------------------------------------
# Table: consent_records
# ---------------------------------------------------------------------------


class ConsentRecordORM(Base):
    __tablename__ = "consent_records"

    consent_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    prospect_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    consent_given: Mapped[bool] = mapped_column(Boolean, nullable=False)
    consent_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    consent_version: Mapped[str] = mapped_column(String(20), default="1.0")
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    data_retention_days: Mapped[int] = mapped_column(Integer, default=90)
    marketing_opt_in: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return (
            f"<ConsentRecordORM consent_id={self.consent_id!r} "
            f"prospect_id={self.prospect_id!r} given={self.consent_given}>"
        )


# ---------------------------------------------------------------------------
# Table: questionnaire_responses
# ---------------------------------------------------------------------------


class QuestionnaireResponseORM(Base):
    __tablename__ = "questionnaire_responses"

    response_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    prospect_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    questionnaire_id: Mapped[str] = mapped_column(String(36), nullable=False)
    # Full list of QuestionResponse objects serialised as JSON
    responses_json: Mapped[Optional[str]] = mapped_column(Text)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    time_to_complete_seconds: Mapped[Optional[int]] = mapped_column(Integer)

    def __repr__(self) -> str:
        return (
            f"<QuestionnaireResponseORM response_id={self.response_id!r} "
            f"prospect_id={self.prospect_id!r} completed={self.completed}>"
        )


# ---------------------------------------------------------------------------
# Table: research_outputs  (polymorphic: b1_financial, b2_news, b3_tech_stack)
# ---------------------------------------------------------------------------


class ResearchOutputORM(Base):
    __tablename__ = "research_outputs"

    research_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    prospect_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    # Discriminator: "b1_financial" | "b2_news" | "b3_tech_stack"
    output_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Full research output serialised as JSON
    data_json: Mapped[Optional[str]] = mapped_column(Text)
    confidence: Mapped[Optional[str]] = mapped_column(String(20))
    researched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<ResearchOutputORM research_id={self.research_id!r} "
            f"type={self.output_type!r} prospect_id={self.prospect_id!r}>"
        )


# ---------------------------------------------------------------------------
# Table: synthesis_outputs
# ---------------------------------------------------------------------------


class SynthesisOutputORM(Base):
    __tablename__ = "synthesis_outputs"

    synthesis_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    prospect_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    tier: Mapped[str] = mapped_column(String(50), nullable=False)
    # Full C2 SynthesisOutput serialised as JSON
    output_json: Mapped[Optional[str]] = mapped_column(Text)
    confidence: Mapped[str] = mapped_column(String(20), default="high")
    model_used: Mapped[str] = mapped_column(String(100), default="claude-opus-4-7")
    synthesized_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<SynthesisOutputORM synthesis_id={self.synthesis_id!r} "
            f"prospect_id={self.prospect_id!r} score={self.overall_score}>"
        )


# ---------------------------------------------------------------------------
# Table: quick_wins_outputs
# ---------------------------------------------------------------------------


class QuickWinsOutputORM(Base):
    __tablename__ = "quick_wins_outputs"

    output_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    prospect_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    # Full QuickWinsOutput serialised as JSON
    output_json: Mapped[Optional[str]] = mapped_column(Text)
    total_candidates_evaluated: Mapped[int] = mapped_column(Integer, default=0)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<QuickWinsOutputORM output_id={self.output_id!r} "
            f"prospect_id={self.prospect_id!r}>"
        )


# ---------------------------------------------------------------------------
# Table: scorecard_outputs
# ---------------------------------------------------------------------------


class ScorecardOutputORM(Base):
    __tablename__ = "scorecard_outputs"

    output_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    prospect_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    # Scorecard content serialised as JSON
    scorecard_content_json: Mapped[Optional[str]] = mapped_column(Text)
    quick_wins_memo_content_json: Mapped[Optional[str]] = mapped_column(Text)
    findings_appendix_content_json: Mapped[Optional[str]] = mapped_column(Text)
    # PDF artifact URLs
    scorecard_pdf_url: Mapped[Optional[str]] = mapped_column(String(2048))
    quick_wins_memo_pdf_url: Mapped[Optional[str]] = mapped_column(String(2048))
    findings_appendix_pdf_url: Mapped[Optional[str]] = mapped_column(String(2048))
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<ScorecardOutputORM output_id={self.output_id!r} "
            f"prospect_id={self.prospect_id!r}>"
        )


# ---------------------------------------------------------------------------
# Table: validation_outputs
# ---------------------------------------------------------------------------


class ValidationOutputORM(Base):
    __tablename__ = "validation_outputs"

    validation_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    prospect_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    overall_validation_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    # Full ValidationOutput serialised as JSON
    output_json: Mapped[Optional[str]] = mapped_column(Text)
    model_used: Mapped[str] = mapped_column(
        String(100), default="claude-haiku-4-5-20251001"
    )
    validated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<ValidationOutputORM validation_id={self.validation_id!r} "
            f"prospect_id={self.prospect_id!r} passed={self.overall_validation_passed}>"
        )


# ---------------------------------------------------------------------------
# Table: partner_review_records
# ---------------------------------------------------------------------------


class PartnerReviewRecordORM(Base):
    __tablename__ = "partner_review_records"

    review_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    prospect_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    partner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    partner_name: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    # Actions and training signals stored as JSON arrays
    actions_json: Mapped[Optional[str]] = mapped_column(Text)
    training_signals_json: Mapped[Optional[str]] = mapped_column(Text)
    review_started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    review_completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<PartnerReviewRecordORM review_id={self.review_id!r} "
            f"prospect_id={self.prospect_id!r} status={self.status!r}>"
        )


# ---------------------------------------------------------------------------
# Table: audit_log
# ---------------------------------------------------------------------------


class AuditLogORM(Base):
    __tablename__ = "audit_log"

    entry_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    prospect_id: Mapped[Optional[str]] = mapped_column(String(36), index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    actor: Mapped[str] = mapped_column(String(100), default="system")
    # Event details stored as JSON
    details_json: Mapped[Optional[str]] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(20), default="info")
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    session_id: Mapped[Optional[str]] = mapped_column(String(36))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))

    def __repr__(self) -> str:
        return (
            f"<AuditLogORM entry_id={self.entry_id!r} "
            f"event={self.event_type!r} actor={self.actor!r}>"
        )


# ---------------------------------------------------------------------------
# Session dependency (FastAPI)
# ---------------------------------------------------------------------------


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Async generator that yields an AsyncSession for use as a FastAPI dependency."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ---------------------------------------------------------------------------
# Database initialisation
# ---------------------------------------------------------------------------


async def init_db() -> None:
    """Create all tables if they do not yet exist.

    Call once at application startup (e.g. in the FastAPI lifespan handler).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
