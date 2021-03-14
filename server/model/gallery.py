from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import uuid

bp_gallery = Blueprint("gallery", __name__, url_prefix="/gallery")
# client = MongoClient("mongodb://127.0.0.1", 27017)
client = MongoClient("mongodb://luckycontrol:qlqjsdlek!@3.133.138.156", 27017)
db = client.cartoon

# FIXME: 개인 갤러리에 저장
def imageSave(id, filter, image):
    db.gallery.insert(
        {
            "id": id,
            "imageId": str(uuid.uuid4()),
            "filter": filter,
            "imageURL": str(image),
            "date": str(datetime.now()),
            "isPublic": False,
            "like": 0
        }
    )

# FIXME: 이미지 전송 전 포장..
def imageSetting(private_data):
    private_images = []
    for image in private_data:
        private = {
            "id": image["id"],
            "imageId": image["imageId"],
            "filter": image["filter"],
            "imageURL": image["imageURL"],
            "date": image["date"].split(' ')[0],
            "isPublic": image["isPublic"],
            "like": image["like"],
        }
        private_images.append(private)

    return private_images

# TODO: 개인 갤러리에서 이미지 가져오기
@bp_gallery.route("/getPrivate", methods=["POST"])
def getPrivate():
    id = request.form["id"]
    sort = request.form["sort"]

    if sort == "최신순":
        private_data = list(db.gallery.find({"id": id}).sort("date", -1))

    elif sort == "추천순":
        private_data = list(db.gallery.find({"id": id}).sort("like", -1))

    else:
        private_data = list(db.gallery.find({"id": id, "filter": "신카이 마코토"}))

    private_images = imageSetting(private_data)

    return jsonify(
        result="OK",
        private_images=private_images,
    ), 200

# TODO: 개인 갤러리 이미지를 공유 -> isPublic - True
@bp_gallery.route("/share", methods=["POST"])
def imageShare():
    id = request.form["id"]
    imageId = request.form["imageId"]

    query = {"id": id, "imageId": imageId}
    newValues = {"$set": {"isPublic": True}}

    db.gallery.update_one(query, newValues)

    return jsonify(
        result='OK',
    ), 200

# TODO: 개인 갤러리 이미지 삭제
@bp_gallery.route("/delete", methods=["POST"])
def imageDelete():
    id = request.form["id"]
    imageId = request.form["imageId"]

    db.gallery.delete_one({"id": id, "imageId": imageId})

    return jsonify(
        result="OK"
    ), 200

@bp_gallery.route("/getPrivateByFilter", methods=["POST"])
def getPrivateByFilter():
    id = request.form["id"]
    filter = request.form["filter"]

    result = list(db.gallery.find({"id": id, "filter": filter}))
    filter_images = imageSetting(result)

    return jsonify(
        result="OK",
        filter_images=filter_images,
    ), 200

# FIXME: 공개갤러리 이미지 가져오기
@bp_gallery.route("/getPublic", methods=["POST"])
def getPublic():
    sort = request.form["sort"]

    if sort == "최신순":
        public_data = list(db.gallery.find({"isPublic": True}).sort("date", -1))

    elif sort == "추천순":
        public_data = list(db.gallery.find({"isPublic": True}).sort("like", -1))

    else:
        public_data = imageSetting(list(db.gallery.find({"isPublic": True, "filter": "신카이 마코토"})))

    public_images = imageSetting(public_data)

    return jsonify(
        result="OK",
        private_images=public_images,
    ), 200

# TODO: 공개 갤러리에서 내리기 -> isPublic - False
@bp_gallery.route("/unshare", methods=["POST"])
def imageUnshare():
    id = request.form["id"]
    imageId = request.form["imageId"]

    query = {"id": id, "imageId": imageId}
    newValues = {"$set": {"isPublic": False}}

    db.gallery.update_one(query, newValues)

    return jsonify(
        result="OK"
    ), 200

# TODO: 공개 갤러리 이미지 추천
@bp_gallery.route("/like", methods=["POST"])
def imageLike():
    pass

@bp_gallery.route("/getPublicByFilter", methods=["POST"])
def getPublicByFilter():
    filter = request.form["filter"]

    result = list(db.gallery.find({"isPublic": True, "filter": filter}))
    filter_images = imageSetting(result)

    return jsonify(
        result="OK",
        filter_images=filter_images
    ), 200


