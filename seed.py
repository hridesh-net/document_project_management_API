from sqlmodel import Session, select
from app.models import Role, Permission
from app.database import engine

def seed_roles_permissions():
    with Session(engine) as session:
        # Check for and create roles
        admin_role = session.exec(select(Role).where(Role.name == "admin")).first()
        user_role = session.exec(select(Role).where(Role.name == "user")).first()

        if not admin_role:
            admin_role = Role(name="admin", description="Admin with full permissions")
            session.add(admin_role)
        if not user_role:
            user_role = Role(name="user", description="User with read-only permissions")
            session.add(user_role)
        session.commit()

        # Check for and create permissions
        read_perm = session.exec(select(Permission).where(Permission.name == "read")).first()
        create_perm = session.exec(select(Permission).where(Permission.name == "create")).first()
        update_perm = session.exec(select(Permission).where(Permission.name == "update")).first()
        delete_perm = session.exec(select(Permission).where(Permission.name == "delete")).first()

        if not read_perm:
            read_perm = Permission(name="read", description="Read permission")
            session.add(read_perm)
        if not create_perm:
            create_perm = Permission(name="create", description="Create permission")
            session.add(create_perm)
        if not update_perm:
            update_perm = Permission(name="update", description="Update permission")
            session.add(update_perm)
        if not delete_perm:
            delete_perm = Permission(name="delete", description="Delete permission")
            session.add(delete_perm)
        session.commit()

        # Associate permissions with roles
        # Admin gets all permissions
        if read_perm not in admin_role.permissions:
            admin_role.permissions.append(read_perm)
        if create_perm not in admin_role.permissions:
            admin_role.permissions.append(create_perm)
        if update_perm not in admin_role.permissions:
            admin_role.permissions.append(update_perm)
        if delete_perm not in admin_role.permissions:
            admin_role.permissions.append(delete_perm)

        # User gets only read permission
        if read_perm not in user_role.permissions:
            user_role.permissions.append(read_perm)

        session.commit()
        print("Seed complete!")

if __name__ == "__main__":
    seed_roles_permissions()