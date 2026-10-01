import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "medicine_allocator.db"


def column_exists(cursor, table_name, column_name):

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = cursor.fetchall()

    return any(
        column[1] == column_name
        for column in columns
    )


def add_column_if_missing(
    cursor,
    table_name,
    column_name,
    column_definition
):

    if column_exists(
        cursor,
        table_name,
        column_name
    ):

        print(
            f"✓ {table_name}.{column_name} already exists."
        )

        return

    cursor.execute(
        f"""
        ALTER TABLE {table_name}
        ADD COLUMN {column_name}
        {column_definition}
        """
    )

    print(
        f"✓ Added {table_name}.{column_name}"
    )


def main():

    print("=" * 60)
    print("Prescription Feature Database Migration")
    print("=" * 60)

    print(f"Database: {DB_PATH}")

    if not DB_PATH.exists():

        print("❌ Database file not found.")

        return

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()

    try:

        # ======================================
        # MEDICINES
        # ======================================

        add_column_if_missing(
            cursor,
            "medicines",
            "prescription_required",
            "BOOLEAN NOT NULL DEFAULT 0"
        )

        # ======================================
        # RESERVATIONS
        # ======================================

        add_column_if_missing(
            cursor,
            "reservations",
            "prescription_path",
            "VARCHAR(500)"
        )

        add_column_if_missing(
            cursor,
            "reservations",
            "prescription_status",
            "VARCHAR(50) NOT NULL DEFAULT 'Not Required'"
        )

        connection.commit()

        print()
        print("✅ Prescription database migration completed.")

    except Exception as e:

        connection.rollback()

        print()
        print("❌ Migration failed:")
        print(e)

    finally:

        connection.close()


if __name__ == "__main__":
    main()