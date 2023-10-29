from werkzeug.security import generate_password_hash,check_password_hash
a=generate_password_hash("peashooter", method='pbkdf2:sha256')
print(check_password_hash(a,"peashooter"))