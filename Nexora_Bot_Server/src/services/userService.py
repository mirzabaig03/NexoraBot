from src.services.supabase import supabase


def ensure_user_exists(clerk_id: str):
    """
    Ensures a user row exists in the users table.
    Creates one if missing.
    """

    result = (
        supabase.table("users")
        .select("clerk_id")
        .eq("clerk_id", clerk_id)
        .execute()
    )

    if not result.data:
        insert_result = (
            supabase.table("users")
            .insert({"clerk_id": clerk_id})
            .execute()
        )

        if not insert_result.data:
            raise Exception("Failed to provision user in database")