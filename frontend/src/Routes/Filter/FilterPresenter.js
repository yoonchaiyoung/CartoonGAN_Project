import React, { useState, useMemo, useCallback } from "react";
import PlotPresenter from "./Plot/PlotPresenter";
import "../../Style/Filter/FilterPresenter.css";
import Helmet from "react-helmet";

const FilterPresenter = () => {
  const [filterName, setFilterName] = useState([
    "초속 5센티미터",
    "5Centimater_crop_BGR",
  ]);

  const filterNames = useMemo(
    () => [
      ["초속 5센티미터", "5Centimater_crop_BGR"],
      ["하울의 움직이는 성", "Howls_crop_BGR"],
      ["파프리카", "Paprika_BGR"],
      ["겨울 왕국", "snow_BGR"],
      ["썸머워즈", "SummerWars_RGB_6cut"],
      ["너의 이름은", "yourname_RGB_6cut"],
    ],
    []
  );

  // FIXME: 필터 사용법 보는 버튼
  const _handleSetFilterInfo = useCallback((e) => {
    e.stopPropagation();
    e.preventDefault();

    const info_container = document.querySelector(".info_container");
    const body = document.getElementsByTagName("body")[0];
    info_container.classList.toggle("is-active");
    body.classList.toggle("not-scroll");
  }, []);

  // FIXME: 필터 버튼
  const _handleClickFilterBtn = useCallback((e) => {
    e.stopPropagation();
    e.preventDefault();

    const filter_btn = document.querySelector(".filter_select_list");
    filter_btn.classList.toggle("is-active");
  }, []);

  // FIXME: 필터 선택
  const _handleSelectFilter = useCallback((e) => {
    e.stopPropagation();
    e.preventDefault();

    setFilterName(e.target.value.split(","));

    const filter_btn = document.querySelector(".filter_select_list");
    filter_btn.classList.toggle("is-active");
  }, []);

  return (
    <>
      <Helmet>
        <title>ARTWORKER | 필터</title>
      </Helmet>
      <div className="filter_container">
        <div className="filter_page_info">
          <ion-icon
            className="info_btn"
            name="alert-circle-outline"
            onClick={_handleSetFilterInfo}
          ></ion-icon>
        </div>
        <div>
          <button
            className="filter_selected_btn"
            onClick={_handleClickFilterBtn}
          >
            {filterName[0]}
          </button>
          <div className="filter_select_list">
            {filterNames.map(
              (filter) =>
                filter[0] !== filterName[0] && (
                  <button
                    key={filter}
                    value={filter}
                    className="filters"
                    onClick={_handleSelectFilter}
                  >
                    {filter[0]}
                  </button>
                )
            )}
          </div>
        </div>
        <PlotPresenter csvFile={filterName[1]} />
      </div>
      {/* 필터 페이지란 무엇인가...? */}
      <div className="info_container">
        <div className="info_close">
          <ion-icon name="close-circle-outline"></ion-icon>
        </div>
        <div className="info_box"></div>
        <div className="info_overlay"></div>
      </div>
    </>
  );
};

export default FilterPresenter;
