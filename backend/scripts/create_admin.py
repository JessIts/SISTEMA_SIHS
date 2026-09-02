from app.core.database import SessionLocal
from app.services.user_service import UserService


from app.core.database import SessionLocal
from app.services.user_service import UserService

def create_admin(
    email: str,
    db,
    service,
    ):
    user = service.repository.get_by_email(email)


    if not user:
        print(f"No existe ningún usuario con el correo: {email}")
        return None

    if user.role.value == "admin":
        print(f"El usuario {email} ya es administrador.")
        return user

    user = service.promote_to_admin(user.uuid)

    print(f"Usuario {email} promovido correctamente a ADMIN.")
    print(f"UUID: {user.uuid}")
    print(f"Rol: {user.role.value}")

    return user


def main():
    import sys


    if len(sys.argv) < 2:
        raise SystemExit(
            "Debe proporcionar el correo electrónico del usuario."
        )

    email = sys.argv[1]

    db = SessionLocal()

    try:
        service = UserService(db)

        return create_admin(
            email=email,
            db=db,
            service=service,
        )

    finally:
        db.close()


if __name__== "__main__":
    main()
