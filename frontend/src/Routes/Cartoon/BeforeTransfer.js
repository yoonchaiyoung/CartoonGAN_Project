import React, { useMemo } from "react";
import "../../Style/Transfer/BeforeTransfer.css";

const BeforeTransfer = ({
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
}) => {
  const filters = useMemo(
    () => ["신카이 마코토", "미야자키 하야오", "호소 다 마모루"],
    []
  );
  return (
    <>
      <div className="input_container">
        <div className="filters">
          {filters.map((filter) => (
            <div id={filter} key={filter} className="filter">
              <button
                key={filter}
                name={filter}
                onClick={(e) => _handleSelectFilter(e, filter)}
              >
                {filter}
              </button>
            </div>
          ))}
        </div>
        <div className="input_box">
          <div
            className="drag_box"
            onDragEnter={_handleOnDragEnter}
            onDragLeave={_handleOnDragLeave}
            onDragOver={_handleOnDragOver}
            onDrop={_handleOnDrop}
            onClick={_handleOnClick}
          >
            <input
              id="fileElem"
              type="file"
              multiple
              accept="image/*"
              onChange={_handleOnUpload}
            ></input>
            <p className="drag_navigate">이곳에 드래그하여 옮겨주세요!</p>
            {images.length > 0 && (
              <div className="image_grid">
                {images.map((image) => (
                  <img
                    draggable="false"
                    key={image.id}
                    id={image.id}
                    src={image.imageURL}
                    onClick={_handleImageDelete}
                    alt="변환할 이미지"
                  ></img>
                ))}
              </div>
            )}
          </div>
          {filter !== "" ? (
            <p className="filter_paragraph">적용될 필터 : {filter}</p>
          ) : null}
          <button className="translate_btn" onClick={_handleImageTransition}>
            이미지 변환
          </button>
        </div>
      </div>
    </>
  );
};

export default BeforeTransfer;
