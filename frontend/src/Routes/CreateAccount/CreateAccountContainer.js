import CreateAccountPresenter from "./CreateAccountPresenter";
import React, { useState } from "react";
import { createAccountApi } from "../../api";

const CreateAccountContainer = ({ history }) => {
  const [account, setAccount] = useState({
    id: "",
    pwd: "",
  });

  const { id, pwd } = account;

  const [checkId, setCheckId] = useState(false);

  // 아이디, 비밀번호 입력
  const _handleAccountUpdate = (e) => {
    const newAccount = {
      ...account,
      [e.target.name]: e.target.value,
    };
    setAccount(newAccount);
  };

  // id 중복체크
  const _handleCheckId = async (id) => {
    if (id.length === 0 || id.length < 4) {
      alert("아이디는 4자 이상 입력해주세요.");
      return;
    }

    const {
      data: { result },
    } = await createAccountApi.checkId(id);

    if (result === "Success") {
      setCheckId(true);
      alert("사용가능한 아이디입니다.");
    } else {
      setCheckId(false);
      alert("입력하신 아이디가 이미 존재합니다.");
    }
  };

  // 계정생성
  const _handleCreateAccount = async () => {
    if (!checkId) {
      alert("아이디 중복확인을 해주세요.");
      return;
    }

    if (pwd.length === 0 || pwd.length < 4) {
      alert("비밀번호는 4자 이상 입력해주세요.");
      return;
    }

    const {
      data: { result },
    } = await createAccountApi.createAccount(id, pwd);
    if (result === "Success") {
      alert("가입되었습니다!");
      history.push("/login");
    }
  };

  return (
    <CreateAccountPresenter
      account={account}
      _handleAccountUpdate={_handleAccountUpdate}
      _handleCheckId={_handleCheckId}
      _handleCreateAccount={_handleCreateAccount}
    />
  );
};

export default CreateAccountContainer;
