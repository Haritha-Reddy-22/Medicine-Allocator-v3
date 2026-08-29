import sqlite3

from config.settings import DATABASE_PATH


def migrate_reservations():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    try:

        # ==========================================
        # CHECK EXISTING COLUMNS
        # ==========================================

        cursor.execute(
            "PRAGMA table_info(reservations)"
        )

        columns = [
            row[1]
            for row in cursor.fetchall()
        ]

        # ==========================================
        # ADD USER_ID
        # ==========================================

        if "user_id" not in columns:

            print(
                "Adding user_id column..."
            )

            # Existing reservations need a valid user.
            # We will temporarily assign them to the
            # first existing user.

            cursor.execute(
                "SELECT id FROM users ORDER BY id LIMIT 1"
            )

            first_user = cursor.fetchone()

            if not first_user:

                print(
                    "❌ No users found in database."
                )

                print(
                    "Please create at least one user "
                    "before running this migration."
                )

                return

            first_user_id = first_user[0]

            # SQLite doesn't allow adding a NOT NULL
            # column without a default to an existing table.
            #
            # So we add it with the first user's ID.
            cursor.execute(
                f"""
                ALTER TABLE reservations
                ADD COLUMN user_id INTEGER
                DEFAULT {first_user_id}
                """
            )

            connection.commit()

            print(
                "✅ user_id column added successfully."
            )

        else:

            print(
                "ℹ️ user_id column already exists."
            )

    except Exception as e:

        connection.rollback()

        print(
            f"❌ Migration failed: {e}"
        )

    finally:

        connection.close()


if __name__ == "__main__":

    migrate_reservations()