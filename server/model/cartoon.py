from flask import Blueprint, request, jsonify
import uuid
from PIL import Image
from io import BytesIO
from datauri import DataURI
import tensorflow as tf
import os

bp_cartoon = Blueprint("cartoon", __name__, url_prefix="/cartoon")

"""
FLOW
1. 이미지를 입력받는다.
2. uuid-이미지이름 으로 저장한다.
3. 이미지를 변환한다.
4. 변환된 이미지를 보낸다.
5. 저장한 이미지들을 삭제한다.
"""
@bp_cartoon.route("/transition", methods=["POST"])
def imageTransition():
    id = request.form["id"]
    filter = request.form["filter"]
    image_length = int(request.form["image_length"])
    input_images_dataURI = [DataURI(request.form[f"image{i}"]).data for i in range(image_length)]

    # # FIXME: uuid-인덱스 로 이미지 저장
    user_uuid = uuid.uuid4()
    os.makedirs(f'./{user_uuid}/before')
    os.makedirs(f'./{user_uuid}/after')

    for idx in range(image_length):
        im = Image.open(BytesIO(input_images_dataURI[idx]))
        im = im.convert('RGB')

        im.save(f'{user_uuid}/before/image{idx}.jpg')

    # TODO: 이미지 변환
    from whitebox import cartoonize
    model_path = 'saved_models'
    location = f'{user_uuid}'

    cartoonize.cartoonize(location, model_path)

    from model import gallery

    output_images_dict = {}
    for idx in range(image_length):
        # FIXME: 이미지를 datauri로 변경
        translated_image = DataURI.from_file(f'./{user_uuid}/after/image{idx}.jpg')

        # FIXME: 회원일 경우 이미지를 개인 갤러리에 저장
        if id != 'Not User':
            gallery.imageSave(id, filter, translated_image)

        # FIXME: 변환된 이미지를 클라이언트에게 보내기 위해..
        output_images_dict[f'image{idx}'] = translated_image

        os.remove(f'./{user_uuid}/before/image{idx}.jpg')
        os.remove(f'./{user_uuid}/after/image{idx}.jpg')

    # FIXME: 저장된 이미지 삭제
    os.rmdir(f'./{user_uuid}/before')
    os.rmdir(f'./{user_uuid}/after')
    os.removedirs(f'./{user_uuid}')

    # FIXME: 이미지들 전송
    return jsonify(
        result="OK",
        imageLength=image_length,
        cartoonImages=output_images_dict,
    )
