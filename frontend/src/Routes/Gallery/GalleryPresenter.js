import React from "react";
import "../../Style/Gallery/Gallery.css";
import PublicGallery from "./PublicGallery/PublicGallery";
import PrivateGallery from "./PrivateGallery/PrivateGallery";
import Helmet from "react-helmet";

const Gallery = ({
  title,
  _handleGalleryCategory,
  _handleClickSortingWayTitle,
  sort,
  _handleSortingWay,
  filters,
}) => {
  return (
    <>
      <Helmet>
        <title>ARTWORKER | 갤러리</title>
      </Helmet>
      <div className="gallery_container">
        <p className="gallery_title">{title}</p>
        <div className="gallery_category">
          <span
            className="gallery_category_item is-active"
            active-color="white"
            id="공개갤러리"
            onClick={_handleGalleryCategory}
          >
            공개갤러리
          </span>
          <span
            className="gallery_category_item"
            active-color="blue"
            id="개인갤러리"
            onClick={_handleGalleryCategory}
          >
            개인갤러리
          </span>
        </div>
        <div className="sortingway_dropdown_container">
          <button
            className="sortingway_text"
            onClick={_handleClickSortingWayTitle}
          >
            정렬방법 - {sort}
          </button>

          <div className="sortingway_dropdown_items">
            <button
              className="sortingway_dropdown_item"
              name="최신순"
              onClick={_handleSortingWay}
            >
              최신순
            </button>
            <button
              className="sortingway_dropdown_item"
              name="필터별"
              onClick={_handleSortingWay}
            >
              필터별
            </button>
            <button
              className="sortingway_dropdown_item"
              name="추천순"
              onClick={_handleSortingWay}
            >
              추천순
            </button>
          </div>
        </div>
        <div className="gallery_content">
          {title === "공개갤러리" ? (
            <PublicGallery filters={filters} sort={sort} />
          ) : (
            <PrivateGallery filters={filters} sort={sort} />
          )}
        </div>
      </div>
    </>
  );
};

export default Gallery;
