from core.database import SessionLocal
from models.medicine import Medicine


db = SessionLocal()

try:
    medicines = (
        db.query(Medicine)
        .filter(Medicine.medicine_name.ilike("%Dolo%"))
        .all()
    )

    if not medicines:
        print("❌ No Dolo medicine found.")
    else:
        for medicine in medicines:
            medicine.prescription_required = True
            print(
                f"✅ {medicine.medicine_name} "
                f"(ID: {medicine.id}) "
                f"→ Prescription Required = True"
            )

        db.commit()
        print("\n✅ Prescription requirement updated successfully.")

finally:
    db.close()