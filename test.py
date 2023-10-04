from werkzeug.security import generate_password_hash,check_password_hash
passw = "pakaya"
hashed=generate_password_hash(passw, method='pbkdf2:sha256')
passw2= "pakaya"
print(check_password_hash(hashed,passw2))