import React, { useCallback, useMemo, useState } from "react";
import GalleryPresenter from "./GalleryPresenter";

const GalleryContainer = () => {
  const [title, setTitle] = useState("공개갤러리");
  const [sort, setSort] = useState("최신순");
  const filters = useMemo(() => ["신카이 마코토", "미야자키 하야오", "호소 다 마모루"], [])

  // FIXME: 공개 / 개인 변환
  const _handleGalleryCategory = useCallback((e) => {
    e.stopPropagation();
    e.preventDefault();

    if (
      e.target.id === "개인갤러리" &&
      window.localStorage.getItem("c_access_token") === null
    ) {
      alert("비회원유저는 개인갤러리를 이용하실 수 없습니다.");
      return;
    }

    let category_active = document.getElementsByClassName("is-active");
    let category = document.getElementById(e.target.id);

    category_active[0].className = category_active[0].className.replace(
      " is-active",
      ""
    );
    category.className += " is-active";
    setTitle(e.target.id);
  }, []);

  // FIXME: 정렬방식 타이틀 클릭
  const _handleClickSortingWayTitle = useCallback((e) => {
    e.stopPropagation();
    e.preventDefault();

    let dropdown = document.querySelector(".sortingway_dropdown_items");
    if (dropdown.className.includes("is-active")) {
      dropdown.className = dropdown.className.replace("is-active", "");
    } else {
      dropdown.className += " is-active";
    }
  }, []);

  // FIXME: 정렬방식 변경
  const _handleSortingWay = useCallback((e) => {
    e.stopPropagation();
    e.preventDefault();

    setSort(e.target.name);

    let dropdown = document.querySelector(".sortingway_dropdown_items");
    dropdown.className = dropdown.className.replace("is-active", "");
  }, []);

  return (
    <GalleryPresenter
      title={title}
      _handleGalleryCategory={_handleGalleryCategory}
      _handleClickSortingWayTitle={_handleClickSortingWayTitle}
      sort={sort}
      _handleSortingWay={_handleSortingWay}
      filters={filters}
    />
  );
};

export default GalleryContainer;
