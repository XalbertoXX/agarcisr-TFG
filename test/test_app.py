import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Test Supabase connection function
def test_supabase_connection():
    # Check if Supabase credentials are available or else skip test
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase credentials not available")
        return  

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table("protocols").select("*").limit(1).execute()

    assert response is not None
    assert hasattr(response, "data")

# Main execution
if __name__ == "__main__":
    try:
        test_supabase_connection()
        print("Success!")
    except Exception as e:
        print(f"Failed to connect: {e}")