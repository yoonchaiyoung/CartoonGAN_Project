import React from "react";
import "../../../Style/Gallery/Image.css";

const PrivateImageComponent = ({
  privateImage,
  _handleMovePublicImage,
  _handleMovePrivateImage,
  _handleDeleteImage,
  _handleSelectDetailImage,
  _handleDownloadImage,
}) => {
  const { id, imageId, filter, imageURL, date, isPublic, like } = privateImage;

  return (
    <>
      <div
        className="private_image"
        onClick={(e) => _handleSelectDetailImage(e, privateImage)}
      >
        <img src={imageURL} alt="개인이미지"></img>
        <div className="private_image_desc">
          <p>사용된 필터 : {filter}</p>
          <p>추천 수 : {like}</p>
          <p>{date}</p>
        </div>
        <div className="private_image_options">
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
          <ion-icon
            name="download-outline"
            onClick={(e) => _handleDownloadImage(e, imageId, imageURL)}
          ></ion-icon>
        </div>
        <div className="private_image_overlay"></div>
      </div>
    </>
  );
};

export default PrivateImageComponent;
