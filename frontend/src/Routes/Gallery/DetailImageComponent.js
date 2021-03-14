import React from "react";
import "../../Style/Gallery/DetailImage.css";

const DetailImageComponent = ({
  type,
  detailImage,
  _handleCancelDetailImage,
  _handleMovePublicImage,
  _handleMovePrivateImage,
  _handleDeleteImage,
  _handleDownloadImage,
}) => {
  const { id, imageId, filter, imageURL, date, isPublic, like } = detailImage;

  return (
    <>
      <div className="detail_image_container">
        <ion-icon
          className="cancel_detail_image"
          name="close-outline"
          onClick={_handleCancelDetailImage}
        ></ion-icon>
        <div className="detail_image_box">
          <div className="detail_image_options">
            {type === "private" && (
              <>
                <ion-icon
                  id={`${id}/${imageId}`}
                  name="close-circle-outline"
                  onClick={_handleDeleteImage}
                ></ion-icon>

                {isPublic === true ? (
                  <ion-icon
                    id={`${id}/${imageId}`}
                    name="cloud-download-outline"
                    onClick={_handleMovePrivateImage}
                  ></ion-icon>
                ) : (
                  <ion-icon
                    id={`${id}/${imageId}`}
                    name="cloud-upload-outline"
                    onClick={_handleMovePublicImage}
                  ></ion-icon>
                )}
              </>
            )}

            <ion-icon
              name="download-outline"
              onClick={(e) => _handleDownloadImage(e, imageId, imageURL)}
            ></ion-icon>
          </div>
          <img src={imageURL} alt="이미지"></img>
          <div className="detail_image_desc">
            <p>사용된 필터 : {filter}</p>
            <p>추천 수 : {like}</p>
            <p>{date}</p>
          </div>
        </div>
      </div>
    </>
  );
};

export default DetailImageComponent;
