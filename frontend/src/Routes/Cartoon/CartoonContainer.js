import CartoonPresenter from "./CartoonPresenter";
import React, { useCallback, useState } from "react";
import { imageApi } from "../../api";

const CartoonContainer = () => {
  const [filter, setFilter] = useState("");
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [transition, setTransition] = useState(false);

  // ======================= 변환 후 사용 될 State ==================

  const [cartoonImages, setCartoonImages] = useState([]);
  const [mainImage, setMainImage] = useState("");

  // =============================================================

  // FIXME: 드래그 시작
  const _handleOnDragEnter = useCallback((e) => {
    e.stopPropagation();
    e.preventDefault();

    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      let drag_box = document.querySelector(".drag_box");
      let drag_navigate = document.querySelector(".drag_navigate");

      if (
        drag_box.classList.length === 1 &&
        drag_navigate.classList.length === 1
      ) {
        drag_box.classList.toggle("is-active");
        drag_navigate.classList.toggle("is-active");
      }

      // 이미지가 몇 개 올려진게 있으면..
      if (document.querySelector(".image_grid") !== null) {
        const image_grid = document.querySelector(".image_grid");

        if (image_grid.classList.length === 1) {
          image_grid.classList.toggle("disable");
        }
      }
    }
  }, []);

  // FIXME: 드래그 끝
  const _handleOnDragLeave = useCallback((e) => {
    e.stopPropagation();
    e.preventDefault();

    let drag_box = document.querySelector(".drag_box");
    let drag_navigate = document.querySelector(".drag_navigate");

    if (
      drag_box.classList.length === 2 &&
      drag_navigate.classList.length === 2
    ) {
      drag_box.classList.toggle("is-active");
      drag_navigate.classList.toggle("is-active");
    }

    if (document.querySelector(".image_grid") !== null) {
      const image_grid = document.querySelector(".image_grid");

      if (image_grid.classList.length === 2) {
        image_grid.classList.toggle("disable");
      }
    }
  }, []);

  // FIXME: 드래그 오버
  const _handleOnDragOver = useCallback((e) => {
    e.stopPropagation();
    e.preventDefault();
  }, []);

  // FIXME: 이미지 미리보기
  const _handleFiles = useCallback(
    (files) => {
      let inputFiles = Array.from(files);
      let result = true;
      // 이미지 파일인지 검사
      inputFiles.forEach((file) => {
        if (!file.type.startsWith("image/")) {
          alert("이미지 파일만 넣어주세요.");
          result = false;
        }
        if (file.type.startsWith("image/svg")) {
          alert("벡터 이미지는 넣을실 수 없습니다.");
          result = false;
        }
      });

      if (!result) {
        return;
      }

      // 비회원은 한 장만
      if (!Boolean(window.localStorage.getItem("c_uid"))) {
        if (images.length + files.length > 1) {
          alert("비회원은 이미지를 한 장만 올리실 수 있습니다.");
          return;
        }
      }
      // 이미지는 5장까지만
      if (Boolean(window.localStorage.getItem("c_uid"))) {
        if (images.length + files.length > 5) {
          alert("이미지는 5장까지만 업로드해주세요.");
          return;
        }
      }

      const getRandomInt = (min, max) => {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min)) + min; //최댓값은 제외, 최솟값은 포함
      }

      // 만약 images.length 가 0이 아니면, index = images.length 부터 시작
      // imageLength = imageLength + images.legnth
      let newImages = [...images];

      inputFiles.forEach((file) => {
        let reader = new FileReader();
        reader.onload = () => {
          const newImage = {
            id: getRandomInt(0, 10000),
            image: file,
            imageURL: reader.result,
          };
          newImages.push(newImage);
          setImages(newImages);
        };

        reader.readAsDataURL(file);
      });
    },
    [images]
  );

  // FIXME: 드랍
  const _handleOnDrop = useCallback(
    (e) => {
      e.stopPropagation();
      e.preventDefault();

      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        _handleFiles(e.dataTransfer.files);

        let drag_box = document.querySelector(".drag_box");
        let drag_navigate = document.querySelector(".drag_navigate");

        if (
          drag_box.classList.length === 2 &&
          drag_navigate.classList.length === 2
        ) {
          drag_box.classList.toggle("is-active");
          drag_navigate.classList.toggle("is-active");
        }

        if (document.querySelector(".image_grid") !== null) {
          const image_grid = document.querySelector(".image_grid");

          if (image_grid.classList.length === 2) {
            image_grid.classList.toggle("disable");
          }
        }
      }
    },
    [_handleFiles]
  );

  // FIXME: 이미지 업로드 클릭 시
  const _handleOnClick = useCallback(() => {
    const fileElem = document.getElementById("fileElem");
    fileElem.click();
  }, []);

  // FIXME: 이미지 업로드 시
  const _handleOnUpload = useCallback(() => {
    const fileElem = document.getElementById("fileElem");
    _handleFiles(fileElem.files);
  }, [_handleFiles]);

  // 이미지 삭제
  const _handleImageDelete = useCallback(
    (e) => {
      e.stopPropagation();
      e.preventDefault();

      let result = window.confirm("선택하신 이미지를 지우시겠습니까?");
      if (result) {
        const newImages = images.filter(
          (image) => image.id.toString() !== e.target.id
        );
        setImages(newImages);
      }
    },
    [images]
  );

  // FIXME: 이미지 변환
  const _handleImageTransition = useCallback(
    async (e) => {
      e.stopPropagation();
      e.preventDefault();

      // 필터 선택했는지 확인
      if (filter === "") {
        alert("필터를 선택해주세요");
        return;
      }

      const imageFiles = [];

      images.forEach((image) => {
        imageFiles.push(image["imageURL"]);
      });

      setLoading(true);

      const {
        data: { imageLength, cartoonImages },
      } = await imageApi.imageTransition(filter, imageFiles, imageFiles.length);

      const newCartoonImages = [];

      for (let i = 0; i < imageLength; i++) {
        const newCartoonImage = {
          id: i,
          imageURL: cartoonImages[`image${i}`],
        };
        newCartoonImages.push(newCartoonImage);
      }
      setCartoonImages(newCartoonImages);
      setMainImage(newCartoonImages[0]);

      setImages([]);
      setLoading(false);
      setTransition(true);
    },
    [filter, images]
  );

  // FIXME: 필터 선택
  const _handleSelectFilter = useCallback((e, filterName) => {
    e.stopPropagation();
    e.preventDefault();

    if (document.getElementsByClassName("is-selected")[0]) {
      const active_filter = document.getElementsByClassName("is-selected")[0];
      active_filter.classList.toggle("is-selected");
    }

    const new_filter = document.getElementById(filterName);
    new_filter.classList.toggle("is-selected");

    setFilter(e.target.name);
  }, []);

  // ========================= 번환 후 사용될 함수 =========================

  // FIXME: Main 이미지 변환
  const _handleSelectMainImage = (e) => {
    e.stopPropagation();
    e.preventDefault();

    const mainImage = {
      id: e.target.name,
      imageURL: e.target.src,
    };
    setMainImage(mainImage);
  };

  // FIXME: 이미지 다운로드
  const _handleImagesDownload = (e) => {
    e.stopPropagation();
    e.preventDefault();

    let downloadLink = document.createElement("a");
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);

    for (let idx = 0; idx < cartoonImages.length; idx++) {
      let cartoonImage = cartoonImages[idx];

      downloadLink.setAttribute("href", cartoonImage["imageURL"]);
      downloadLink.setAttribute("download", `image${idx}`);
      downloadLink.click();
    }

    document.body.removeChild(downloadLink);
  };

  // FIXME: 되돌아가기 버튼
  const _handleReset = (e) => {
    e.stopPropagation();
    e.preventDefault();

    let result = window.confirm("이미지 변환 화면으로 돌아가시겠습니까?");
    if (result) {
      setTransition(false);
      setCartoonImages([]);
      setMainImage("");
    } else {
      return;
    }
  };

  // ======================== Presenter ======================

  return (
    <CartoonPresenter
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
      loading={loading}
      transition={transition}
      cartoonImages={cartoonImages}
      mainImage={mainImage}
      _handleSelectMainImage={_handleSelectMainImage}
      _handleImagesDownload={_handleImagesDownload}
      _handleReset={_handleReset}
    />
  );
};

export default CartoonContainer;
