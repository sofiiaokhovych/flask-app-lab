from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[Optional[str]] = mapped_column(
        Enum("news", "publication", "tech", "other", name="post_category")
    )
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post(title={self.title})>"