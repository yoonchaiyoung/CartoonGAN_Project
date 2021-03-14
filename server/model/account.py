from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import bcrypt
from flask_jwt_extended import create_access_token
import datetime

bp_login = Blueprint("login", __name__, url_prefix="/login")
client = MongoClient("mongodb://[아이디]:[비밀번호]@[AWS호스팅주소]", 27017)
db = client.cartoon

# 로그인을 위해 계정찾기
def findAccount(id, pwd):
    id_check = list(db.Login.find({"id": id}))
    if len(id_check) == 0:
        return "이이디를 잘못입력하셨거나, 계정이 없습니다."

    else:
        encrypted_password = id_check[0]["pwd"]

        result = bcrypt.checkpw(pwd.encode("utf-8"), encrypted_password.encode("utf-8"))
        if result is True:
            return True
        else:
            return "비밀번호를 잘못입력하셨습니다."

# 아이디 중복검사 함수
def check_duplicate_id(id):
    id_check = list(db.Login.find({"id": id}))

    if len(id_check) == 0:
        return True
    else:
        return False

# 로그인
@bp_login.route("", methods=["POST"])
def login():
    id = request.form["id"]
    pwd = request.form["pwd"]

    result = findAccount(id, pwd)
    if result is True:
        # access_token, refresh_token 생성
        expires = datetime.timedelta(minutes=20)

        return jsonify(
            result="Success",
            id=id,
            access_token=create_access_token(identity=id, expires_delta=expires),
        ), 200

    else:
        return jsonify(
            result=result,
        )

# # 토큰 refresh
# @bp_login.route("/refresh", methods=["POST"])
# @jwt_refresh_token_required
# def refresh():
#     current_user = get_jwt_identity()
#     ret = {
#         "access_token": create_access_token(identity=current_user, expires_delta=1000 * 1200)
#     }
#     return jsonify(ret), 200

# 아이디 중복확인
@bp_login.route("/check_id/<id>", methods=["GET"])
def check_id(id):
    result = check_duplicate_id(id)
    if result is True:
        return jsonify(
            result="Success"
        )

    else:
        return jsonify(
            result="Fail"
        )

# 계정생성
@bp_login.route("/createAccount", methods=["POST"])
def createAccount():
    create_id = request.form["create_id"]
    create_pwd = request.form["create_pwd"]

    encrypted_password = bcrypt.hashpw(create_pwd.encode("utf-8"), bcrypt.gensalt())
    encrypted_password = encrypted_password.decode("utf-8")

    db.Login.insert(
        {
            "id": create_id,
            "pwd": encrypted_password,
        }
    )

    return jsonify(
        result="Success"
    )

# @bp_login.route("/test", methods=["POST"])
# def test():
#     pwd = request.form["pwd"]
#
#     encrypted_password = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
#     print(encrypted_password)
#
#     result = bcrypt.checkpw("1234".encode("utf-8"), encrypted_password)
#     print(result)
#
#     return jsonify(
#         {
#             "result": result
#         }
#     )
#
# @bp_login.route("/test2", methods=["POST"])
# def test2():
#     id = request.form["id"]
#     pwd = request.form["pwd"]
#
#     json = {
#         "id": id,
#         "pwd": pwd
#     }
#
#     encoded = jwt.encode(json, "secret-key", algorithm="HS256")
#     decoded = jwt.decode(encoded, "secret-key", algorithms="HS256")
#
#     print(encoded)
#     print(decoded)
#
#     return jsonify(
#         {
#             "result": decoded
#         }
#     )

