import React, { useEffect, useState, useCallback } from "react";
import { galleryApi } from "../../../api";
import PublicImageComponent from "./PublicImageComponent";
import "../../../Style/Gallery/PrivateGalleryStyle.css";
import DetailImageComponent from "../DetailImageComponent";
import Loading from "../../../Components/Loading";

const PublicGallery = ({ sort }) => {
  const [publicImages, setPublicImages] = useState([]);
  const [detailImageState, setDetailImageState] = useState(false);
  const [detailImage, setDetailImage] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const getPublicData = async () => {
      setLoading(true);
      let data = await galleryApi.getPublic(sort);

      let {
        data: { private_images },
      } = data;

      setPublicImages(private_images);
      setLoading(false);
    };

    getPublicData();
  }, [sort]);

  // FIXME: 필터 선택 및 데이터 가져오기
  const _handleSelectFilter = useCallback((e) => {
    // 필터에 맞는 데이터 가져오기
    const getFilterData = async () => {
      let data = await galleryApi.getPublicByFilter(e.target.name);
      let {
        data: { filter_images },
      } = data;

      setPublicImages(filter_images);
    };

    // 데이터 수정하기
    getFilterData();

    // 하단 밑줄 수정하기
    const filter_btns = document.getElementsByClassName("filter_btn");
    for (let filter of filter_btns) {
      if (filter.classList.length > 1) {
        filter.classList.toggle("is-selected");
        break;
      }
    }

    e.target.classList.toggle("is-selected");
  }, []);

  // FIXME: 선택한 이미지 자세히보기
  const _handleSelectDetailImage = useCallback((e, detailImage) => {
    e.stopPropagation();
    e.preventDefault();

    const body = document.getElementsByTagName("body")[0];
    body.classList.toggle("not-scroll");

    setDetailImage(detailImage);
    setDetailImageState(true);
  }, []);

  // FIXME: 선택한 이미지 자세히보기 취소
  const _handleCancelDetailImage = useCallback((e) => {
    e.stopPropagation();
    e.preventDefault();

    const body = document.getElementsByTagName("body")[0];
    body.classList.toggle("not-scroll");

    setDetailImageState(false);
  }, []);

  // FIXME: 선택한 이미지 다운로드
  const _handleDownloadImage = useCallback((e, imageId, imageURL) => {
    e.stopPropagation();
    e.preventDefault();

    let downloadLink = document.createElement("a");
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);

    downloadLink.setAttribute("href", imageURL);
    downloadLink.setAttribute("download", imageId);
    downloadLink.click();

    document.body.removeChild(downloadLink);
  }, []);

  return loading ? (
    <Loading text={"이미지를 불러오는중..."} usage={"load"} />
  ) : (
    <div className="private_gallery_box">
      {sort === "필터별" ? (
        <>
          <div className="filter_container">
            <button
              className="filter_btn is-selected"
              name="신카이 마코토"
              onClick={_handleSelectFilter}
            >
              신카이 마코토
            </button>
            <button
              className="filter_btn"
              name="미야자키 하야오"
              onClick={_handleSelectFilter}
            >
              미야자키 하야오
            </button>
            <button
              className="filter_btn"
              name="호소 다 마모루"
              onClick={_handleSelectFilter}
            >
              호소 다 마모루
            </button>
          </div>
          {publicImages.length > 0 ? (
            <div className="private_gallery_grid">
              {publicImages.map((publicImage) => (
                <PublicImageComponent
                  key={publicImage["imageId"]}
                  type="public"
                  publicImage={publicImage}
                  _handleSelectDetailImage={_handleSelectDetailImage}
                  _handleCancelDetailImage={_handleCancelDetailImage}
                  _handleDownloadImage={_handleDownloadImage}
                />
              ))}
            </div>
          ) : (
            <span className="none_private_image">
              공개 갤러리에 이미지가 없습니다.
            </span>
          )}
        </>
      ) : publicImages.length > 0 ? (
        <div className="private_gallery_grid">
          {publicImages.map((publicImage) => (
            <PublicImageComponent
              key={publicImage["imageId"]}
              type="public"
              publicImage={publicImage}
              _handleSelectDetailImage={_handleSelectDetailImage}
              _handleCancelDetailImage={_handleCancelDetailImage}
              _handleDownloadImage={_handleDownloadImage}
            />
          ))}
        </div>
      ) : (
        <span className="none_private_image">
          공개 갤러리에 이미지가 없습니다.
        </span>
      )}
      {detailImageState ? (
        <DetailImageComponent
          type="public"
          detailImage={detailImage}
          _handleCancelDetailImage={_handleCancelDetailImage}
          _handleDownloadImage={_handleDownloadImage}
        />
      ) : (
        <></>
      )}
    </div>
  );
};

export default PublicGallery;
