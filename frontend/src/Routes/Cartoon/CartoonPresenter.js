import React from "react";
import Helmet from "react-helmet";
import styled, { keyframes } from "styled-components";
import BeforeTransfer from "./BeforeTransfer";
import AfterTransfer from "./AfterTransfer";
import Loading from "../../Components/Loading";

const initAnimation = keyframes`
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
`;

const Cartoon = styled.div`
  width: 100%;
  height: 100vh;

  position: absolute;
  top: 0;
  left: 0;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  background: #222831;

  .cartoonContainer {
    width: 100%;
    height: 100%;

    animation: ${initAnimation} 1s ease-in;
  }
`;

const CartoonPresenter = ({
  images,
  filter,
  _handleOnDragEnter,
  _handleOnDragLeave,
  _handleOnDragOver,
  _handleOnDrop,
  _handleOnClick,
  _handleOnUpload,
  _handleImageDelete,
  _handleSelectFilter,
  _handleImageTransition,
  loading,
  transition,
  cartoonImages,
  mainImage,
  _handleSelectMainImage,
  _handleImagesDownload,
  _handleReset,
}) => {
  return (
    <>
      <Helmet>
        <title>ARTWORKER | 이미지변환</title>
      </Helmet>
      <Cartoon>
        <div className="cartoonContainer">
          {loading ? (
            <Loading text={"이미지 변환중..."} usage={"transfer"}/>
          ) : // FIXME: 이미지 변환 후
          transition ? (
            <AfterTransfer
              cartoonImages={cartoonImages}
              mainImage={mainImage}
              _handleReset={_handleReset}
              _handleSelectMainImage={_handleSelectMainImage}
              _handleImagesDownload={_handleImagesDownload}
            />
          ) : (
            // FIXME: 이미지 변환 전
            <BeforeTransfer
              images={images}
              filter={filter}
              _handleOnDragEnter={_handleOnDragEnter}
              _handleOnDragLeave={_handleOnDragLeave}
              _handleOnDragOver={_handleOnDragOver}
              _handleOnDrop={_handleOnDrop}
              _handleOnClick={_handleOnClick}
              _handleOnUpload={_handleOnUpload}
              _handleImageDelete={_handleImageDelete}
              _handleSelectFilter={_handleSelectFilter}
              _handleImageTransition={_handleImageTransition}
            />
          )}
        </div>
      </Cartoon>
    </>
  );
};

export default CartoonPresenter;
