import React from "react";
import "../../../Style/Gallery/Image.css";

const PublicImageComponent = ({
  publicImage,
  _handleSelectDetailImage,
  _handleDownloadImage,
}) => {
  const { filter, imageURL, date, like } = publicImage;

  return (
    <>
      <div
        className="private_image"
        onClick={(e) => _handleSelectDetailImage(e, publicImage)}
      >
        <img src={imageURL} alt="개인이미지"></img>
        <div className="private_image_overlay"></div>
        <div className="private_image_desc">
          <p>사용된 필터 : {filter}</p>
          <p>추천 수 : {like}</p>
          <p>{date}</p>
        </div>
      </div>
    </>
  );
};

export default PublicImageComponent;
