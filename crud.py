import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import (
    db_manager,
    User,
    Profile,
    Post,
    Product,
    OrderProductAssociation,
)
from core.models.order import Order


async def create_user(username: str, session: AsyncSession) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user - ", user)
    return user


async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
    query = select(User).where(User.username == username)
    user: User | None = await session.scalar(statement=query)
    print("found user - ", user)
    return user


async def create_user_profile(
    user_id: int, first_name: str | None, last_name: str | None, session: AsyncSession
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profile(session: AsyncSession) -> list[User]:
    query = (
        select(User)
        .options(joinedload(User.profile))
        .order_by(User.id)
        .where(User.profile != None)
    )
    users = await session.scalars(query)

    for user in users:
        print(
            "User - ",
            user,
            " Profile - ",
            user.profile.first_name,
            user.profile.last_name,
        )
        print("*" * 12)

    return list(users)


async def create_post(
    user_id: int, session: AsyncSession, *post_tittles: str
) -> list[Post]:
    posts = [Post(user_id=user_id, tittle=post_tittle) for post_tittle in post_tittles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession) -> list[User]:
    query = select(User).options(selectinload(User.posts)).where(User.posts != None)
    users = await session.scalars(query)

    for user in users:
        print("User - ", user, "Posts: ")
        for post in user.posts:
            print(post.tittle)
        print("*" * 12)

    return list(users)


async def get_posts_with_user(session: AsyncSession) -> list[Post]:
    query = select(Post).options(joinedload(Post.user))
    posts = await session.scalars(query)

    for post in posts:
        print("Post - ", post, "User - ", post.user)

    return list(posts)


async def get_users_with_posts_and_profiles(session: AsyncSession) -> list[User]:
    query = select(User).options(joinedload(User.profile), selectinload(User.posts))
    users = await session.scalars(query)

    for user in users:
        print("User: ", user)
        print("Profile: ", user.profile)
        for post in user.posts:
            print("Posts: ")
            print("---", post)
        print("*" * 12)
        print()

    return list(users)


async def get_profiles_with_user_and_posts(session: AsyncSession) -> list[Profile]:
    query = select(Profile).options(joinedload(Profile.user).selectinload(User.posts))

    profiles = await session.scalars(query)

    for profile in profiles:
        print("Profile: ", profile)
        print("User: ", profile.user)
        print("Posts: ")
        for post in profile.user.posts:
            print("-----", post)

        print("*" * 12)
        print()

    return list(profiles)


async def create_order(session: AsyncSession, promo_code: str | None = None) -> Order:

    order = Order(promo_code=promo_code)
    session.add(order)
    await session.commit()
    print(order.id, order.created_at, order.promo_code)
    return order


async def create_product(
    session: AsyncSession, name: str, description: str, price: int
) -> Product:
    product = Product(name=name, description=description, price=price)

    session.add(product)
    await session.commit()
    print(product.id, product.name, product.description, product.price)
    return product


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    query = select(Order).options(
        selectinload(Order.products_details).joinedload(OrderProductAssociation.product)
    )
    orders = await session.scalars(query)

    for order in orders:
        print("Order: ", order.id, order.promo_code, order.created_at)
        print("---Products: ")
        for detail in order.products_details:
            print(
                "------------",
                detail.product.name,
                detail.id,
                detail.order_id,
                detail.product_id,
                detail.count,
                detail.unit_price,
            )
        print("*" * 30)
        print()

    return list(orders)


async def main():
    # session = db_manager.session_dep()
    async with db_manager.session_factory() as session:
        # await create_user(username="Ape", session=session)
        # await create_user(username="Grave", session=session)
        # user_YE = await get_user_by_username(username="YE", session=session)
        # user_ape = await get_user_by_username(username="Ape", session=session)
        # await create_user_profile(
        #     user_id=user_YE.id, first_name="Kanye", last_name="West", session=session
        # )
        # await create_user_profile(
        #     user_id=user_ape.id, first_name="Monkey", last_name="Smith", session=session
        # )
        # await show_users_with_profile(session=session)
        #
        # await create_post(user_YE.id, session, "SQL", "SQLMAP")
        # await create_post(user_ape.id, session, "FastApi", "Pydantic")
        product_one = await create_product(
            session=session, name="PS4", description="New console", price=500
        )

        product_two = await create_product(
            session=session, name="Xbox", description="Console of Microsoft", price=600
        )

        # --------------------------------------------
        order_one = await create_order(session=session)
        order_two_with_promo = await create_order(session=session, promo_code="hui")

        # --------------------------------------------
        order_one = await session.scalar(
            select(Order)
            .where(Order.id == order_one.id)
            .options(selectinload(Order.products_details))
        )
        order_two_with_promo = await session.scalar(
            select(Order)
            .where(Order.id == order_two_with_promo.id)
            .options(selectinload(Order.products_details))
        )

        # -----------------------------------------------
        order_one.products_details.append(
            OrderProductAssociation(
                product=product_one, count=10, unit_price=product_one.price
            )
        )
        order_two_with_promo.products_details.append(
            OrderProductAssociation(
                product=product_two, count=30, unit_price=product_two.price
            )
        )

        await session.commit()
        await get_orders_with_products(session=session)


if __name__ == "__main__":
    asyncio.run(main())
