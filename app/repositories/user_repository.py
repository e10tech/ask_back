from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserGoogleAccount, UserLocalAccount
from app.core.security import now_utc


async def get_user_with_local_account(
    db: AsyncSession, login_id: str
) -> tuple[User | None, UserLocalAccount | None]:
    stmt = (
        select(User, UserLocalAccount)
        .join(UserLocalAccount, UserLocalAccount.user_id == User.id)
        .where(UserLocalAccount.login_id == login_id)
    )
    result = await db.execute(stmt)
    row = result.first()
    if not row:
        return None, None
    return row[0], row[1]


async def get_user_by_google_sub(
    db: AsyncSession, google_sub: str
) -> tuple[User | None, UserGoogleAccount | None]:
    stmt = (
        select(User, UserGoogleAccount)
        .join(UserGoogleAccount, UserGoogleAccount.user_id == User.id)
        .where(UserGoogleAccount.google_sub == google_sub)
    )
    result = await db.execute(stmt)
    row = result.first()
    if not row:
        return None, None
    return row[0], row[1]


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def upsert_google_account(
    db: AsyncSession, user: User, google_sub: str, google_email: str | None
) -> UserGoogleAccount:
    existing, google_account = await get_user_by_google_sub(db, google_sub)
    if existing and google_account:
        return google_account
    stmt = select(UserGoogleAccount).where(UserGoogleAccount.user_id == user.id)
    res = await db.execute(stmt)
    account = res.scalar_one_or_none()
    if account:
        account.google_sub = google_sub
        account.google_email = google_email
    else:
        account = UserGoogleAccount(
            user_id=user.id, google_sub=google_sub, google_email=google_email
        )
        db.add(account)
    await db.flush()
    return account


async def touch_local_login(db: AsyncSession, local_account: UserLocalAccount) -> None:
    stmt = (
        update(UserLocalAccount)
        .where(UserLocalAccount.user_id == local_account.user_id)
        .values(last_login_at=now_utc())
    )
    await db.execute(stmt)
