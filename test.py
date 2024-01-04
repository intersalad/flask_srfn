from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client
from gotrue.errors import AuthApiError

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)





#email = "vladvolkov06@yandex.ru"
#password= "intersalad"
#user = supabase.auth.sign_up({ "email": email, "password": password })

#session = None

#try:
#    session = supabase.auth.sign_in_with_password({ "email": email, "password": password })
#    print(session)
#except:
#    print("login failed")




#data = supabase.table("users").insert({"name":"vlad"}).execute()
#data = supabase.table("users").update({"name": "new_name"}).eq("id", 8).execute()
#print(data)


