import React, { useRef, useState } from "react";
import LoginPresenter from "./LoginPresenter";
import { loginApi } from "../../api";

const LoginContainer = ({ history }) => {
  const [account, setAccount] = useState({
    id: "",
    pwd: "",
  });

  const { id, pwd } = account;

  const idRef = useRef();
  const pwdRef = useRef();

  const _handleInputAccount = (e) => {
    const newAccount = {
      ...account,
      [e.target.name]: e.target.value,
    };
    setAccount(newAccount);
  };

  const _handleLogin = async () => {
    if (id.length === 0) {
      alert("아이디를 입력해주세요.");
      idRef.current.focus();
      return;
    }

    if (pwd.length === 0) {
      alert("비밀번호를 입력해주세요.");
      pwdRef.current.focus();
      return;
    }

    const { data } = await loginApi.login(id, pwd);

    if (data["result"] === "Success") {
      window.localStorage.setItem("c_access_token", data["access_token"]);
      window.localStorage.setItem("c_uid", data["id"]);
      history.push("/");
      window.location.reload();
      return;
    } else {
      alert(data["result"]);
      return;
    }
  };

  return (
    <LoginPresenter
      account={account}
      idRef={idRef}
      pwdRef={pwdRef}
      _handleInputAccount={_handleInputAccount}
      _handleLogin={_handleLogin}
    />
  );
};

export default LoginContainer;
