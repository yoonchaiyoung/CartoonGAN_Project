import React from "react";
import { Helmet } from "react-helmet";
import styled, { keyframes } from "styled-components";

const introAnimation = keyframes`
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
`;

const Login = styled.div`
  width: 100%;
  min-height: 100vh;

  background: #222831;

  display: flex;
  justify-content: center;
  align-items: center;
`;

const LoginContainer = styled.div`
  min-width: 50vh;
  height: 60vh;
  border-radius: 20px;
  box-shadow: 2px 2px 6px black;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: ${introAnimation} 1s ease-in-out;

  @media screen and (max-width: 400px) {
    border: none;
    box-shadow: none;
  }
`;

const Title = styled.h1`
  font-size: 2rem;
  color: white;
`;

const LoginForm = styled.div`
  width: 100%;
  height: 100%;
  padding: 10px 0px;

  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
`;

const LoginInputContainer = styled.div`
  width: 70%;

  z-index: 10;
`;

const LoginInput = styled.input`
  width: 100%;
  height: 3vh;
  outline: 0;
  font-size: 18px;
  color: white;
  background-color: transparent;
  border: none;
  border-bottom: 1px solid white;
`;

const LoginInputTitle = styled.h1`
  color: white;
`;

const LoginButton = styled.button`
  width: 70%;
  height: 4vh;
  color: black;
  background-color: white;
  border-radius: 20em;
  transition: 0.2s ease-in-out;

  :hover {
    opacity: 0.7;
  }
`;

const LoginPresenter = ({
  account,
  _handleInputAccount,
  _handleLogin,
  idRef,
  pwdRef,
}) => {
  const { id, pwd } = account;
  return (
    <>
      <Helmet>
        <title>ARTWORKER | 로그인</title>
      </Helmet>
      <Login>
        <LoginContainer>
          <LoginForm>
            <Title>ARTWORKER</Title>
            <LoginInputContainer>
              <LoginInputTitle>아이디</LoginInputTitle>
              <LoginInput
                name="id"
                type="text"
                value={id}
                onChange={_handleInputAccount}
                ref={idRef}
              />
            </LoginInputContainer>
            <LoginInputContainer>
              <LoginInputTitle>비밀번호</LoginInputTitle>
              <LoginInput
                name="pwd"
                type="password"
                value={pwd}
                onChange={_handleInputAccount}
                ref={pwdRef}
              />
            </LoginInputContainer>
            <LoginButton onClick={() => _handleLogin()}>로그인</LoginButton>
          </LoginForm>
        </LoginContainer>
      </Login>
    </>
  );
};

export default LoginPresenter;
