from flask import Blueprint,jsonify, request
from models import User, db

views = Blueprint('views', __name__)

@views.route('/api/users', methods = ['GET'])
def get_users():
  users = User.query.all()
  result = [user.to_json() for user in users]
  return jsonify(result)

@views.route('/api/createuser', methods = ['POST'])
def create_user():
  try:
    data = request.json

    required_fields = ['FirstName','LastName','Email','password']
    for field in required_fields:
      if field not in data:
          error_message = f"{field} is a required field!!"
          print(error_message)  # This will show in the console
          return jsonify({"error": error_message}), 400

    firstname = data.get('FirstName')
    lastname = data.get('LastName')
    email = data.get('Email')
    role = data.get('Role')
    gender = data.get('Gender')
    description = data.get('Description')
    password = data.get('password')
    if gender == "Female":
      image_url = f"https://avatar.iran.liara.run/public/girl?username={firstname}"
    elif gender == "Male":
      image_url = f"https://avatar.iran.liara.run/public/boy?username={firstname}"
    else:
      image_url = None

    new_user = User(FirstName = firstname, LastName = lastname, Email = email, Role = role, Gender = gender, Description = description, password=password, Image_Url = image_url)
    db.session.add(new_user)
    db.session.commit()    
    return jsonify({"success": "A new user has been created successfully"}), 201
  except Exception as e:
    db.session.rollback()
    print(str(e))
    return jsonify({"error": f"Unable to create user, error: {str(e)}"}), 500

@views.route('/api/updateuser/<int:id>', methods = ['PUT'])
def update_user(id):
  try:
    user = User.query.get(id)
    if not user:
      return jsonify({'error':'User not found!!'}),400
    data = request.json

    user.FirstName = data.get('FirstName', user.FirstName)
    user.LastName = data.get('LastName', user.LastName)
    user.Email = data.get('Email', user.Email)
    user.Role = data.get('Role',user.Role)
    user.Description = data.get('Description', user.Description)
    user.Gender = data.get('Gender', user.Gender)
    if user.Gender == "Female":
      user.Image_Url = f"https://avatar.iran.liara.run/public/girl?username={user.FirstName}"
    elif user.Gender == "Male":
      user.Image_Url = f"https://avatar.iran.liara.run/public/boy?username={user.FirstName}"
    else:
      user.Image_Url = None
    
    db.session.commit()
    return jsonify(user.to_json()),201
  except Exception as e:
    db.session.rollback()
    return jsonify({"error":f"Error: {str(e)}"}), 500

@views.route('/api/deleteuser/<int:id>', methods = ['DELETE'])
def delete_user(id):
  try:
    user = User.query.get(id)
    if not user:
      return jsonify({"error":f"Error: User not found!!"}),400
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success":f"User has been deleted successfully"}),201
  except Exception as e:
    db.session.rollback()
    return jsonify({"error":f"Error: {str(e)}"}),500