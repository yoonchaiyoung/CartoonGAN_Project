import React from "react";
import { Link } from "react-router-dom";
import "../../Style/Transfer/AfterTransfer.css";

const AfterTransfer = ({
  cartoonImages,
  mainImage,
  _handleReset,
  _handleSelectMainImage,
  _handleImagesDownload,
}) => {
  return (
    <div className="result_container">
      <div className="reset_box">
        <ion-icon name="arrow-back-outline" onClick={_handleReset}></ion-icon>
      </div>
      <div className="content_container">
        <div className="smallImage_container">
          {cartoonImages.map((cartoonImage) => (
            <img
              key={cartoonImage.id}
              name={cartoonImage.id}
              src={cartoonImage.imageURL}
              onClick={_handleSelectMainImage}
              alt="보조이미지"
            />
          ))}
        </div>
        <div className="mainImage_container">
          <img src={mainImage.imageURL} alt="메인이미지" />
        </div>
        <div className="result_buttons">
          <Link className="result_button" to="/gallery">
            이미지 갤러리
          </Link>
          <button className="result_button" onClick={_handleImagesDownload}>
            이미지 다운로드
          </button>
        </div>
      </div>
    </div>
  );
};

export default AfterTransfer;
