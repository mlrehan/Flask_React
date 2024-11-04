from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  FirstName = db.Column(db.String(50), nullable = False)
  LastName = db.Column(db.String(50), nullable = False)
  Email = db.Column(db.String(250), unique = True, nullable = False)
  Role = db.Column(db.String(50), nullable = False)
  Description = db.Column(db.Text)
  Gender = db.Column(db.String(10), default = "Male")
  PasswordHash = db.Column(db.String(500), nullable = False)
  Image_Url = db.Column(db.String(150))

  @property
  def password(self):
    raise AttributeError("Password is readony field")
  
  @password.setter
  def password(self, password):
    self.PasswordHash = generate_password_hash(password=password)

  def to_json(self):
    return {
      "id":self.id,
      "FirstName" : self.FirstName,
      "LastName" : self.LastName,
      "Email" : self.Email,
      "Role" : self.Role,
      "Description" : self.Description,
      "Gender" : self.Gender,
      "Image_Url" : self.Image_Url,
      "Password" : self.PasswordHash
    }
  
  def __repr__(self) -> str:
    return f"id: {self.id}; First Name: {self.FirstName}; Last Name: {self.LastName}; Email: {self.Email}"
  
  def check_password(self, password):
    return check_password_hash(pwhash = self.PasswordHash, password=password)