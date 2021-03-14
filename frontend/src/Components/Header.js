import React, { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../Style/Header.css";

const Header = () => {
  const [login, setLogin] = useState(false);

  useEffect(() => {
    const status = window.localStorage.getItem("c_access_token");
    setLogin(Boolean(status));
  }, [login]);

  const _handleLogout = useCallback(() => {
    const result = window.confirm("로그아웃 하시겠습니까?");
    if (result) {
      window.localStorage.removeItem("c_access_token");
      window.localStorage.removeItem("c_uid");
      setLogin(false);
    }
  }, []);

  const _handleBurger = useCallback(() => {
    const navLinks = document.querySelector(".nav-links");
    const burger = document.querySelector(".burger");
    const body = document.getElementsByTagName("body")[0];

    navLinks.classList.toggle("nav-active");
    burger.classList.toggle("toggle");
    body.classList.toggle("not-scroll");
  }, []);

  const _handleClickLink = useCallback(() => {
    const burger = document.querySelector(".burger");
    const nav = document.querySelector(".nav-links");
    const body = document.getElementsByTagName("body")[0];

    nav.classList.toggle("nav-active");
    burger.classList.toggle("toggle");
    
    for (let className of body.classList) {
      if (className === "not-scroll") {
        body.classList.toggle("not-scroll");
        break;
      }
    }

  }, []);

  return (
    <>
      <nav className="nav">
        <Link className="logo" to="/">
          ARTWORKER
        </Link>

        <div className="nav-links">
          <Link className="link" to="/filter" onClick={_handleClickLink}>
            필터
          </Link>
          <Link className="link" to="/cartoon" onClick={_handleClickLink}>
            이미지 변환
          </Link>
          <Link className="link" to="/gallery" onClick={_handleClickLink}>
            갤러리
          </Link>
          {login ? (
            <button onClick={_handleLogout}>로그아웃</button>
          ) : (
            <>
              <Link className="link" to="/login" onClick={_handleClickLink}>
                로그인
              </Link>
              <Link
                className="link"
                to="/login/createAccount"
                onClick={_handleClickLink}
              >
                회원가입
              </Link>
            </>
          )}
        </div>
        <div className="burger" onClick={_handleBurger}>
          <div className="line1"></div>
          <div className="line2"></div>
          <div className="line3"></div>
        </div>
      </nav>
    </>
  );
};

export default Header;
