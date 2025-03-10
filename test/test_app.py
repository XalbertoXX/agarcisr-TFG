import os
from supabase import create_client, Client

# You should store these in environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def test_supabase_connection():
    """Test that we can connect to Supabase database."""
    # Skip test if credentials aren't available
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase credentials not available")
    
    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Test a simple query to verify connection
    response = supabase.table("your_table_name").select("*").limit(1).execute()
    
    # If we get here without exception, connection works
    assert response is not None
    assert hasattr(response, "data")

if __name__ == "__main__":
    # For manual execution
    try:
        test_supabase_connection()
        print("✅ Successfully connected to Supabase database")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")