import React, { useEffect, useState, useCallback } from "react";
import "../../../Style/Gallery/PrivateGalleryStyle.css";
import { galleryApi } from "../../../api";
import PrivateImageComponent from "./PrivateImageComponent";
import DetailImageComponent from "../DetailImageComponent";
import Loading from "../../../Components/Loading";

const PrivateGallery = ({ sort }) => {
  const [privateImages, setPrivateImages] = useState([]);
  const [act, setAct] = useState(0);
  const [detailImageState, setDetailImageState] = useState(false);
  const [detailImage, setDetailImage] = useState({});
  const [loading, setLoading] = useState(false);

  // FIXME: sorting 방법에 따라 리로드..
  useEffect(() => {
    const id = window.localStorage.getItem("c_uid");

    const getPrivateData = async () => {
      setLoading(true);
      let data = await galleryApi.getPrivate(id, sort);

      let {
        data: { private_images },
      } = data;

      setPrivateImages(private_images);
      setLoading(false);
    };

    getPrivateData();
  }, [sort, act]);

  // FIXME: 필터 선택 및 데이터 가져오기
  const _handleSelectFilter = useCallback((e) => {
    const id = window.localStorage.getItem("c_uid");
    // 필터에 맞는 데이터 가져오기
    const getFilterData = async () => {
      let data = await galleryApi.getPrivateByFilter(id, e.target.name);
      let {
        data: { filter_images },
      } = data;

      setPrivateImages(filter_images);
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

  // FIXME: 이미지를 공개 갤러리로
  const _handleMovePublicImage = useCallback(
    (e) => {
      e.stopPropagation();
      e.preventDefault();

      let result = window.confirm(
        "선택하신 이미지를 공개갤러리에 업로드 하시겠습니까?"
      );

      if (result) {
        const id = e.target.id.split("/")[0];
        const imageId = e.target.id.split("/")[1];

        galleryApi.share(id, imageId);

        setAct(act + 1);
      }
    },
    [act]
  );

  // FIXME: 이미지를 개인 갤러리로
  const _handleMovePrivateImage = useCallback(
    (e) => {
      e.stopPropagation();
      e.preventDefault();

      let result = window.confirm(
        "선택하신 이미지를 공개갤러리에서 내리시겠습니까?"
      );

      if (result) {
        const id = e.target.id.split("/")[0];
        const imageId = e.target.id.split("/")[1];

        galleryApi.unshare(id, imageId);

        setAct(act + 1);
      }
    },
    [act]
  );

  // FIXME: 선택한 이미지 삭제
  const _handleDeleteImage = useCallback(
    (e) => {
      e.stopPropagation();
      e.preventDefault();

      let result = window.confirm("선택하신 이미지를 삭제하시겠습니까?");

      if (result) {
        const id = e.target.id.split("/")[0];
        const imageId = e.target.id.split("/")[1];

        const imageDelete = async () => {
          const {
            data: { result },
          } = await galleryApi.delete(id, imageId);

          if (result === "OK") {
            setAct(act + 1);
          }
        };

        imageDelete();
      }
    },
    [act]
  );

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
          {privateImages.length > 0 ? (
            <div className="private_gallery_grid">
              {privateImages.map((privateImage) => (
                <PrivateImageComponent
                  key={privateImage["imageId"]}
                  type="public"
                  privateImage={privateImage}
                  _handleSelectDetailImage={_handleSelectDetailImage}
                  _handleCancelDetailImage={_handleCancelDetailImage}
                  _handleDownloadImage={_handleDownloadImage}
                  _handleMovePublicImage={_handleMovePublicImage}
                  _handleMovePrivateImage={_handleMovePrivateImage}
                  _handleDeleteImage={_handleDeleteImage}
                />
              ))}
            </div>
          ) : (
            <span className="none_private_image">
              개인 갤러리에 이미지가 없습니다.
            </span>
          )}
        </>
      ) : privateImages.length > 0 ? (
        <div className="private_gallery_grid">
          {privateImages.map((privateImage) => (
            <PrivateImageComponent
              key={privateImage["imageId"]}
              type="private"
              privateImage={privateImage}
              _handleMovePublicImage={_handleMovePublicImage}
              _handleMovePrivateImage={_handleMovePrivateImage}
              _handleDeleteImage={_handleDeleteImage}
              _handleSelectDetailImage={_handleSelectDetailImage}
              _handleDownloadImage={_handleDownloadImage}
            />
          ))}
        </div>
      ) : (
        <span className="none_private_image">
          개인 갤러리에 이미지가 없습니다.
        </span>
      )}
      {detailImageState ? (
        <DetailImageComponent
          type="private"
          detailImage={detailImage}
          _handleCancelDetailImage={_handleCancelDetailImage}
          _handleMovePublicImage={_handleMovePublicImage}
          _handleMovePrivateImage={_handleMovePrivateImage}
          _handleDeleteImage={_handleDeleteImage}
          _handleDownloadImage={_handleDownloadImage}
        />
      ) : (
        <></>
      )}
    </div>
  );
};

export default PrivateGallery;
