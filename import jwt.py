import jwt

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczNjE4MDY1NCwianRpIjoiNDA0MWQxYTctNmZkZS00MWIzLWEwMTEtMDIxM2EwOWMwYWJhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImpzbWl0aEBwbHltb3V0aC5hYy51ayIsIm5iZiI6MTczNjE4MDY1NCwiY3NyZiI6ImZhZjg2YjAwLWQ0YjktNGFjZC05NmM0LTdmNmI1YzIxYTI4MSIsImV4cCI6MTczNjE4NjA1NCwicm9sZSI6ImFkbWluIn0.zhGiNwmhHQcFtMWsPB5MkOQsZWqe1BtcKQAeX8GNGd8"

decoded_token = jwt.decode(token, options={"verify_signature": False})
print(decoded_token)